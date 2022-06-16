import re
import os
import json
#import paths

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



    #get all the xml files
    xml_path = xml_path + '/'
    for folder in os.listdir(xml_path):
        json_data = {}
        if os.path.isdir(xml_path + folder):
            json_path = xml_path + folder + '/' + 'values.json'
            folder_path = xml_path + folder + '/'
            for xml in os.listdir(folder_path):
                if xml.endswith(".xml"):
                    file_path = folder_path + xml
                    #open the xml file
                    with open(file_path) as file:
                        file_name = os.path.basename(file_path)
                        quantity = []
                        direction = []
                        data = file.readlines()
                        #TODO chose the block of detail series in reference of the direction
                        #get all the values of the xml file in the first block of detail series
                        first_block = True
                        for line in data:
                            if re.search(r"</ccma:Detail_Series>", line):
                                first_block = False
                            if re.search(r"<ccma:direction>.*?</ccma:direction>", line):
                                direction.append(re.search(r"<ccma:direction>(.*?)</ccma:direction>", line).group(1))
                            if re.search(r"<ccma:quantity>.*?</ccma:quantity>", line) and first_block:
                                quantity.append(re.findall(r'\d+', line)[0])
                        #add the values to the json
                        values_xml_name = os.path.splitext(file_name)[0]
                        json_data[values_xml_name] = ",".join(quantity)
                        json_data[values_xml_name + '_direction'] = ",".join(direction)

            #write the json file
            #json_path = xml_path + 'values.json'
            with open(json_path, 'w') as outfile:
                json.dump(json_data, outfile, indent=4)

if __name__ == "__main__":
    values_json_generator('C:/Users/coraj/Documents/Internet Explorer/Universidad/work/NL-automation/values/')