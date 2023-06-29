# NL-automation
excel (donde estan los excels)

code (donde estan los codigos)

values ( donde estan los valores para los time series)

xml (donde estan los mensajes creados)

xsd (donde se ponen los xsd que van a procesarse para )


#problem
we have to manually test many xml files 
and for each test we have to change values inside the file because of the requierment for each file that is going to be processd to have an unique ID 
manually generating the files for each test takes a lot of time 
manually generating the requiered structures in the software (generate profile for test buyer, seller, etc) takes time 
manually testing all of this takes time 

#solution
have a place where you can configure all the files you want to test
make it easy to generate new files with unique ID 
make it generate all the structure for the software to process the message
test all the messages on its own 
report the test results

how it works
1)the program reads XSD files 
this XSD files contain the structure of XML messages that we want to test and the structure is stored in a EXCEL file
2)in this file we write a DEFAULT case that we then copy its column and modify to create each test case 
we also have another EXCEL that is called EBASE struct in here we can define  the content for each struct we want to generate in the software 
3) we create a base XML (using the default case) 
  3.1in the generated XML we have to edit the namespace manually to the content of a real message (possible automation fix for later but not used enough to require it)
4)we create the xmls and jsons (the jsons are read by the program to create everithing and prepare the test scenario and the xml is the message that is processed in the scenario)


note it doesnt work perfectly some typos in naming structures require manual fixes in the code (add to list of typos, etc) 
but with this we could automatically generate all the messages needed easily for the testing of the software 

ill try to add the code for the software also




