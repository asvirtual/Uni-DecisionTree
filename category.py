class Category:
    def __init__(self, name, values=[True, False]):
        self.__name = name
        self.__values = values


    def get_name(self):
        return self.__name
    

    def get_values(self):
        return self.__values
    

    def __contains__(self, value):
        return value in self.__values

    
    def __str__(self):
        return self.__name
    

    def __eq__(self, other):
        return self.__name == other.__name and self.__values == other.__values