import pandas as pd 
import sys
import sys, os
sys.path.insert(0, os.path.abspath('..'))
import paths
from os import listdir



def make__done_test_cases(test_cases_folder_path):
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path,skiprows=1)

        #remove the columns that are not needed
        
        tested_values = [] 
        list1 =  df['extra values to test'].tolist()
        list2 =  df['default tested values'].tolist()
        row = 2
        for element1 ,element2 in zip(list1,list2):
            value = ""
            if not element2 == 'default tested values':
                if str(element1) != 'nan':
                    value = str(element1)
                if str(element2) != 'nan':
                    if str(element1) != 'nan':
                        value += ","
                    value += str(element2)
            else:
                value = str(element2)
            tested_values.append(value)

        df = df[df.columns.difference(['default tested values'])]
        df = df[df.columns.difference(['path'])]
        df = df[df.columns.difference(['optional'])]
        df = df[df.columns.difference(['BaseType'])]
        df = df[df.columns.difference(['restricted values'])]
        df = df[df.columns.difference(['Enumerations'])]
        df = df[df.columns.difference(['extra values to test'])]
        df['default tested values'] = tested_values
        df = df.reindex(columns=["#","Test message","Element","Case","default tested values","Error","Observations","Status"])

        #save the excel
        path = paths.done_test_cases_folder_path + "\\" + excel
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()

make__done_test_cases(paths.test_cases_folder_path)