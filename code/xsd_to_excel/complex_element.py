import sys
class complex_data():
    
    def __init__(self):
        self.Name = ""
        self.Type = ""
        self.Cardinality = ""
        self.Base_Type = ""
        self.Constraints = []
        self.Enumerations = []
        self.BSDataType = ""
        self.BSDescription = ""
        self.BSFunctionalParameter = ""
        

class Complex_Element_Object():
    _height = 0    

    def get_height(self):
        return type(self)._height

    def set_height(self,val):
        type(self)._height = val

    height = property(get_height, set_height)

    def __init__(self):
        self.complex_data = complex_data()
        self.children = []
        self.parent = ""
        self.level = 1

    def add_children(self, child):
        child.parent = self
        child.level = self.level +1
        if child.level > self.height:
            self.height = child.level
        self.children.append(child)
        

    def print_tree2(self,level):
        spaces = "|  " * level
        prefix = spaces + "|__"
        print(prefix + self.complex_data.Name)
        if self.children:
            for child in self.children:
                child.print_tree2(level+1)
                
    def print_tree(self):
        print("\n\n")
        level = 0
        spaces = "|  " * level
        prefix = spaces + "|__"
        print(prefix + self.complex_data.Name)
        if self.children:
            for child in self.children:
                child.print_tree2(level+1)

    def find_node_in_tree(self,name_of_node_in_search: str):
        
        if self.complex_data.Name == name_of_node_in_search :
            return self
        else:
            name_list = name_of_node_in_search.split("_") 
            #typo in the xsd Measurement_Series should be MeasurementSeries
            #! add an error for new typos to know to add
            listOfTypos = ["Measurement","Series", "Detail","Series",'Acknowledgement','MarketDocument','Volume',"Series",'Reading',"DateAndOrTime","AggregatedAllocation","Series","Allocation","Series"]
            #if the name of the current node is in the name list the desired node is a child of this node 
            # remove the name from the node in the name lists
            if self.complex_data.Name in name_list:
                name_list.remove(self.complex_data.Name)
            #the same thing but taking in to consideration typos
            #Measurement_Series is expected to be MeasurementSeries but the xsd has it separated so i took that in to consideration
            if(len(name_list)>1):
                if((name_list[0] in listOfTypos) and (name_list[1] in listOfTypos)):
                    indices = [i for i, x in enumerate(listOfTypos) if x == name_list[0] ]
                    for index in indices:
                        if name_list[0] == listOfTypos[index] and name_list[1] == listOfTypos[index+1]:
                            aux = name_list[0] + "_" + name_list[1]
                            name_list.remove(name_list[1])
                            name_list.remove(name_list[0])
                            name_list.insert(0,aux)
            if self.complex_data.Name in name_list:
                name_list.remove(self.complex_data.Name)
            
            #make the name for the child node to use
            name_of_node_in_search = "_".join(name_list)
            for child in self.children:
                parent = child.find_node_in_tree(name_of_node_in_search)
                if parent != None:
                    return parent

