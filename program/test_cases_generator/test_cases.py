from email import header
from importlib.resources import path
import pandas as pd 
import sys
sys.path[0] += '\\..'
import paths
from os import listdir 
from os import path
import paths 
import re
import json
import element_tests
import pathlib


number_of_titles = 0
#test_cases_column_names = ["#","Element","path","Test message","Status","Error","Observations","optional","BaseType","restricted values","Enumerations","Case","Daylight saving case","base value","default tested values","extra values to test","number of cases","messageID","excel path","new cases"]
json_file_columns = json.load(open(paths.Excel_columns))
test_cases_column_names  = json_file_columns["test_cases_excel_columns"]
def add_title(df ,title):
    global number_of_titles
    number_of_titles += 1
    row = pd.Series()
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    row = pd.Series(test_cases_column_names)
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
    row = pd.Series(test_cases_column_names)
    row_df = pd.DataFrame([row])
    df = pd.concat([df,row_df],ignore_index=True)
    return df

def add_test_cases(df ,row,added_subtitles,columns,title,cont,excel_row,element_path,number):
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
    restricted_values = row["Constraints"]
    json_element_test = element_tests.tests
    mapped = row["DEFAULT VALUES"]
    #make a test case for each case
    for case in list_of_cases:
        test_values = json_element_test[element_path_string_for_json][case]
        daylight_saving_cases = ["DSNormal","DSLong","DSShort"]
        
        for daylight_saving_case in daylight_saving_cases:
            excel_row = df.shape[0]
            if excel_row != 4:
                if added_subtitles:
                    number = '=INDIRECTO(DIRECCION(FILA()-3,COLUMNA()))+1'
                    added_subtitles = False
                else:
                    number = '=INDIRECTO(DIRECCION(FILA()-1,COLUMNA()))+1'
            else:
                number = 0
                added_subtitles = False
            #number = number + 1
            test_message = element_path_string.split("/")[0] + "_" + element_path_string.split("/")[len(element_path_string.split("/"))-1] + "_" + case + "_" + daylight_saving_case
            number_of_cases = "=(LARGO(H{})-LARGO(SUSTITUIR(H{},\"'\",\"\")) + LARGO(I{})-LARGO(SUSTITUIR(I{},\"'\",\"\")))/2".format(excel_row,excel_row,excel_row,excel_row)
            messageID = get_messageID(element_path_string,case,daylight_saving_case)
            new_cases = "True"
            current_tests_values = "this is filed in after when the xml is created a user might add values to extra values column"
            test_folder = str(pathlib.Path().resolve()) + paths.xmls_cases_folder_path + "\\" + element_path_string.split("/")[0]+ "\\" + test_message
                        
            if case == "Correct_Value":
                ExpectedErrorCode = "0"    
            else:
                ExpectedErrorCode = "FILL_IN_ERROR_CODE"
            
            new_row = [number,element,element_path_string,test_message,status,error,observation,optional,BaseType,restricted_values,Enumerations,case,daylight_saving_case,mapped,test_values,"",number_of_cases,messageID,new_cases,current_tests_values,test_folder,ExpectedErrorCode]
            row_df = pd.DataFrame([new_row])
            df = pd.concat([df,row_df],ignore_index=True)
            cont +=1
    return excel_row,cont,df,number

