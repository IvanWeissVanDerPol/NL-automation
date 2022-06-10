import pandas as pd
import json
import numpy as np 

def get_json_xmlData(df):
    values_json_path = "values/values.json"
    values_json_file = open(values_json_path, "r")
    values_json_data = json.load(values_json_file)
    time_series = values_json_data[df['values file name']['message_1']]
    values_json_file.close()
    xml_data = {
        "xmlData": [{
        "ExpectedErrorCode": df['message path']['message_1'],
        "messageID": df['messageID']['message_1'],
        "XMLName": "FALTA_NOMBRE",
        "XMLFolderPath": "FALTA_RUTA",
        "timeSerie": time_series,
        "startDate": df['startDate']['message_1'],
        "endDate": df['endDate']['message_1'],
        "reciver": df['reciver']['message_1'],
        "gridpoint": df['gridpoint']['message_1'],
        "direction": df['direction']['message_1'],
    }]}
    return json.dumps(xml_data)

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
    printCompleteDf(sub_df)
    return sub_df

def get_sub_df_transposed_reindex(df: pd.DataFrame, start_index, end_index):
    sub_df = get_sub_df_transposed(df, start_index, end_index)
    sub_df.reset_index(inplace = True, drop = True)
    return sub_df

def get_df_from_excel_base(excel_path):
    df = pd.read_excel(excel_path)
    df_col1_list = df.iloc[:, 0].tolist()
    start_json_info = df_col1_list.index("Info para json") + 1
    end_json_info = len(df_col1_list)
    return get_sub_df_transposed(df, start_json_info, end_json_info)

def create_json_array(df):
    name_of_object = df.columns.tolist()[0]
    json_array = []
    dict_data = {}
    for index in df.index.tolist():
        if pd.isna(index):
            break
        for key in df.columns.tolist()[1:]:
            aux = df.loc[index, key]
            dict_data[key] = aux
        json_data = json.dumps(dict_data)
        json_array.append(json_data) 
    return json_array   

def printCompleteDf(df: pd.DataFrame):
    print("\n\n\n\nprinting_full_df\n")
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    print(df)

def get_config_json_from_excel_EBASE_Struct(excel_path):
    df = pd.read_excel(excel_path)
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

    return json.dumps(config_json)

df = get_df_from_excel_base('excel/posible nuevo excel base.xlsx')
json_xml_data = get_json_xmlData(df)
json_config = get_config_json_from_excel_EBASE_Struct('excel/EBASE Struct.xlsx')
validation_json = {
    json_config,
    json_xml_data
}
print(validation_json)

# with open('code/excel_to_json/test.json', 'w') as outfile:
#         json.dump(xml_data, outfile, indent=4)