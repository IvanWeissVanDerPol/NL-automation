import sys
import json
from logging import root
from os import name
import xmlschema
from pprint import pprint

from xsd_to_excel.Simple_Element import Simple_Element_Object
from xsd_to_excel.complex_element import Complex_Element_Object


def get_tree(xsd_path ):
    xsd = xmlschema.XMLSchema(xsd_path)
    dict = xsd.to_dict(xsd_path)
    
    simple_Element_List = []
    #make a list of all simpleType elements in the xsd file 
    for simpleType in dict["xsd:simpleType"]:
        aux_SEO = Simple_Element_Object()
        aux_SEO.Name = simpleType["@name"] 
        #get the list of restrictions 
        for Constraints in simpleType["xsd:restriction"]:
            #base
            if Constraints == "@base":
                aux_SEO.Type = simpleType["xsd:restriction"][Constraints]
            #valid values for the elements
            elif Constraints == 'xsd:enumeration':
                if len(simpleType["xsd:restriction"][Constraints]) == 1:
                    possible_value = str(simpleType["xsd:restriction"][Constraints]["@value"])
                    aux_SEO.possible_allowed_value.append(possible_value)
                else:
                    for possible_allowed_value in simpleType["xsd:restriction"][Constraints]:
                        possible_value += str(possible_allowed_value["@value"])
                        aux_SEO.possible_allowed_value.append(possible_value)
            #anything else
            else:
                Constraints_aux = Constraints.replace("xsd:" ,"")
                Constraints_aux += " = "
                Constraints_aux += str(simpleType["xsd:restriction"][Constraints]["@value"])
                aux_SEO.restriction.append(Constraints_aux)    
        simple_Element_List.append(aux_SEO)

    #make the complex type tree from the xsd
    base_type = ""
    restrictions =[]
    possible_allowed_value_list = [] 
    child_name_in_bfs = []
    complexType = dict["xsd:complexType"]
    first_time = True
    root = None
    #make a tree of the complexType elements
    #create a node load all the elements (values and children nodes get the values loaded not the grand children)
    for aux_CEO in complexType:
        node = Complex_Element_Object()
        node = load_node(root,aux_CEO,node,simple_Element_List)
        if first_time :
            first_time = False
            root = node
        #root.print_tree()
    return root
        

def find_type(simple_Element_List,node_type):
    for element in simple_Element_List:
            if node_type == element.Name:
                return element
    return None

#loads all values except children and parent
def load_node(root:Complex_Element_Object,aux_CEO,node:Complex_Element_Object,simple_Element_List):
        #get the values from the xsd
        Name = aux_CEO["@name"] 
        base_type = ""
        restrictions = ""
        Type = ""
        possible_allowed_value_list = ""
        if aux_CEO.get("xsd:sequence")!= None:
            Cardinality = str(aux_CEO["xsd:sequence"]["@minOccurs"]) + ".." + str(aux_CEO["xsd:sequence"]["@maxOccurs"])
        else:
            Cardinality = str(aux_CEO["@minOccurs"]) + ".." + str(aux_CEO["@maxOccurs"])
        if aux_CEO.get("@type"):
            Type = aux_CEO["@type"].split(":")[1]
            base_simple_element = find_type(simple_Element_List=simple_Element_List, node_type=Type)
            if base_simple_element:
                base_type = base_simple_element.Type.rsplit(":")[1]
                restrictions = base_simple_element.restriction
                possible_allowed_value_list = base_simple_element.possible_allowed_value

        # save the values in the node
        node.complex_data.Name = Name
        node.complex_data.Type = Type
        node.complex_data.Cardinality = Cardinality
        node.complex_data.Base_Type = base_type
        node.complex_data.Constraints = restrictions
        node.complex_data.Enumerations = possible_allowed_value_list

        if aux_CEO.get("xsd:sequence") != None:
            if aux_CEO.get("xsd:sequence").get("xsd:element")!= None:
                node_in_tree = node
                if root != None:
                    node_in_tree = root.find_node_in_tree(Name)
                    #if the node does not exist in the tree 
                    #an error happend and the code needs to be adjusted
                    if node_in_tree  == None:
                        print("stop")
                        sys.exit("node not found in tree, posibbly a typo check if a node has a name like AggregatedAllocation_Series and add AggregatedAllocation Series to the list of typos ")
                                # i wrote the code to see each _ as a node of the xml so if a node has a _ in the name you add it to typos list and it fixes it 
                load_children(root,node_in_tree,aux_CEO["xsd:sequence"]["xsd:element"],simple_Element_List)
        return node

def load_children(root,parent:Complex_Element_Object,aux_CEO,simple_Element_List):
    if type(aux_CEO) is list:
        for child in aux_CEO:
            child_node = Complex_Element_Object()
            child_node = load_node(root,child,child_node,simple_Element_List)
            parent.add_children(child_node)
    else:
        child_node = Complex_Element_Object()
        child_node = load_node(root,aux_CEO,child_node,simple_Element_List)
        parent.add_children(child_node)


