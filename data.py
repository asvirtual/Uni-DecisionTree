from category import Category
from json import loads


'''
    Represents a single entry in the training data set
    @param attributes: a dictionary containing the attributes of the entry, in the shape of {category: value}, with
        category being the name of the category and value being the value registered the category in the entry
    @param decision: the registered decision (output) for the entry
'''
class DataEntry:
    def __init__(self, attributes, decision=False):
        self.__attributes = attributes
        self.__decision = decision


    def get_decision(self):
        return self.__decision


    def get(self, category):
        try:
            return self.__attributes[category.get_name()]
        except KeyError:
            print(f"[ERROR] Category {category} not found")
            return None
        

    def to_dict(self):
        return self.__attributes
    

    def __getitem__(self, name):
        return self.get(name)


    def __str__(self):
        return f"DataEntry: [{', '.join([f'{key}: {value}' for key, value in self.__attributes.items()])}, Decision: {self.__decision}]"


'''
    Represents the training data set
    @param categories: a list of categories, in the shape of class Category
    @param outputs: a list of possible outputs
'''
class Data:
    def __init__(self, categories, outputs):
        if not all([isinstance(category, Category) for category in categories]):
            raise ValueError(f"[ERROR] All categories must be of type Category")
        
        if any([output is None for output in outputs]):
            raise ValueError(f"[ERROR] Outputs cannot be None")
        
        self.__categories = categories
        self.__outputs = outputs
        self.__data = []

    
    '''
        Adds a new entry to the data set
        @param entry: the entry to be added, shape of class DataEntry
        @param decision: the registered decision (output) for the entry
    '''
    def append(self, entry, decision):
        if not set(entry.keys()) == set([cat.get_name() for cat in self.__categories]):
            raise ValueError(f"[ERROR] Entry categories must match the data categories")
        
        if decision not in self.__outputs:
            raise ValueError(f"[ERROR] Decision {decision} not valid")

        self.__data.append(DataEntry(entry, decision))
    

    def remove(self, entry):
        self.__data.remove(entry)


    def get_categories(self):
        return self.__categories
    

    def get_data(self):
        return self.__data
    

    def get_outputs(self):
        return self.__outputs
    
    
    '''
        Returns a subset of the data set based on the value of a given category
        @param category: the category to be used to filter the data set
        @param value: the value to be used to filter the data set
    '''
    def get_subset(self, category, value):
        if category not in self.__categories:
            raise ValueError(f"[ERROR] Category {category} not found in entry")
        
        if value not in category:
            raise ValueError(f"[ERROR] Value {value} not valid for category {category}")

        subset = Data(self.__categories, self.__outputs)
        for entry in self.__data:
            if entry[category] == value:
                subset.append(entry.to_dict(), entry.get_decision())

        return subset
    

    '''
        Returns a list of all decisions in the data set
    '''
    def get_decisions(self):
        return [entry.get_decision() for entry in self.__data]


    def __len__(self):
        return len(self.__data)


    def __getitem__(self, index):
        return self.__data[index]
    

'''
    Represents a query to be made to the decision tree
    @param categories: a list of categories, in the shape of class Category
    @param attributes: a dictionary containing the attributes of the query, in the shape of {category: value}, with
        category being the name of the category and value being the value registered the category in the query
'''
class Query:
    def __init__(self, categories, attributes=None):
        self.__categories = categories
        self.__attributes = attributes if attributes is not None else {}


    def get_categories(self):
        return self.__categories


    def get(self, category):
        if category not in self.__categories:
            raise ValueError(f"[ERROR] Category {category} not found in query")

        return self.__attributes[category.get_name()]


    def __getitem__(self, name):
        return self.get(name)


    def __str__(self):
        return f"Query: {'{'} {', '.join([f'{category}: {self[category]}' for category in self.__categories])} {'}'}"
    

def load_json(file):
    try:
        with open(file, "r") as f:
            json_data = loads(f.read())

            categories = [Category(category["name"], category["values"]) for category in json_data["categories"]]
            outputs = json_data["outputs"]

            data = Data(categories, outputs)
            for entry in json_data["training_data"]:
                data.append(entry["input"], entry["output"])

            query = None
            if json_data.get("query"):
                query = Query(categories, json_data["query"])

            return categories, data, query
            
    except KeyError:
        print("[ERROR] Malformatted JSON data")