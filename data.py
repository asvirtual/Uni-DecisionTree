from category import Category
from json import loads


'''
    Represents a single entry in the training data set
    @param attributes: a dictionary containing the attributes of the entry, in the shape of {category: value}, with
        category being the name of the category and value being the value registered the category in the entry
    @param decision: the decision made
'''
class DataEntry:
    def __init__(self, attributes, decision=False):
        # self.__dict__.update({ 
        #     "decision": decision, 
        #     "attributes": attributes
        # })

        self.attributes = attributes
        self.decision = decision


    def get_decision(self):
        return self.decision


    def get(self, category):
        try:
            return self.attributes[category.get_name()]
        except KeyError:
            print(f"[ERROR] Category {category} not found")
            return None
        

    def to_dict(self):
        return self.attributes


    def __str__(self):
        return f"DataEntry: [{', '.join([f'{key}: {value}' for key, value in self.attributes.items()])}, Decision: {self.decision}]"


class Data:
    def __init__(self, categories, outputs):
        if not all([isinstance(category, Category) for category in categories]):
            raise ValueError(f"[ERROR] All categories must be of type Category")
        
        self.categories = categories
        self.outputs = outputs
        self.data = []

    
    '''
        Adds a new entry to the data set
        @param entry: the entry to be added, shape of class DataEntry
    '''
    def append(self, entry, decision):
        if not set(entry.keys()) == set([cat.get_name() for cat in self.categories]):
            raise ValueError(f"[ERROR] Entry categories must match the data categories")

        self.data.append(DataEntry(entry, decision))
    

    def remove(self, entry):
        self.data.remove(entry)


    def get_categories(self):
        return self.categories
    

    def get_data(self):
        return self.data
    

    def get_outputs(self):
        return self.outputs
    

    def get_subset(self, category, value):
        if category not in self.categories:
            raise ValueError(f"[ERROR] Category {category} not found in entry")
        
        if value not in category.get_values():
            raise ValueError(f"[ERROR] Value {value} not valid for category {category}")

        subset = Data(self.categories, self.outputs)
        for entry in self.data:
            if entry.get(category) == value:
                subset.append(entry.to_dict(), entry.get_decision())

        return subset
    

    def get_decisions(self):
        return [entry.get_decision() for entry in self.data]


    def __len__(self):
        return len(self.data)


    def __getitem__(self, index):
        return self.data[index]
    

class Query:
    def __init__(self, categories, attributes=None):
        self.categories = categories
        self.attributes = attributes if attributes is not None else {}


    def get_categories(self):
        return self.categories


    def get(self, category):
        if category not in self.categories:
            raise ValueError(f"[ERROR] Category {category} not found in query")

        return self.attributes[category.get_name()]


    def __str__(self):
        return f"Query: [{', '.join([str(category) for category in self.categories])}]"
    

def load_json(file):
    with open(file, "r") as f:
        json_data = loads(f.read())
        categories = [Category(category["name"], category["values"]) for category in json_data["categories"]]
        outputs = json_data["outputs"]
        data = Data(categories, outputs)
        for entry in json_data["training_data"]:
            data.append(entry["input"], entry["output"])

        query = Query(categories, json_data["query"])        
        return categories, data, query