import json
import pandas as pd 
import sys
sys.path[0] += '\\..'
import paths
from os import listdir
import paths 
import re
import element_tests

json_file_columns = json.load(open(paths.Excel_columns))
json_file_columns["test_cases_excel_columns"]

number_of_titles = 0
def add_title(df ,title):
    global number_of_titles
    number_of_titles += 1
    #row = pd.Series(["#","Element","path","Test message","Status","Error","Observations","optional","BaseType","restricted values","Enumerations","Case","Daylight saving case","base value","default tested values","extra values to test","number of cases","messageID","excel path"])
    #!test
    row = pd.Series(json_file_columns["test_cases_excel_columns"])
    
    
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    row = pd.Series(title)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df

def add_subtitle(df ,subtitle):
    global number_of_titles
    number_of_titles += 1
    row = pd.Series(subtitle)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    #row bellow every subtitle to understand what each column is
    #row = pd.Series(["#","Element","path","Test message","Status","Error","Observations","optional","BaseType","restricted values","Enumerations","Case","Daylight saving case","base value","default tested values","extra values to test","number of cases","messageID"])
    #!test
    row = pd.Series(json_file_columns["test_cases_excel_columns"])
    
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df

def add_test_cases(df ,row,added_subtitles,columns,title,cont,excel_row,element_path):
    list_of_cases = row.tests
    list_of_cases = list_of_cases.replace("[", "")
    list_of_cases = list_of_cases.replace("]", "")
    list_of_cases = list_of_cases.replace('"', "")
    list_of_cases = list_of_cases.replace("'", "")
    list_of_cases = list_of_cases.replace(", ", ",")
    list_of_cases = list_of_cases.split(",")
    
    element_path_list = list(element_path.values())
    element_path_list = list(filter(("").__ne__, element_path_list))
    element_path_string = "/".join(element_path_list)
    element = element_path_list[-1]
    element_path_string_for_json = element_path_string.split("/",1)[1] 
    # add all other info from row
    optional = "false"
    if(row.Cardinality =="0..1"):
        optional = "true"
    status = ""
    error = ""
    observation = ""
    BaseType = row['BaseType']
    Enumerations = row["Enumerations"]
    restricted_values = row.Constraints
    json_element_test = element_tests.tests
    mapped = row["Default Values"]
    #make a test case for each case
    for case in list_of_cases:
        test_values = json_element_test[element_path_string_for_json][case]
        daylight_saving_cases = ["DSNormal","DSLong","DSShort"]
        for daylight_saving_case in daylight_saving_cases:
            if excel_row != 6:
                if added_subtitles:
                    number = '=INDIRECTO(DIRECCION(FILA()-3,COLUMNA()))+1'
                    added_subtitles = False
                else:
                    number = '=INDIRECTO(DIRECCION(FILA()-1,COLUMNA()))+1'
            else:
                number = 0
                added_subtitles = False
            test_message = '=CONCATENAR(INDIRECTO(DIRECCION(3,1)),"_",INDIRECTO(DIRECCION(FILA(),COLUMNA()-2)),"_",INDIRECTO(DIRECCION(FILA(),COLUMNA()+8)),"_",INDIRECTO(DIRECCION(FILA(),COLUMNA()+9)))'
            number_of_cases = "=LARGO(O6)-LARGO(SUSTITUIR(O6,",","")) +1"
            messageID = get_messageID(element_path_string,case,daylight_saving_case)
            new_row = [number,element,element_path_string,test_message,status,error,observation,optional,BaseType,restricted_values,Enumerations,case,daylight_saving_case,mapped,test_values,number_of_cases,"",messageID]
            row_df = pd.DataFrame([new_row])
            df = pd.concat([df,row_df],ignore_index=True)
            cont +=1
            excel_row +=1
    return excel_row,cont,df

