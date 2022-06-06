import json
import message_details_generator.tree_to_excel as message_details_generator
import test_cases_generator.test_cases as test_cases_generator
import message_details_generator.add_Tests as add_Tests
import message_details_generator.base_xml_generator as base_xml_generator
import message_details_generator.base_json_generator as base_json_generator
import paths as paths
import test_cases_generator.NLprotocol_script_tester.file_processor as file_processor


stay_in_program = True
while stay_in_program:
    print("chose what to do:")
    print("1. make excels from xsd")    #makes an excel tat contains the xsd details here you put the default values and all te test cases (['Correct_Value', 'Invalid_Value', 'Empty_Value', 'Missing_Element']) and the rules for each element
    print("2. make test cases")
    print("3. make base xmls")
    print("4. make xmls")
    print("99. exit")
    case = input()
#    case = ""
    if case == "1":
        message_details_generator.make_excels_from_xsd(folder_Of_xsd=paths.xsd_folder_path) # makes a base excel with the structure of the xsd
        add_Tests.add_paths(message_details_folder_path=paths.message_details_folder_path)  # adds an column that contains the path to the element in the xsd tree
        add_Tests.add_Tests(message_details_folder_path=paths.message_details_folder_path)  # adds an column that contains the tests for each element (the tests are defined in element_tests.py)
    elif case == "2":
        test_cases_generator.make_test_cases(message_details_folder_path=paths.message_details_folder_path) # makes tests case excel tat contains default test values , if you want to add add them in this format ["test1,"test2","test3"] and if an error occurs in excel replace = with = 
        base_xml_generator.update_base_xmls()                                                                
    elif case == "3":
        print("are you sure?")
        print("creating new base xml will require you to manually set the namespace of all the base xml")
        print("before creating the test cases xmls")
        print("1. yes")
        print("2. no")
        sure = input()
        if sure == "1":
            base_xml_generator.make_base_xmls(test_cases_folder_path=paths.test_cases_folder_path)  # makes base xmls but you will need to manually put in a correct namespace from an example xml
            base_json_generator.make_base_jsons(message_details_folder_path=paths.message_details_folder_path)  # makes base json
    elif case == "4":
        base_xml_generator.update_base_xmls()                                                           # updates the base xmls
        base_json_generator.update_base_jsons()
        base_xml_generator.make_test_cases_xmls(test_cases_folder_path=paths.test_cases_folder_path)    # make test cases xmls
        base_json_generator.make_test_cases_jsons(test_cases_folder_path=paths.test_cases_folder_path)
