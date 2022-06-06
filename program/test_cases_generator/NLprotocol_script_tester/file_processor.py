from cgi import test
import copy
from lxml import etree
from typing import ContextManager, Optional
import pandas as pd 
import numpy as np
import sys
import shutil
import os
import re

from pandas.io.pytables import AppendableFrameTable
sys.path[0] += '\\..'
import paths
from os import error, listdir



sandro_script_path = "gen\\processing_template_scripts\\NLALL2_601_MeasurementSeriesNotification.gen"


def make_process_case(test_cases_folder,xml,xml_folder):
    name = xml.replace("xml", "gen")
    new_case_path = test_cases_folder + "\\" + name
    shutil.copyfile(sandro_script_path, new_case_path)
    fin = open(new_case_path, "rt")
    data = fin.read()
    xml_path = "C:\\Users\\Ivan\\Documents\\projects\\WPG\\nl protocol\\xsd converter\\" + xml_folder + "\\" + xml
    data = data.replace("L:\\QA\\NLALL2\\Inbound\\B020_021.xml",xml_path)
    fin.close()
    fin = open(new_case_path, "wt")
    fin.write(data)
    fin.close()

    

def process_script(test_cases_folder_path):
    #get the test cases excel files 
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        # make the datarame from the test cases excel file
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path)
        for row in df.iterrows():
            row = row[1]
            if not pd.isnull(row['new cases']) and not pd.isnull(row["Element"]) and row["new cases"] != "new cases": 
                xml_folder = row["test folder"] 
                row["new cases"] = "False"
                
                new_path = xml_folder.replace("xml\cases", "gen")
                new_path = new_path.replace("\\", "/")
                test_folder = listdir(xml_folder)
                for xml in test_folder:
                    os.makedirs(new_path, exist_ok=True)
                    make_process_case(new_path,xml,xml_folder)
                    
                    
        # path = paths.xmls_folder_path + "\\" + "title" + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False,)
        writer.save()