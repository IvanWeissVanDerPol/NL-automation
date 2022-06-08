import copy
from email import message
from lxml import etree
from typing import ContextManager, Optional
import pandas as pd 
import numpy as np
import sys
import shutil
import os
import json
import re
import copy

from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'
import paths
from os import error, listdir
times = json.load(open(paths.times_json_path))
DS_pints_path = json.load(open(paths.DS_path))

def create_xml(has_child_list,rows,col_list,name,default_value_list):
    #gets the rows data and writes it to the xml
    path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
    f = open(file=path,mode="a")
    get_xml_row_data(has_child_list=has_child_list, col_list=col_list,rows=rows,previous_col=0,f=f,default_value_list=default_value_list)
    f.close()

def get_xml_row_data(has_child_list,rows,col_list,previous_col,f,default_value_list):
    if len(col_list)!=0:
        has_child = has_child_list.pop(0)
        element = rows.pop(0)
        col = col_list.pop(0)
        default_value = default_value_list.pop(0)
        if (default_value != "not_mapped" and default_value != "not_mapped and not used"):
            #f.write("<ccma:"+element+">"+default_value+"</ccma:"+element+">")
            write_xml_Row(has_child_list= has_child_list,has_child=has_child, col=col, col_list=col_list, element=element, previous_col= previous_col, rows=rows,f=f, default_value_list=default_value_list,default_value=default_value)

def write_xml_Row(has_child_list,rows,col_list,previous_col,has_child,element,col,f,default_value, default_value_list):
    tabs = "\t"*col
    prefix = tabs + "<ccma:" + str(element) + ">"
    if(str(default_value) == 'nan'):
        default_value = ""
    
    value = str(default_value)
    sufix = "</ccma:"+ str(element) + ">"
    
    line = prefix
    if len(col_list) >=0:
        if has_child:
            if col == 0:
                line=line.replace(">", "")
                value +=">"
                line+=value
            if len(col_list) >0:
                if col < col_list[0]:
                    value = ""
            line+="\n"
            f.write(line)
            #while has kids
            if len(col_list) >0:
                while col < col_list[0]:
                    get_xml_row_data( has_child_list=has_child_list, col_list=col_list, rows= rows, previous_col=previous_col,f=f,default_value_list= default_value_list)
                    if len(col_list)==0:
                        break
                #
            line=tabs + sufix
            line+="\n"
            f.write(line)
        else:
            line+=value
            line+=sufix
            line+="\n"
            f.write(line)
    else:
        x=1

def get_base_Xml(excel_name):
    message_details_folder_path = paths.message_details_folder_path
    folder = listdir(message_details_folder_path)
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    for excel in folder:
        if name in excel:
            path = message_details_folder_path + "\\" + excel
            df = pd.read_excel(path)
            
            BaseType = df['BaseType']
            default_element_values = df['DEFAULT VALUES']
            #remove the columns that are not needed
            df = df[df.columns.difference(['Type'])]
            df = df[df.columns.difference(['Cardinality'])]
            df = df[df.columns.difference(['Constraints'])]
            df = df[df.columns.difference(['Enumerations'])]
            df = df[df.columns.difference(['tests'])]
            df = df[df.columns.difference(['BaseType'])]
            df = df[df.columns.difference(['DEFAULT VALUES'])]
            df = df[df.columns.difference(['Tests Values'])]
            df = df[df.columns.difference(['BS data Type'])]
            df = df[df.columns.difference(['BS description'])]
            df = df[df.columns.difference(['BS functional Parameter'])]
            df = df[df.columns.difference(['tests'])]
            df = df[df.columns.difference(['path'])]
            

            element_points_in_Excel = list(zip(*np.where(df.notnull())))
            element_list = []
            has_child_list = []
            col_list = []
            default_value_list = []
            for row ,point,type_aux,default_value in zip(df.iterrows(),element_points_in_Excel,BaseType.iteritems(),default_element_values.iteritems()):
                col_list.append(point[1])
                element_list.append(row[1][point[1]])
                default_value_list.append(default_value[1])
                if not pd.isnull(type_aux[1]):
                    has_child_list.append(False)
                else:
                    has_child_list.append(True)
                
            #write the xml file
            create_xml(has_child_list=has_child_list, col_list=col_list,rows=element_list,name=name,default_value_list=default_value_list)
            excel_df = pd.DataFrame()
            columns=list(df.columns.values)

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


    path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
    test_cases_folder = make_test_case_folder(path,test_message)
    #list_of_lines_containing_element = find_element_in_xml(element=element,f=f)
    if Default_Values != "mapped" and Default_Values != "not_mapped":
        for value in test_values:
            #generates a copy of the base file
            new_case_path = make_test_case(test_cases_folder,test_values.index(value))
            messageID = make_messageID(new_case_path)
            set_messageID(new_case_path,messageID)
            set_Measurement_Series_mRID(new_case_path,messageID)
            aux_time_case = Daylight_saving_case + "_day"
            set_time_elements(new_case_path, aux_time_case)
            
            #modifies the copy
            if str(case) == 'Missing_Element':
                delete_block(child_of_element_to_be_duplicated_path=element_path,new_case_path=new_case_path)
            else:
                modify_test_case(new_case_path,element_path,value)
    
    os.remove(test_cases_folder + "\\base.xml")
    return test_values,new_case_path

