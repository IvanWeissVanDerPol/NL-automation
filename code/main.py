import json
from base_xml_to_case_xml.case_xml_generator import generate_xml_cases_from_decompressed_excel
from excel_to_json.verification_json_generator import generate_json
from xml_ts_template_to_json.values_json_generator import values_json_generator
from xsd_to_excel.make_excel_from_xsd import make_excels_from_xsd
from excel_to_xml.xml_generator import make_base_xmls

import paths 

stay_in_program = True
while stay_in_program:
    print("chose what to do:")
    print("[1] make excels from xsd")    #makes an excel tat contains the xsd details here you put the default values and all te test cases (['Correct_Value', 'Invalid_Value', 'Empty_Value', 'Missing_Element']) and the rules for each element
    print("[2] make base xmls")
    print("[3] make xmls and jsons")
    print("[any] exit")
    case = input()
    if case == "1":
        make_excels_from_xsd(folder_Of_xsd=paths.xsd_folder_path) # makes a base excel with the structure of the xsd
    elif case == "2":
        print("are you sure?")
        print("creating new base xml will require you to manually set the namespace of all the base xml")
        print("before creating the test cases xmls")
        print("[1] yes")
        print("[2] no")
        sure = input()
        if sure == "1":
            make_base_xmls(message_details_folder_path=paths.message_details_folder_path)
    elif case == "3":
        values_json_generator(paths.times_txt_paths)
        generate_xml_cases_from_decompressed_excel(message_details_folder_path=paths.message_details_folder_path)
        generate_json(folder_path=paths.message_details_folder_path, struct_excel_path=paths.struct_excel_path)
    else:
        stay_in_program = False