def make_test_cases(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    list_of_element_path_string = []
    for excel in folder:
        path = message_details_folder_path + "\\" + excel
        df = pd.read_excel(path)
        
        #remove the columns that are not needed
        df = df[df.columns.difference(['Type'])]
        
        excel_df = pd.DataFrame()
        excel_df = excel_df.assign(new_cases = "")
        columns=list(df.columns.values)
        test_cases_cont = 0
        #read the rows
        element_path = {}
        aux_col = []
        for col in columns:
            if col.startswith('L'):
                aux_col.append(col)
        excel_row = 2
        added_subtitles = False
        for row in df.iterrows():
            row = row[1]
            if not(pd.isnull(row.L1)) or not(pd.isnull(row.L2)):
                if not(pd.isnull(row.L1)):
                    excel_df = add_title(df=excel_df, title=row.L1)
                    title = row.L1
                    element_path["L1"] = row.L1
                    excel_row +=2
                    
                if not(pd.isnull(row.L2)):
                    excel_df = add_subtitle(df=excel_df,subtitle=row.L2)
                    added_subtitles =True
                    element_path["L2"] = row.L2
                    excel_row +=2
                    
            else:
                #make the element path
                for col in aux_col:
                    if not pd.isnull(row[col]):
                        element_path[col] = row[col]
                        index = aux_col.index(col)
                        for pos in range(index+1,len(aux_col)):
                            element_path[aux_col[pos]] = ""
                            
                    
                    if not(pd.isnull(row.tests)) and not(pd.isnull(row[col])): 
                        if row["Default Values"] != 'not_mapped' : 
                            excel_row,test_case_cont ,excel_df = add_test_cases(df=excel_df,added_subtitles=added_subtitles, row=row, columns=columns, title=title, cont=test_cases_cont, excel_row=excel_row,element_path=element_path)
                            added_subtitles = False
            element_path_list = list(element_path.values())
            element_path_list = list(filter(("").__ne__, element_path_list))
            element_path_string = "/".join(element_path_list)
            if  "\\" in element_path_string:
                element_path_string = element_path_string.split("/",1)[1] 
            list_of_element_path_string.append(element_path_string)
        #save the excel
        df["path"] = list_of_element_path_string
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False,columns=["L1","L2","L3","L4","L5","path","Default Values","tests","BS data Type","BS description","BS functional Parameter","BaseType","Cardinality","Constraints","Enumerations"])
        writer.save()
        path = paths.test_cases_folder_path + "\\test_cases_" + title + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        excel_df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()
        
def make_done_test_cases(test_cases_folder_path):
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path,skiprows=1)
        
        #remove the columns that are not needed
        df = df[df.columns.difference(['#'])]
        df = df[df.columns.difference(['path'])]
        df = df[df.columns.difference(['optional'])]
        df = df[df.columns.difference(['BaseType'])]
        df = df[df.columns.difference(['restricted values'])]
        df = df[df.columns.difference(['Enumerations'])]
        df = df[df.columns.difference(['Case'])]
        df = df[df.columns.difference(['Daylight saving case'])]
        df = df[df.columns.difference(['base value'])]
        df = df[df.columns.difference(['extra values to test'])]
        df = df[df.columns.difference(['acknoledgement'])]
        

        #save the excel
        path = paths.done_test_cases_folder_path + "\\" + excel.rsplit("_",1)[1]
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False, columns=['Element','Test message','Error','Observations','Status','default tested values'])
        writer.save()
        
def get_messageID(path,case,Daylight_saving_case):
    xmlElementPath = path.split("/")
    xsd_name = xmlElementPath[0]
    xsd_element_name = xmlElementPath[len(xmlElementPath) - 1 ]
    Daylight_saving_case = Daylight_saving_case.replace("_","")
    case = case.replace("_","")
    string = xsd_name + xsd_element_name +  case + Daylight_saving_case
    aux_string = "IP"
    for words in string:
        wordsAUX = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', words)
        if len(wordsAUX) > 0:
            words = wordsAUX
            words = ''.join(words)
            words = ''.join(c for c in words if c.isupper())
        aux_string = aux_string + words
    aux_string = aux_string + "XX"        
    aux_string = aux_string + "0" * (32 - len(aux_string))
    aux_string = list(aux_string)
    aux_string.insert(8, "-")
    aux_string.insert(13, "-")
    aux_string.insert(18, "-")
    aux_string.insert(23, "-")
    aux_string = ''.join(aux_string)
    messageID =  aux_string
    
    return messageID