def set_time_elements(new_case_path, Daylight_saving_case):
    add_points(new_case_path=new_case_path,points_path=DS_pints_path[Daylight_saving_case])    
    modify_DS(new_case_path=new_case_path,date_elements_value_list=times[Daylight_saving_case])


def modify_test_case(new_case_path,element_path,value):
    #get the path for thr element and make it a xml tree path  (add ccma: prefix) to all parts
    #then get the tree and go to the root of the xml tree
    element_path = element_path.split("/") 
    auxList = []
    for element in element_path:
        element = "ccma:" + element
        auxList.append(element)
    auxList.pop(0)
    element_path = "/".join(auxList)
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    node = tree.findall(element_path,tree.nsmap)
    for element in node:
        element.text = str(value)
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)
    
def set_Measurement_Series_mRID(new_case_path,messageID):
    element_path = "ccma:Measurement_Series/ccma:mRID"
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    node = tree.findall(element_path,tree.nsmap)
    if len(node) != 0:
        node[0].text = messageID
        etree.ElementTree(tree).write(new_case_path, pretty_print=True)


def make_messageID(new_case_path):
    messageID = new_case_path.rsplit("\\",1)[1].replace(".xml","").split("_")
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

def set_messageID(new_case_path,messageID):
    element_path = "ccma:EDSNBusinessDocumentHeader/ccma:MessageID"
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    node = tree.findall(element_path,tree.nsmap)
    if len(node) != 0:
        node[0].text = messageID
        etree.ElementTree(tree).write(new_case_path, pretty_print=True)
    
def add_lowecases_for_MRID(text,list_of_lower_cases_pos):
    for pos in list_of_lower_cases_pos:
        text.insert(pos,"-")
    return text
    
def delete_block(new_case_path,child_of_element_to_be_duplicated_path):
    prefix = "ccma:"
    child_of_element_to_be_duplicated_path = child_of_element_to_be_duplicated_path.split("/")
    child_of_element_to_be_duplicated_path.pop(0)
    child_of_element_to_be_duplicated_path[0] = prefix + child_of_element_to_be_duplicated_path[0]
    separator = "/"+prefix
    child_of_element_to_be_duplicated_path = separator.join(child_of_element_to_be_duplicated_path)
    element_to_change  = child_of_element_to_be_duplicated_path.rsplit("/")[1]
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    node = tree.findall(child_of_element_to_be_duplicated_path,tree.nsmap)
    for child in node:
        parent = child.getparent()
        parent.remove(child)
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)

def duplicate_element_box(new_case_path,child_of_element_to_be_duplicated_path):
    child_of_element_to_be_duplicated_path = "ccma:Measurement_Series/ccma:DateAndOrTime/ccma:startDateTime"
    element_to_change  = child_of_element_to_be_duplicated_path.rsplit("/")[1]
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    node = tree.findall(child_of_element_to_be_duplicated_path,tree.nsmap)
    child = node[0]
    parent = child.getparent()
    grandparent = parent.getparent()

    
    new_block = copy.deepcopy(parent)
    new_element = new_block.findall("ccma:startDateTime",tree.nsmap)
    #change the value from the new element
    new_element = new_element[0]
    new_element.text = "new values aaaaaaaaaaaaaaaaaaaaaaaaa"
    
    #add new element to tree
    grandparent.append(new_block)
    #save the new tree
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)
    
def add_points(new_case_path,points_path):
    marker = new_case_path.rsplit("\\",1)[1]
    marker = filter(str.isdigit, marker)
    marker = "".join(marker)
    marker = marker[::-1]
    child_of_element_to_be_duplicated_path = "ccma:Measurement_Series/ccma:Detail_Series/ccma:Point"
    points_tree = etree.parse(points_path) 
    points_tree = points_tree.getroot()
    DetailSeries_list = points_tree.getchildren()
    tree = etree.parse(new_case_path)
    tree = tree.getroot()
    
    node = tree.findall(child_of_element_to_be_duplicated_path,tree.nsmap)
    points = node[0]
    Detail_Series = points.getparent()
    Detail_Series.remove(points)
    measurement_Series = Detail_Series.getparent()
    measurement_Series.append(copy.deepcopy(Detail_Series))
    Detail_Series = measurement_Series.findall("ccma:Detail_Series",tree.nsmap)
    
    
    for x in range(0,2):
        FlowDirection = Detail_Series[x].findall("ccma:FlowDirection/ccma:direction",tree.nsmap)[0]
        FlowDirection.text = "E" + str(17+x)
        add_points_function(DetailSeries_list[x],Detail_Series[x],marker)
    etree.ElementTree(tree).write(new_case_path, pretty_print=True)
    
