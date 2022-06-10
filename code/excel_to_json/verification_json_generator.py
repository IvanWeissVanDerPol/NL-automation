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
        "reciver": row['reciver'],
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

def get_df_from_excel_base(excel_path):
    df = pd.read_excel(excel_path, na_filter = False)
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

def get_config_json_from_excel_EBASE_Struct(row, excel_path):
    list_struct = [f for f in row.axes[0].tolist() if f.startswith('struct_')]
    df = pd.read_excel(excel_path, na_filter = False)
    #TODO: ayuda
    return config_json

def get_config_json_from_excel_EBASE_Struct1(row, excel_path):
    df = pd.read_excel(excel_path, na_filter = False)
    df_col1_list = df.iloc[:, 0].tolist()
    marketparties_index = 0
    Netareas_index = df_col1_list.index("Netareas")
    Gridpoints_index = df_col1_list.index("Gridpoints")
    supplyContracts_index = df_col1_list.index("supplyContracts")
    connections_index = df_col1_list.index("connections")
    end_index = len(df_col1_list)

    config_json = {}

    marketparties_df = get_sub_df_transposed_struct(df, marketparties_index, Netareas_index)
    config_json['marketparties'] = create_json_array(marketparties_df)
    Netareas_df = get_sub_df_transposed_struct(df, Netareas_index, Gridpoints_index)
    config_json['netareas'] = create_json_array(Netareas_df)
    Gridpoints_df = get_sub_df_transposed_struct(df, Gridpoints_index, supplyContracts_index)
    config_json['gridpoints'] = create_json_array(Gridpoints_df)
    supplyContracts_df = get_sub_df_transposed_struct(df, supplyContracts_index, connections_index)
    config_json['supplyContracts'] = create_json_array(supplyContracts_df)
    connections_df = get_sub_df_transposed_struct(df, connections_index, end_index)
    config_json['connections'] = create_json_array(connections_df)

    return config_json
folder_path = 'excel/message_details'
list_excels = [f for f in os.listdir(folder_path) if not f.startswith('~')]
list_excels = [f for f in list_excels if f.endswith('.xlsx')]
for excel_file in list_excels:
    message_name = excel_file.rsplit('_',1)[1].split('.')[0]
    excel_path = folder_path + '/' + excel_file
    df_info_json = get_df_from_excel_base(excel_path)
    values_json_path = "values/" + message_name + "/values.json"
    #for para cada columna del json
    for row in df_info_json.iterrows():
        message_name = row[0]
        if message_name != 'DEFAULT VALUES':
            row = row[1]
            json_xml_data = [get_json_xmlData(row, values_json_path)]
            json_config = get_config_json_from_excel_EBASE_Struct(row, 'excel/EBASE Struct.xlsx')
            validation_json = {
                'config': json_config,
                'xmlData': json_xml_data
            }
            with open('code/excel_to_json/test.json', 'w') as outfile:
                    json.dump(validation_json, outfile, indent=4)