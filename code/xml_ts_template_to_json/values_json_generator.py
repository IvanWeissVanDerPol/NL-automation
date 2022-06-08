import re
import os
import json
import paths
def values_json_generator(xml_path):
    """
        generates a json file with the values of the quantities in the xml files that contains the folder that is passed as a parameter
        the json file is generated in the same folder as the xml file with the name values.json
        the json file contains the following structure:
        {
            "xml_file_name":{"quantity_value1","quantity_value2",...},
            "xml_file_name2":{"quantity_value1","quantity_value2",...},
            ...
        }
    """
    #folder where the xml files are
    #xml_path = '../../values/'

    json_data = {}

    #get all the xml files
    for xml in os.listdir(xml_path):
        if xml.endswith(".xml"):
            file_path = xml_path + xml
            #open the xml file
            with open(file_path) as file:
                file_name = os.path.basename(file_path)
                quantity = []
                data = file.readlines()
                #get all the values of the xml file
                for line in data:
                    if re.search(r"<ccma:quantity>.*?</ccma:quantity>", line):
                        quantity.append(re.findall(r'\d+', line)[0])
                #add the values to the json
                json_data[os.path.splitext(file_name)[0]] = ",".join(quantity)

    #write the json file
    with open(paths.times_json_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=4)

if __name__ == "__main__":
    values_json_generator('../../values/')