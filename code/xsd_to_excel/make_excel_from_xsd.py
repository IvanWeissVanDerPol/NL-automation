import json
import shutil
from re import L
import pandas as pd
from os import listdir
import sys
from xsd_to_excel.complex_element import Complex_Element_Object
from xsd_to_excel.xsd_converter_to_tree import get_tree
sys.path.append("..")
sys.path.append("...")
import paths
import element_tests
import os
import xlsxwriter

#traverse the tree and add each node to the list of list (each list in the list represents a column in the final excel)
# might not be the best way but its "a" way ja ja ja
def traverse_tree(node:Complex_Element_Object ,listOLists):
    
    for cont in range (1,node.height+1):
        df_level = "L" + str(cont)    
        listOLists[df_level].append("")       

    
    
    df_level = "L" + str(node.level)
    listOLists[df_level].pop()
    aux_name =  node.complex_data.Name 
    if len(node.children) == 0:
        aux_name =  node.complex_data.Name + "_LEAF_NODE"
    listOLists[df_level].append(aux_name)      
    
    listOLists["DEFAULT VALUES"].append("")
    
    #do the same for each child of the node        
    for child in node.children:
        traverse_tree(child,listOLists)

#make an excel for each xsd in the folder
#open the folder and get the root from the xsd
#initialize lists of list as empty this lists represent columns in the final excel
#load the BS json file (business logic or something)
#save the excel
def make_excels_from_xsd(folder_Of_xsd):
    folder_path = folder_Of_xsd
    folder = listdir(folder_path)
    for file in folder:
        if file.endswith(".xsd"):
            file_path = folder_path + "\\" + file
            done_processing_path = folder_path + "\\done\\" + file
            name = file_path.split(".")[0].rsplit("\\")[1]
            #generate the tree from the xsd
            root = get_tree(xsd_path=file_path)
            
            path = paths.message_details_folder_path + "\\message_details_" + name + ".xlsx"
            listOLists = {}

            #initialize the list of list as empty             
            for cont in range (1,root.height+1):
                df_level = "L" + str(cont)    
                listOLists[df_level] = [] 
            listOLists["DEFAULT VALUES"] = []

            #make the list of lists and turn it in to an excel sheet
            traverse_tree(root,listOLists)

            df = pd.DataFrame(data=listOLists)
            writer = pd.ExcelWriter(path=path, engine='xlsxwriter',mode='w')
            df.to_excel(writer, sheet_name='compressed cases',index=False)
            writer.save()
            add_paths(path)
            # shutil.move(file_path, done_processing_path)
            

def add_paths(excel_path):
        df = pd.read_excel(excel_path)                                    #get the excel file you want to process
        columns=list(df.columns.values)
        #read the rows
        element_path = {}
        aux_col = []                                                #auxiliary column to figure out the path of an element in the xsd tree
        for col in columns:
            if col.startswith('L'):
                aux_col.append(col)
        list_of_xml_elements_paths_strings = []
        for row in df.iterrows():
            row = row[1]
            element_path_string = ""

            for col in aux_col:
                if not pd.isnull(row[col]):
                    element_path[col] = row[col]
                    index = aux_col.index(col)
                    for pos in range(index+1,len(aux_col)):
                        element_path[aux_col[pos]] = ""
                
                if not(pd.isnull(row[col])): 
                    element_path_list = list(element_path.values())
                    element_path_list = list(filter(("").__ne__, element_path_list))
                    element_path_string = "/".join(element_path_list)

            list_of_xml_elements_paths_strings.append(element_path_string)

        
        #remove non leaf nodes
        strings_to_remove = []
        for num in range(0,len(list_of_xml_elements_paths_strings)):
            string = list_of_xml_elements_paths_strings[num]
            if  "_LEAF_NODE" not in string:
                strings_to_remove.append(string)
            else:
                string = string.replace("_LEAF_NODE", "")
                list_of_xml_elements_paths_strings[num] = string
                
        for string in strings_to_remove:
            list_of_xml_elements_paths_strings.remove(string)
            
        json_info = ["","info para json", "message path", "message name", "values file", "error code", "Message ID", "startDate", "endDate", "receiver", "grid_point", "direction", "timeSeries", "struct", "struct_market_paries", "struct_net_areas", "struct_grid_points", "struct_supply_contracts", "struct_connections"]    
        list_of_xml_elements_paths_strings = list_of_xml_elements_paths_strings + json_info
        df = pd.DataFrame(list_of_xml_elements_paths_strings, columns=['XML ELEMENT PATH'])
        df["DEFAULT VALUES"] = ""
        writer = pd.ExcelWriter(path=excel_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='compressed cases',index=False,columns = ['XML ELEMENT PATH','DEFAULT VALUES'])
        writer.save()