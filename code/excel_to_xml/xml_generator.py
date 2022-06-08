import copy
from email import message
from lxml import etree
from typing import ContextManager, Optional
import pandas as pd 
import numpy as np
import sys
import os
import json
import copy
import paths
from os import error, listdir
from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'


times = json.load(open(paths.times_json_path))
DS_pints_path = json.load(open(paths.DS_path))
list_of_xml_elements = []

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
    
    if "/" in element:
        element = element.rsplit("/",1)[1]
        
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


def create_xml(has_child_list,rows,col_list,name,default_value_list):
    #gets the rows data and writes it to the xml
    path = paths.xmls_folder_path +"\\base\\base_" + name + ".xml"
    os.remove(path)
    f = open(file=path,mode="a")
    get_xml_row_data(has_child_list=has_child_list, col_list=col_list,rows=rows,previous_col=0,f=f,default_value_list=default_value_list)
    f.close()
    # read the file and remove duplicate lines
    f = open(file=path,mode="r")
    lines =f.read()
    lines = lines.split("\n")
    f.close()
    os.remove(path)
    change_occurred = True
    string_to_remove = []
    while change_occurred:
        change_occurred = False
        for string in string_to_remove:
            lines.remove(string)
        string_to_remove = []
        for row_index in range(0,len(lines)-1):
            current_index = row_index
            next_index = current_index + 1
            string = lines[current_index]
            next_string = lines[next_index].replace("/","")
            # if string is the same as the next string remove both of them
            if string == next_string:
                string_to_remove.append(string)
                string_to_remove.append(lines[next_index])
                change_occurred = True
    lines = [ x for x in lines if "load_from_file" not in x ]
    f = open(file=path,mode="a")
    for line in lines:
        line += "\n"
        f.write(line)
    f.close()

def get_base_Xml(excel_name):
    message_details_folder_path = paths.message_details_folder_path
    folder = listdir(message_details_folder_path)
    name = excel_name.rsplit("_",1)[1]
    name = name.split(".")[0]
    for excel in folder:
        if name in excel:
            path = message_details_folder_path + "\\" + excel
            df = pd.read_excel(path)
            element_path_list = list(df['XML ELEMENT PATH'])
            default_element_values = list(df['DEFAULT VALUES'])
            
            finished_reading_xml_data = False
            for element_path in element_path_list:
                prev_element = ""
                if str(element_path) == "nan":
                    finished_reading_xml_data = True
                if not finished_reading_xml_data:
                    elements = element_path.split("/")
                    for element in elements:
                        if prev_element == "":
                            prev_element = element
                        else:
                            element = prev_element + "/" + element
                            prev_element = element
                        if element not in list_of_xml_elements:
                            list_of_xml_elements.append(element)
                    
            has_child_list = []
            col_list = []
            default_value_list = []
            for element in list_of_xml_elements:
                if element in element_path_list:
                    has_child_list.append(False)
                    element_pos = element_path_list.index(element)
                    default_value_list.append(default_element_values[element_pos])
                else:
                    has_child_list.append(True)
                    default_value_list.append("")
                col_list.append(element.count('/'))
            create_xml(has_child_list=has_child_list, col_list=col_list,rows=list_of_xml_elements,name=name,default_value_list=default_value_list)


def make_base_xmls(message_details_folder_path):
    #get the test cases excel files 
    folder = listdir(message_details_folder_path)
    for excel in folder:
        #make the baseXml file
        get_base_Xml(excel)