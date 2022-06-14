import pandas as pd
import json
import numpy as np 
import os

def get_json_xmlData(row, values_json_path):
    values_json_file = open(values_json_path, "r")
    values_json_data = json.load(values_json_file)
    values_json_file.close()
    time_series = values_json_data[row['values file']]
    xml_data = {
        "ExpectedErrorCode": row['error code'],
        "messageID": row['Message ID'],
        "XMLName": row['message name'],
        "XMLFolderPath": row['message path'],
        "timeSerie": time_series,
        "startDate": row['startDate'],
        "endDate": row['endDate'],
        "reciver": row['receiver'],
        "gridpoint": row['grid_point'],
        "direction": row['direction']
    }
    return xml_data

def get_sub_df_transposed(df: pd.DataFrame, start_index, end_index):
    sub_df = df.iloc[start_index:end_index]
    sub_df.reset_index(inplace = True, drop = True)
    sub_df = sub_df.T
    sub_df.columns = sub_df.iloc[0]
    sub_df = sub_df[1:]
    return sub_df

def get_sub_df_transposed_struct(df: pd.DataFrame, start_index, end_index):
    sub_df = df.iloc[start_index:end_index]
    sub_df.reset_index(inplace = True, drop = True)
    sub_df = sub_df.T
    sub_df.columns = sub_df.iloc[0]
    sub_df = sub_df[1:]
    sub_df.index = sub_df[sub_df.columns.tolist()[0]]
    return sub_df

def get_sub_df_transposed_reindex(df: pd.DataFrame, start_index, end_index):
    sub_df = get_sub_df_transposed(df, start_index, end_index)
    sub_df.reset_index(inplace = True, drop = True)
    return sub_df

def get_df_from_excel_base(excel_path, sheet_name):
    df = pd.read_excel(excel_path, na_filter = False, sheet_name=sheet_name)
    df_col1_list = df.iloc[:, 0].tolist()
    start_json_info = df_col1_list.index("info para json") + 1
    end_json_info = len(df_col1_list)
    return get_sub_df_transposed(df, start_json_info, end_json_info)

def create_json_array(df):
    name_of_object = df.columns.tolist()[0]
    json_array = []
    for index in df.index.tolist():
        dict_data = {}
        if index == '':
            break
        for key in df.columns.tolist()[1:]:
            
            dict_data[key] = df.loc[index, key]
        json_array.append(dict_data) 
    return json_array   

def get_config_json_from_excel_EBASE_Struct(row, struct_df):
    df_col1_list = struct_df.iloc[:, 0].tolist()
    list_struct = []
    for struct in row.axes[0].tolist():
        if "struct_" in struct:
            struct = struct.replace("struct_", "")
            list_struct.append(struct)
    config_json = {}
    for element in list_struct:
        row_element_array = row["struct_"+element].split(", ")
        element_index = int(df_col1_list.index(element))
        element_end_index = int(df_col1_list[element_index + 1]) + element_index
        element_struct_df = get_sub_df_transposed_struct(struct_df, element_index, element_end_index + 1)
        unwanted_column_list = element_struct_df.columns.tolist()
        unwanted_index_list = element_struct_df.index.tolist()
        unwanted_column_list = [x for x in unwanted_column_list if x.isdigit()]
        unwanted_index_list = [x for x in unwanted_index_list if x not in row_element_array and x != ""]
        #remove the number columns
        for number_col in unwanted_column_list:
            element_struct_df.drop(number_col, axis=1, inplace=True)
        #remove unwanted elements
        for row_element_name in unwanted_index_list:
            element_struct_df.drop(row_element_name, inplace=True)
        #create the dictionary only with the elements that are in the message details excel
        config_json[element] = create_json_array(element_struct_df)
    #TODO: ayuda
    return config_json

def generate_json(folder_path, struct_excel_path):
    """
    Generate the json file for the verification
    folder_path= 'excel/message_details'
    struct_excel_path= 'excel/EBASE Struct.xlsx'
    """
    
    list_excels = [f for f in os.listdir(folder_path) if not f.startswith('~')]
    list_excels = [f for f in list_excels if f.endswith('.xlsx')]
    for excel_file in list_excels:
        message_name = excel_file.rsplit('_',1)[1].split('.')[0]
        excel_path = folder_path + '/' + excel_file
        df_info_json = get_df_from_excel_base(excel_path, 'decompressed cases')
        values_json_path = "values/" + message_name + "/values.json"
        #for para cada columna del json
        struct_df = pd.read_excel(struct_excel_path, na_filter = False)
        for row in df_info_json.iterrows():
            message_name = row[0]
            if message_name != 'DEFAULT VALUES':
                row = row[1]
                json_xml_data = [get_json_xmlData(row, values_json_path)]
                json_config = get_config_json_from_excel_EBASE_Struct(row, struct_df)
                validation_json = {
                    'config': json_config,
                    'xmlData': json_xml_data
                }
                json_path = 'xml/cases/' + message_name + '.json'
                with open(json_path, 'w') as outfile:
                        json.dump(validation_json, outfile, indent=4)