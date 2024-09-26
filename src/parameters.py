class Parameters:
    """
    Get parameters from parameters.txt
    """
    def __init__(self, file_path):
        self.type_converter = {
            'int': int, 
            'bool': self.__check_if_parameter_is_bool, 
            'str': str, 
            'float': float,
            'list': self.__convert_to_list  
        }
        self.file_path = file_path

    def get(self):
        self.data_array = []
        with open(self.file_path, "r") as file:
            for line in file.readlines():
                stripped_line = line.strip()
                if stripped_line and stripped_line[0] != "#":
                    start_index = stripped_line.find("=") + 1
                    comment_index = stripped_line.find("#")
                    type_index_start = stripped_line.find("(") + 1
                    type_index_end = stripped_line.find(")")

                    self.data = stripped_line[start_index:comment_index].strip()
                    self.data_type = stripped_line[type_index_start:type_index_end].strip()

                    self.__check_parameter_type_append()
        return self.data_array    

    def __convert_to_list(self, data):
        return [int(element.strip()) for element in data.strip('[]').split(',')]

    def __check_if_parameter_is_bool(self, data):
        if data == 'True':
            return True
        elif data == 'False':
            return False

    def __check_parameter_type_append(self):
        if self.data_type in self.type_converter:
            self.data = self.type_converter[self.data_type](self.data)
            self.data_array.append(self.data)

