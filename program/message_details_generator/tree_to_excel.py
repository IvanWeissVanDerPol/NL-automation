import json
import shutil
import os
from re import L
import pandas as pd
import xlsxwriter
from os import listdir
import sys
sys.path.append("..")
sys.path.append("...")
import paths
import message_details_generator.xsd_converter_to_tree as xsd_converter_to_tree
import message_details_generator.complex_element as complex_element
import element_tests

#traverse the tree and add each node to the list of list (each list in the list represents a column in the final excel)
# might not be the best way but its "a" way ja ja ja
def traverse_tree(node:complex_element ,listOLists,json_file):
    if node.complex_data.Name in json_file:
        sub_json = json_file[node.complex_data.Name]
    else:
        sub_json = json_file
    
    for cont in range (1,node.height+1):
        df_level = "L" + str(cont)    
        listOLists[df_level].append("")       

    df_level = "L" + str(node.level)
    listOLists[df_level].pop()
    listOLists[df_level].append(node.complex_data.Name)       
    listOLists["Type"].append(node.complex_data.Type)       
    listOLists["Cardinality"].append(node.complex_data.Cardinality)       
    listOLists["BaseType"].append(node.complex_data.Base_Type)       
    listOLists["Constraints"].append(node.complex_data.Constraints)
    listOLists["Enumerations"].append(node.complex_data.Enumerations)
    listOLists["DEFAULT VALUES"].append("")
    
    if(node.complex_data.Base_Type != ""):
        string = node.complex_data.Name + "_1",node.complex_data.Name + "_2"
        tests = element_tests.tests
        # listOLists["Tests Values"].append(string)
    # else:
        # listOLists["Tests Values"].append("")
    if "Data type" in sub_json:
        listOLists["BS data Type"].append(sub_json['Data type'])
        listOLists["BS description"].append(sub_json['description'])
        listOLists["BS functional Parameter"].append(sub_json['functional parameter'])
    else:
        listOLists["BS data Type"].append("")
        listOLists["BS description"].append("")
        listOLists["BS functional Parameter"].append('')
        

    #do the same for each child of the node        
    for child in node.children:
        traverse_tree(child,listOLists,sub_json)

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
            root = xsd_converter_to_tree.get_tree(xsd_path=file_path)
            
            path = paths.message_details_folder_path + "\\message_details_" + name + ".xlsx"
            listOLists = {}

            #initialize the list of list as empty             
            for cont in range (1,root.height+1):
                df_level = "L" + str(cont)    
                listOLists[df_level] = [] 
            listOLists["Type"] = []
            listOLists["Cardinality"] = []
            listOLists["BaseType"] = []
            listOLists["Constraints"] = []
            listOLists["Enumerations"] = []
            listOLists["DEFAULT VALUES"] = []
            listOLists["BS data Type"] = []
            listOLists["BS description"] = []
            listOLists["BS functional Parameter"] = []

            #make the list of lists and turn it in to an excel sheet
            json_file = json.load(open(paths.BS_json_path))
            traverse_tree(root,listOLists,json_file)
            #make the tests cases excel
            df = pd.DataFrame(data=listOLists)
            writer = pd.ExcelWriter(path=path, engine='xlsxwriter',mode='w')
            df.to_excel(writer, sheet_name='Sheet1',index=False)
            writer.save()
            shutil.move(file_path, done_processing_path)
            

