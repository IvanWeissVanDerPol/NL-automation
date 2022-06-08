import pandas as pd
import json
import numpy as np

df = pd.read_excel('excel/posible nuevo excel base.xlsx')

df_col1_list = df.iloc[:, 0].tolist()
first_nan_index = df_col1_list.index("Info para json")
df.drop(df.loc[0:first_nan_index].index, inplace=True) 
pd.option_context('display.max_rows', None, 'display.max_colwidth', None)
df.reset_index(inplace = True, drop = True)

df = df.T
df.columns = df.iloc[0]
df = df[1:]    

values_json_path = "values/values.json"
values_json_file = open(values_json_path, "r")
values_json_data = json.load(values_json_file)
time_series = values_json_data[df['values file name']['message_1']]
values_json_file.close()

xmlData = [{
    "ExpectedErrorCode": df['message path']['message_1'],
    "messageID": df['messageID']['message_1'],
    "XMLName": "FALTA_NOMBRE",
    "XMLFolderPath": "FALTA_RUTA",
    "timeSerie": time_series,
    "startDate": df['startDate']['message_1'],
    "endDate": df['endDate']['message_1'],
    "reciver": df['reciver']['message_1'],
    "gridpoint": df['gridpoint']['message_1'],
    "direction": "FALTA_DIRECCION",
}]