def add_points_function(DetailSeries_list,Detail_Series,marker):
    for point in DetailSeries_list:
        point[1].text = str( int(float(point[1].text) + float("0.00"+ marker)))
        Detail_Series.append(point)
    
def modify_DS(new_case_path,date_elements_value_list):
    tree = etree.parse(new_case_path)
    root = tree.getroot()
    date_elements_list = ["startDateTime","endDateTime","CreationTimestamp"]
    for element,value in zip(date_elements_list,date_elements_value_list):
        if value != "":
            searched_element = ".//ccma:"+ element    
            elements = root.findall(searched_element,root.nsmap)
            element = elements[0]
            element.text = str(value)
    etree.ElementTree(root).write(new_case_path, pretty_print=True)
    


def make_test_case(test_cases_folder,number):
    name = test_cases_folder.rsplit("\\",1)[1]
    new_case_path = test_cases_folder + "\\" + name + "_" + str(number) + ".xml"
    base_case_path = test_cases_folder + "\\base.xml"
    shutil.copyfile(base_case_path, new_case_path)
    return new_case_path

def find_element_in_xml(element,f):
    list_of_lines_containing_element = []
    for line in f:
        if element in line:
            list_of_lines_containing_element.append(line)
    return list_of_lines_containing_element 

def make_test_case_folder(path,test_message):
    test_case_path = path.rsplit("\\",1)[1]
    test_case_path = test_case_path.replace("base_", "")
    name = test_case_path.replace(".xml", "")

    test_folder = paths.xmls_cases_folder_path + "\\" + name
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
    
    test_message_no_point = test_message.split(".")[0]
    test_folder = test_folder + "\\" + test_message_no_point
    test_folder = test_folder.replace("\n", "")
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)

    test_case_path = test_folder + "\\" + "base.xml"
    shutil.copyfile(path, test_case_path)
    return test_folder

def make_test_cases_xmls(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:

        # make the data frame from the test cases excel file
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path)

        # excel_df = pd.DataFrame()
        # read the rows from the test cases excel file
        # only when elements are not empty a test case will be created based on the test values
        # when elements are empty it means the row is a visual row for people that may contain sub rows
        # example 
        # Element	Test message	Status	Error	Observations	optional	BaseType	restricted values	Enumerations	Case	tested values	Default values
        # AllocationVolumeRevisionRequest												
        # EDSNBusinessDocumentHeader												

        list_of_tests_values = []
        list_of_test_path = []
        for row in df.iterrows():
            row = row[1]
            #print(row.Element)
            if not pd.isnull(row['new cases']) and not pd.isnull(row["Element"]) and row["new cases"] != "new cases": 
                row["new cases"] = 'True'
                tests_values,new_case_path = create_cases(row=row,excel_name=excel,excel_folder=path)
                tests_values = "[" + ",".join(tests_values).lstrip(",") + "]"
                
                new_case_path = new_case_path.rsplit("\\",1)[0]
                list_of_tests_values.append(tests_values)
                list_of_test_path.append("C:\\Users\\Ivan\\Documents\\projects\\WPG\\nl protocol\\xsd converter\\" + new_case_path)
            elif row["#"] == "#":
                list_of_tests_values.append("current tests values")
                list_of_test_path.append("test folder")
            else:
                list_of_tests_values.append("")
                list_of_test_path.append("")
            
        #save the excel
        df["current tests values"] = list_of_tests_values 
        df["test folder"] = list_of_test_path         
        # path = paths.xmls_folder_path + "\\" + "title" + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False,)
        writer.save()

def make_base_xmls(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        #make the baseXml file
        base_Xml = get_base_Xml(excel)
def update_xml(base_xml_excel_path,base_Xml_path):
        df = pd.read_excel(base_xml_excel_path)
        for ind in df.index:
            element_path = df["path"][ind]
            value = df["DEFAULT VALUES"][ind] 
            if value != "not_mapped" and value != "mapped" and not pd.isnull(value):
                modify_test_case(new_case_path = base_Xml_path,element_path = element_path, value = value)
        
def update_base_xmls():
    excel_folder = listdir(paths.message_details_folder_path)
    for excel in excel_folder:
        correspondingXML = "base_" + excel.rsplit("_",2)[1] + ".xml"
        base_Xml_path = paths.xmls_base_folder_path + "\\" + correspondingXML
        excel_path = paths.message_details_folder_path + "\\" + excel
        if os.path.isfile(base_Xml_path):
            update_xml(base_xml_excel_path=excel_path, base_Xml_path=base_Xml_path)





