import copy
import uuid
from lxml import etree
from typing import ContextManager, Optional
import pandas as pd 
import numpy as np
import sys
import shutil
import os
import re
import json

from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'
import paths
from os import error, listdir
times = json.load(open(paths.times_json_path))
DS_pints_path = json.load(open(paths.DS_path))

#from internet to print jsons nicely
class NoIndent(object):
    def __init__(self, value):
        self.value = value


class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result



def make_base_jsons(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        #make the baseXml file
        make_base_json(excel,message_details_folder_path)
        
def make_base_json(excel_name,message_details_folder_path):
    
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    path = message_details_folder_path + "\\" + excel_name
    df = pd.read_excel(path)
    
    list_of_usefull_columns = ["path","DEFAULT VALUES"]
    columns = list(df.columns.values)
    #remove the columns that are not needed
    df = df[df['Add to Json'].isin(['yes'])]
    for column in columns:
        if column not in list_of_usefull_columns:
            df = df[df.columns.difference([column])]
    #df = df[df["Add to Json"].str.contains('yes')]
    
        
    print(df)
    jsonDict = {}
    for row in df.iterrows():
        row = row[1]
        path = row['path']
        value = str(row['DEFAULT VALUES'])
        jsonDict[path] = value
    jsonDict["ExpectedErrorCode"] = "ExpectedErrorCode_defaultValue"
    print(jsonDict)
    path = paths.xmls_base_folder_path +"\\base_" + name + ".json"
    with open(path, 'w') as json_file:
        json.dump(jsonDict, json_file, indent=1)
    
    
def update_base_jsons():
    excel_folder = listdir(paths.message_details_folder_path)
    for excel in excel_folder:
        excelName = excel.rsplit(".",1)[0]
        corresponding_json = "base_" + excelName.rsplit("_",1)[1] + ".json"
        base_json_path = paths.xmls_base_folder_path + "\\" + corresponding_json
        excel_path = paths.message_details_folder_path + "\\" + excel
        if os.path.isfile(base_json_path):
            update_json(base_json_excel_path=excel_path, base_json_path=base_json_path)

def update_json(base_json_excel_path,base_json_path):
        df = pd.read_excel(base_json_excel_path)
        for ind in df.index:
            element_path = df["path"][ind]
            value = df["DEFAULT VALUES"][ind] 
            if value != "not_mapped" and value != "mapped" and not pd.isnull(value):
                with open(base_json_path) as json_file:
                    data = json.load(json_file)
                data[element_path] = str(value)
                with open(base_json_path, 'w') as json_file:
                    json.dump(data, json_file, indent=1)

def make_test_cases_jsons(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:

        # make the data frame from the test cases excel file
        excel_folder = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(excel_folder)


        list_of_tests_values = []
        list_of_test_path = []
        for row in df.iterrows():
            row = row[1]
            if not pd.isnull(row['new cases']) and not pd.isnull(row["Element"]) and row["new cases"] != "new cases": 
                row["new cases"] = 'True'
                tests_values,new_case_path = create_cases(row=row,excel_name=excel,excel_folder=excel_folder)
                tests_values = "[" + ",".join(tests_values).lstrip(",") + "]"
                
                new_case_path = new_case_path.rsplit("\\",1)[0]
                list_of_tests_values.append(tests_values)
                list_of_test_path.append("C:\\Users\\Ivan\\Documents\\projects\\WPG\\nl protocol\\xsd converter\\" + new_case_path)
                
            else:
                list_of_tests_values.append("")
                list_of_test_path.append("")
            
        #save the excel
        df["current tests values"] = list_of_tests_values 
        df["test folder"] = list_of_test_path         
        # path = paths.xmls_folder_path + "\\" + "title" + ".xlsx"
        writer = pd.ExcelWriter(path=excel_folder, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False,)
        writer.save()

def create_cases(excel_name,row,excel_folder):
    row = row
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    test_message = row['Test message']
    test_values = row['default tested values']              # values that will be tested
    extra_test_values = row['extra values to test']        # extra values to test
    element_path = row['path']
    Daylight_saving_case = row['Daylight saving case']
    Default_Values = row['base value']
    case = row['Case']
    ExpectedErrorCode = row["ExpectedErrorCode"]
    #if extra values to be tested are empty, then don't add them
    if not pd.isnull(extra_test_values):
        test_values = list(test_values.replace("[","").replace("]","").split(", "))
        extra_test_values = list(extra_test_values.replace("[","").replace("]","").split(", "))
        test_values = ", ".join(test_values + extra_test_values)
        test_values = "[" + test_values + "]"
        
    test_values = test_values.replace("[", "")
    test_values = test_values.replace("]", "")
    test_values = test_values.replace("(", "")
    test_values = test_values.replace(")", "")
    test_values = test_values.replace("'", "")
    test_values = test_values.replace('"', "")
    test_values = test_values.split(", ")


    path = paths.xmls_folder_path +"\\base\\base_" + name + ".json"
    test_cases_folder = copy_base_json_to_folder(path,test_message)
    #list_of_lines_containing_element = find_element_in_xml(element=element,f=f)
    if Default_Values != "mapped" and Default_Values != "not_mapped":
        a_file = open(paths.times_json_path, "r")
        points_Dict = json.load(a_file)
        a_file.close()
        for value in test_values:
            #generates a copy of the base file
            new_case_path = make_test_case(test_cases_folder,test_values.index(value))
            messageID = make_messageID(new_case_path)
            set_element(new_case_path,"MeasurementSeriesNotification/EDSNBusinessDocumentHeader/MessageID",messageID)
            set_element(new_case_path,"MeasurementSeriesNotification/Measurement_Series/mRID",messageID)
            xmlName = test_cases_folder.rsplit("\\",1)[1] + "_" + str(test_values.index(value)) + ".xml"
            set_element(new_case_path,"XMLName",xmlName)   
            test_cases_folder_path = "C:/Users/Ivan/Documents/projects/WPG/nl protocol/xsd converter/" + test_cases_folder.replace("\\","/")
            
            aux_time_case = Daylight_saving_case + "_day"
            set_element(new_case_path,"XMLFolderPath",test_cases_folder_path)
            set_element(new_case_path,"timeSerie",points_Dict[aux_time_case])                
            set_element(new_case_path,"ExpectedErrorCode",ExpectedErrorCode)
            set_time_elements(new_case_path,aux_time_case)
            #modifies the copy
            if str(case) == 'Missing_Element':
                #delete_block(child_of_element_to_be_duplicated_path=element_path,new_case_path=new_case_path)
                set_element(new_case_path,element_path,"")
            else:
                set_element(new_case_path,element_path,value)   
    
    os.remove(test_cases_folder + "\\base.json")
    return test_values,new_case_path


def set_time_elements(new_case_path, aux_time_case):
    
    date_elements_value_list= times[aux_time_case]
    set_element(new_case_path,"MeasurementSeriesNotification/Measurement_Series/DateAndOrTime/startDateTime",date_elements_value_list[0])
    set_element(new_case_path,"MeasurementSeriesNotification/Measurement_Series/DateAndOrTime/endDateTime",date_elements_value_list[1])
    set_element(new_case_path,"MeasurementSeriesNotification/EDSNBusinessDocumentHeader/CreationTimestamp",date_elements_value_list[2])

def copy_base_json_to_folder(path,test_message):
    test_case_path = path.rsplit("\\",1)[1]
    test_case_path = test_case_path.replace("base_", "")
    name = test_case_path.replace(".json", "")

    test_folder = paths.xmls_cases_folder_path + "\\" + name
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    test_message_no_point = test_message.split(".")[0]
    test_folder = test_folder + "\\" + test_message_no_point
    test_folder = test_folder.replace("\n", "")
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

    test_case_path = test_folder + "\\" + "base.json"
    shutil.copyfile(path, test_case_path)
    return test_folder


def make_messageID(new_case_path):
    messageID = new_case_path.rsplit("\\",1)[1].replace(".json","").split("_")
    aux_string = ""
    for words in messageID:
        wordsAUX = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', words)
        if len(wordsAUX) > 0:
            words = wordsAUX
            words = ''.join(words)
            words = ''.join(c for c in words if c.isupper())
        aux_string = aux_string + words
    
    messageID = "IP" + aux_string
    messageID = list(messageID)
    while len(messageID) < 32:
        messageID.append("0")
        
    messageID = add_lowecases_for_MRID(messageID,[8,13,18,23])
    messageID = ''.join(messageID)
    return messageID

def set_element(new_case_path,element_path,value):
    a_file = open(new_case_path, "r")
    json_object = json.load(a_file)
    a_file.close()

    json_object[element_path] = value

    a_file = open(new_case_path, "w")
    json.dump(json_object, a_file, indent=1)
    a_file.close()

    
def make_test_case(test_cases_folder,number):
    name = test_cases_folder.rsplit("\\",1)[1]
    new_case_path = test_cases_folder + "\\" + name + "_" + str(number) + ".json"
    base_case_path = test_cases_folder + "\\base.json"
    shutil.copyfile(base_case_path, new_case_path)
    return new_case_path

    
def add_lowecases_for_MRID(text,list_of_lower_cases_pos):
    for pos in list_of_lower_cases_pos:
        text.insert(pos,"-")
    return text