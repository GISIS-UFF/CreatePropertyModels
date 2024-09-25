class GetParameters:
    """
    Get parameters from parameters.txt
    """
    def __init__(self, file_path):
        self.type_converter = {'int': int, 'bool': self.__check_if_parameter_is_bool, 'str': str, 'float': float}
        self.file_path = file_path

    def get_parameter(self):
        self.parameters_array = []
        with open(self.file_path, "r") as file:
            for line in file.readlines():
                stripped_line = line.strip()
                if stripped_line and stripped_line[0] != "#":
                    start_index = stripped_line.find("=") + 1
                    comment_index = stripped_line.find("#")
                    type_index_start = stripped_line.find("(") + 1
                    type_index_end = stripped_line.find(")")

                    self.parameter = stripped_line[start_index:comment_index].strip()
                    self.parameter_type = stripped_line[type_index_start:type_index_end].strip()

                    self.__check_if_parameter_is_list()
                    self.__check_parameter_type_append()
        return self.parameters_array    

    def __check_if_parameter_is_list(self):
         if self.parameter_type == 'list':
            self.parameter = self.parameter.strip('[]').split(',')
            converted_list = [int(element.strip()) for element in self.parameter]
            self.parameters_array.append(converted_list)

    def __check_if_parameter_is_bool(self, parameter):
        if parameter == 'True':
            return True
        elif parameter == 'False':
            return False

    def __check_parameter_type_append(self):
        if self.parameter_type in self.type_converter:
            self.parameter = self.type_converter[self.parameter_type](self.parameter)
            self.parameters_array.append(self.parameter) 
