import os
import shutil
from matplotlib.pyplot import pause
import numpy as np
import pandas as pd 
from os import listdir 
import paths
from bs4 import BeautifulSoup
import lxml
import xml.dom.minidom as minidom

string_of_start_of_json_stuff = "info para json"
string_of_values_file = "values file"

def printCompleteDf(df):
    pd.set_option("max_rows", None)
    pd.set_option("max_columns", None)
    print(df)

def make_message_case_folder(path,test_message):
    test_case_path = path.rsplit("\\",1)[1]
    test_case_path = test_case_path.replace("base_", "")
    name = test_case_path.replace(".xml", "")

    test_folder = paths.xmls_cases_folder_path + "\\" + name
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    test_case_path = test_folder + "\\" + "base.xml"
    shutil.copyfile(path, test_case_path)
    return test_folder

def create_messages(df):
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]
    #the idea
    #it receives a data frame where each column is a field of a message and each row is a message
    # mi intent is to first go across each row and see if it has an array [val1, val2] in it
    # if it has an array make a x copy of the row and place the value of the array in the corresponding field where x is the number of elements in the array
    # then continue to the next field and so on until the end   
    made_new_row = True
    while(made_new_row):
        made_new_row = False
        for row in df.iterrows():
            row = row[1]
            row_index = list(df.index).index(row.name)
            #iterate across the columns and print the values
            for col in df.columns:
                if not pd.isna(col):
                    value = row[col]
                    if not pd.isna(value):
                        value = ""
                    if "[" in str(row[col]):
                        array = row[col].replace("[", "").replace("]", "").split(",")
                        for element in array:
                            copy_of_row = row.copy()        
                            # modify the copy
                            copy_of_row[col]= element 
                            copy_of_row.name = copy_of_row.name + "_" + str(array.index(element))
                            df = df.append(copy_of_row)
                            made_new_row = True
                        # remove the original row
                        df = df.drop(df.index[row_index])
                        break
    return df.T

    
    

def decompress_excel_messages(excel,message_details_folder_path):
        path = message_details_folder_path + "\\" + excel
        pd.set_option('display.max_rows', None)
        df = pd.read_excel(path, sheet_name='compressed cases')
        df.style.hide_index()

        df = df[df[df.columns.tolist()[0]].notna()]
        df = create_messages(df)

        # save the new df in a new sheet of the excel file 
        excel_path = message_details_folder_path + "\\" + excel
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode="a", if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='decompressed cases')
        
        



def generate_xml_cases_from_decompressed_excel(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        decompress_excel_messages(excel,message_details_folder_path)
        
        path = message_details_folder_path + "\\" + excel
        case_name = excel.rsplit("_",1)[1].replace(".xlsx", "")
        base_path = paths.xmls_folder_path +"\\base\\base_" + case_name + ".xml"
        case_folder_path = make_message_case_folder(base_path,case_name)
        df = pd.read_excel(path, sheet_name='decompressed cases')
        df = df.fillna('')
        #find row that contains the string "info para json" and get the index
        df_col1 = df[df.columns.tolist()[0]]
        index = df_col1[df_col1.str.contains(string_of_start_of_json_stuff)].index.tolist()[0] -1
        #find row that contains values file name
        values_file_index = df_col1[df_col1.str.contains(string_of_values_file)].index.tolist()[0] 
        values_file_name_df = df.iloc[values_file_index]
        #remove every row after the index
        df = df.iloc[:index]
    
        
        df = df.T
        df.style.hide_index()
        df.columns = df.iloc[0]
        df = df[1:]
        #each row is a message  
        #make a copy of the base xml file and modify it
        for row in df.iterrows():
            message_name = row[0]
            time_series_parrent_node = []
            if message_name != "DEFAULT VALUES":
                shutil.copyfile(base_path, case_folder_path + "\\" + message_name + ".xml")
                with open(case_folder_path + "\\" + message_name + ".xml", "r") as file:
                    data = file.read()
                Bs_data = BeautifulSoup(data, "xml",)
                row = row[1]
                #each col is a field of the message 
                #go to that field of the xml and load the new value
                for col in row.index:
                    if "load_from_values_file" in str(row[col]):
                        aux_col = col.rsplit("/",1)[0]
                        if aux_col not in time_series_parrent_node:
                            time_series_parrent_node.append(aux_col)
                    if row[col] != "not_mapped":
                        if "/" in col:
                            element_name_arr = col.rsplit("/")
                            xml_element = Bs_data
                            for element_name in element_name_arr:
                                xml_element = xml_element.find(element_name)
                            xml_element.string = row[col]
                #store the data and remove unused tags
                data = str(Bs_data)
                data = data.split("\n")
                lines_to_remove = []
                for line in data:
                    if "not_mapped" in line:
                        #remove the line from data
                        lines_to_remove.append(line)
                for line in lines_to_remove:
                    data.remove(line)
                
                #remove empty lines
                changes_occurred = True
                while changes_occurred :
                    changes_occurred = False
                    range_of_lines = len(data)-1
                    lines_to_remove = []
                    for line_index in range(0,range_of_lines):
                        current_line = data[line_index]
                        next_line = data[line_index+1]
                        current_line_aux = current_line.replace("</", "<")
                        next_line_aux = next_line.replace("</", "<")
                        if current_line_aux == next_line_aux:
                            lines_to_remove.append(current_line)
                            lines_to_remove.append(next_line)
                            changes_occurred = True
                    for line in lines_to_remove:
                        data.remove(line)
                # add the time series points
                #open the time series values xml from value files
                values_file_name = values_file_name_df[message_name]
                value_file_path = paths.times_txt_paths + "\\" + case_name + "\\" + values_file_name + ".xml"
                with open(value_file_path, "r") as file:
                    values_data = file.read()
                Bs_values = BeautifulSoup(values_data, "xml",)
                Bs_data = BeautifulSoup("".join(data), "xml")
                
                series_blocks = Bs_values.findChildren(recursive=False)[0].findChildren(recursive=False)
                series_block_name = series_blocks[0].name
                parent_node = Bs_data.find(series_block_name).parent
                #remove the original time series block
                parent_node.find(series_block_name).decompose()

                #add each block from series_blocks to the parent node as a child node
                for series_block in series_blocks:
                    parent_node.append(series_block)
                
                data = str(Bs_data).replace("\n", "")
                data = data.replace('<?xml version="1.0" encoding="utf-8"?>', "")
            
                data = data.replace("ccma:", "")
                data = data.replace("<", "<ccma:")
                data = data.replace("<ccma:/", "</ccma:")
                data = data.replace("><", ">\n<")
                data = data.split("\n")
                data = "".join(data)
                
                xml = minidom.parseString(data)
                xml_pretty_str = xml.toprettyxml()
                xml_pretty_str = xml_pretty_str.replace('<?xml version="1.0" ?>\n', "")
                with open(case_folder_path + "\\" + message_name + ".xml", "w") as file:
                    file.write(str(xml_pretty_str))
 
