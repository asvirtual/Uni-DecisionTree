class Category:
    def __init__(self, name, values=[True, False]):
        self.name = name
        self.values = values


    def get_name(self):
        return self.name
    

    def get_values(self):
        return self.values

    
    def __str__(self):
        return self.name + f": [{', '.join(self.values)}]"
    

    def __eq__(self, other):
        return self.name == other.name and self.values == other.values