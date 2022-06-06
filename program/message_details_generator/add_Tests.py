import pandas as pd
from os import listdir
from pandas.io import excel
import xlsxwriter
import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension
import element_tests 
import sys
import json
import paths
sys.path[0] += '\\..'

def add_paths(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        path = message_details_folder_path + "\\" + excel
        df = pd.read_excel(path)                                    #get the excel file you want to process
        excel_df = pd.DataFrame()
        columns=list(df.columns.values)
        test_cases_cont = 0
        #read the rows
        element_path = {}
        aux_col = []                                                #auxiliary column to figure out the path of an element in the xsd tree
        for col in columns:
            if col.startswith('L'):
                aux_col.append(col)
        excel_row = 2
        added_subtitles = False
        list_of_Paths_strings = []
        for row in df.iterrows():
            row = row[1]
            element_path_string = ""

            for col in aux_col:
                if not pd.isnull(row[col]):
                    element_path[col] = row[col]
                    index = aux_col.index(col)
                    for pos in range(index+1,len(aux_col)):
                        element_path[aux_col[pos]] = ""
                        
                
                if not(pd.isnull(row.BaseType)) and not(pd.isnull(row[col])): 
                    if row["Default Values"] != 'not_mapped' : 
                        element_path_list = list(element_path.values())
                        element_path_list = list(filter(("").__ne__, element_path_list))
                        element_path_string = "/".join(element_path_list)
                        added_subtitles = False
            list_of_Paths_strings.append(element_path_string)

        df["path"] = list_of_Paths_strings
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False,columns = ['L1','L2','L3','L4','L5','path','Type','BaseType','Cardinality','Constraints','Default Values','Enumerations','BS data Type','BS description','BS functional Parameter'])
        writer.save()


def add_Tests(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    
    for file in folder:
        #path where the message details excels are stored
        path = message_details_folder_path + "\\" + file
        df = pd.read_excel(path)
        #all the test cases for each element base type tests + type tests
        list_of_tests = []
        list_of_tests2 = []
        
        for row in df.iterrows():
            invalid_keys = []
            tests = ""
            row = row[1]
            path = str(row["path"])
            if path != "nan":
                path = path.split("/",1)[1]
                if path in element_tests.tests:
                    tests = element_tests.tests[path]
                    valid_keys = tests
                    for element in tests:
                        if "Value" in element and tests[element] == [""]: 
                            invalid_keys.append(element)
                            
                    tests = list(valid_keys.keys())
                    #remove invalid keys from tests list
                    for element in invalid_keys:
                        tests.remove(element)
                    tests = str(tests)
            list_of_tests.append(tests)
            list_of_tests2.append("")
            
        df["tests"] = list_of_tests
        #adds empthy column to the excel file where user can decide if info should be in the json
        df['Add to Json'] = list_of_tests2
        #save the generated document
        path = message_details_folder_path + "\\" + file
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()