def make_test_cases(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    list_of_element_path_string = []
    for excel in folder:
        path = message_details_folder_path + "\\" + excel
        message_details_excel_df = pd.read_excel(path)
        
        #remove the columns that are not needed
        message_details_excel_df = message_details_excel_df[message_details_excel_df.columns.difference(['Type'])]
        
        test_cases_excel_df = pd.DataFrame()
        columns=list(message_details_excel_df.columns.values)
        test_cases_cont = 0
        #read the rows
        element_path = {}
        aux_col = []
        #get all the L(number)columns and make a list of all of them
        for col in columns:     
            if col.startswith('L'):
                aux_col.append(col)
        excel_row = 2
        added_subtitles = False
        number = 0
        for row in message_details_excel_df.iterrows():
            row = row[1]
            #(L1 is the title and L2 is the subtitle) L1 contains the xml type and L2 contains the main blocks of the xsd
            if not(pd.isnull(row.L1)) or not(pd.isnull(row.L2)):
                if not(pd.isnull(row.L1)):
                    test_cases_excel_df = add_title(df=test_cases_excel_df, title=row.L1)
                    title = row.L1
                    element_path["L1"] = row.L1
                    excel_row +=1
                    
                if not(pd.isnull(row.L2)):
                    test_cases_excel_df = add_subtitle(df=test_cases_excel_df,subtitle=row.L2)
                    added_subtitles =True
                    element_path["L2"] = row.L2
                    excel_row +=1
                    
            else:
                #if the row is not a title or subtitle
                #update the element path from the prev use 
                for col in aux_col:
                    if not pd.isnull(row[col]):
                        element_path[col] = row[col]
                        index = aux_col.index(col)
                        for pos in range(index+1,len(aux_col)):
                            element_path[aux_col[pos]] = ""
                            
                    #if the test case is defined for the row (the tests cases are previously defined )
                        if not(pd.isnull(row.tests)): 
                            # some elements are not mapped yet so we need to check if the element is mapped
                            if row["DEFAULT VALUES"] != 'not_mapped' : 
                                excel_row,test_case_cont ,test_cases_excel_df,number = add_test_cases(df=test_cases_excel_df,added_subtitles=added_subtitles, row=row, columns=columns, title=title, cont=test_cases_cont, excel_row=excel_row,element_path=element_path,number=number)
                                added_subtitles = False
            element_path_list = list(element_path.values())
            element_path_list = list(filter(("").__ne__, element_path_list))
            element_path_string = "/".join(element_path_list)
            if  "\\" in element_path_string:
                element_path_string = element_path_string.split("/",1)[1] 
            list_of_element_path_string.append(element_path_string)
        
        #set first row as header (allows using column names to refer to the columns)
        new_header = test_cases_excel_df.iloc[1] #grab the first row for the header
        test_cases_excel_df = test_cases_excel_df[1:] #take the data less the header row
        test_cases_excel_df.columns = new_header #set the header row as the df header
        #remove the first row (some how the first row is a blank row and this is an ez work around)
        #test_cases_excel_df.drop(message_details_excel_df.index[0], inplace=True)
        #! this line removes info I ivan consider annoying and useless 
        # drop the columns Status	Error	Observations	optional	BaseType	restricted values	Enumerations Case
        test_cases_excel_df.drop(["Status","Error","Observations","optional","BaseType","restricted values","Enumerations"], axis=1, inplace=True)
        # re order the columns
        
        message_details_excel_df["path"] = list_of_element_path_string
        #save the excel
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        message_details_excel_df.to_excel(writer,header=True, sheet_name='Sheet1',index=False,columns=["L1","L2","L3","L4","L5","path","DEFAULT VALUES","tests","BS data Type","BS description","BS functional Parameter","BaseType","Cardinality","Constraints","Enumerations"])
        writer.save()
        path = paths.test_cases_folder_path + "\\test_cases_" + title + ".xlsx"
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        test_cases_excel_df.to_excel(writer,header=False, sheet_name='Sheet1',index=False, columns=["#", "path", "Test message", "Element", "Daylight saving case", "base value", "Case", "default tested values", "extra values to test", "number of cases", "messageID", "new cases", "current tests values", "test folder", "ExpectedErrorCode"])
        writer.save()
        
def make_done_test_cases(test_cases_folder_path):
    folder = listdir(test_cases_folder_path)
    for excel in folder:
        path = test_cases_folder_path + "\\" + excel
        df = pd.read_excel(path)
        df['tested values'] = ""
        for row in df.iterrows():
            row = row[1]
            test_values = row['default tested values']             
            extra_test_values = row['extra values to test']        
            if not pd.isnull(extra_test_values):
                test_values = list(test_values.replace("[","").replace("]","").split(", "))
                extra_test_values = list(extra_test_values.replace("[","").replace("]","").split(", "))
                test_values = ", ".join(test_values + extra_test_values)
                test_values = "[" + test_values + "]"
                row['tested values'] = test_values 
            
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
        df.to_excel(writer, sheet_name='Sheet1',index=False, columns=['Element','Test message','Error','Observations','tested values'])
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

def make_excel_that_shows_error_codes(message_details_folder_path):
    folder = listdir(message_details_folder_path)
    for excel in folder:
        path = message_details_folder_path + "\\" + excel
        message_details_excel_df = pd.read_excel(path)
        message_details_excel_df.dropna(subset=['tests'],inplace=True)
        selenium_excel_df = pd.DataFrame({"Excel path", "returned error code",	"expected error code",	"returned message"})
        prev_value_list = []
        for ms_row in message_details_excel_df.iterrows():
            selenium_excel_df[ms_row[1]["path"].split("/",1)[1]] = ""
            prev_value_list.append(0)
        tests = element_tests.tests
        
        # dic =  {}
        # for element in tests:
        #     for case in tests[element]:
        #         lower_case_regex = "[a-z]"
        #         short_case =  (re.sub(lower_case_regex, "", case))
        #         for value in tests[element][case]:
        #             new_value = short_case + "/" + value
        #             if element not in dic:
        #                 dic[element] = []    
        #             dic[element].append(new_value)
        # json_dic = json.dumps(dic)
        # f = open("dict.json","w")
        # f.write(json_dic)
        # f.close()
        
        # finished = False
        # next_column = 5
        # while not finished:
        #     element_path = (selenium_excel_df.iloc[:, next_column].name).lsplit("/",1)[1]
            
        list_of_columns = list(selenium_excel_df.columns)[1:]
        prev_dataframe = pd.DataFrame()
        for current_column in list_of_columns:
            aux_repeted_list = []
            aux_dataframe = pd.DataFrame()
            if prev_dataframe.empty:
                current_dataframe = pd.DataFrame(tests[current_column]["Correct_Value"] , columns=[current_column]  )
            else:
                for element in tests[current_column]["Correct_Value"]:
                    for x in range(0,len(prev_dataframe)):
                        aux_repeted_list.append(element)
                current_dataframe = pd.DataFrame(aux_repeted_list, columns=[current_column]  )
            current_number_of_elements = len(list(tests[current_column]["Correct_Value"]))
            prev_dataframe = pd.concat([prev_dataframe]*current_number_of_elements, ignore_index=True)
            current_dataframe = pd.concat([prev_dataframe,current_dataframe], axis=1)
            prev_dataframe = current_dataframe.copy()
            prev_column = current_column
        #save the excel
        path = paths.done_test_cases_folder_path + "\\" + excel.rsplit("_",1)[1]
        writer = pd.ExcelWriter(path=path, engine='xlsxwriter')
        current_dataframe.to_excel(writer, sheet_name='Sheet1',index=False, columns=['Element','Test message','Error','Observations','tested values'])
        writer.save()
        #message_details_excel_df['element'] = message_details_excel_df.apply(lambda row: row.path.rsplit("/",1)[1],axis = 1)
        
                
        # for col in aux_col:
        #     if not pd.isnull(row[col]):
        #         element_path[col] = row[col]
        #         index = aux_col.index(col)
        #         for pos in range(index+1,len(aux_col)):
        #             element_path[aux_col[pos]] = ""
