import os
import shutil
import numpy as np
import pandas as pd 
from os import listdir 
import paths

string_of_start_of_json_stuff = "info para json"

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

def create_messages(df,case_folder_path):
    df = df.T
    df.columns = df.iloc[0]
    df = df[1:]
    printCompleteDf(df)
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
                            # insert the copy into the data frame at index row_index
                            print(copy_of_row)
                            #df.reset_index(inplace=True)
                            df = df.append(copy_of_row)
                            made_new_row = True
                        # remove the original row
                        df = df.drop(df.index[row_index])
                        break
    return df.T

    
    

def decompress_excel_messages(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        
        path = message_details_folder_path + "\\" + excel
        name = excel.rsplit("_",1)[1].replace(".xlsx", "")
        base_path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
        case_folder_path = make_message_case_folder(base_path,name)
        pd.set_option('display.max_rows', None)
        df = pd.read_excel(path, sheet_name='compressed cases')
        df.style.hide_index()

        df = df[df[df.columns.tolist()[0]].notna()]
        
        df = create_messages(df,case_folder_path)
        # save the new df in a new sheet of the excel file 
        excel_path = message_details_folder_path + "\\" + excel
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode="a", if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='decompressed cases')

        print("pause    ")
        
        
