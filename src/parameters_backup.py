class Parameters:
    """
    Get data_array from data_array.txt
    """
    def __init__(self, file_path):
        self.file_path = file_path

        self.type_converter = {
            'int': int, 
            'bool': self.__check_if_parameter_is_bool, 
            'str': str, 
            'float': float,
            'list': self.__convert_to_list  
        }

        self.get()

        self.model_id = self.data_array[0]
        self.export_model_to_binary_file = self.data_array[1]
        self.plot_model_bool = self.data_array[2]
        self.model_smoothing_bool = self.data_array[3]
        self.smooth_level = self.data_array[4]
        self.binary_model_path = self.data_array[5]
        self.vs_velocity_approximation = self.data_array[6]
        self.rho_value_approximation = self.data_array[7]
        self.image_to_model_id = self.data_array[8]
        self.model_extra_routine = self.data_array[9]
        self.image_file_path = self.data_array[10]
        self.vp_velocity = self.data_array[11]
        self.vs_velocity = [round(i / 1.7, 2) for i in self.data_array[11]] if self.data_array[6] else self.data_array[12]
        self.rho_value = [round((0.31 * i ** 0.25) * 1e3, 2) for i in self.data_array[11]] if self.data_array[7] else self.data_array[13]
        self.complex_model_bool = self.data_array[14]
        self.inverse_velocity = self.data_array[15]
        self.vpmin = self.data_array[16]
        self.vpmax = self.data_array[17]
        self.vsmin = self.data_array[18] if not self.data_array[6] else round(self.data_array[16] / 1.7, 2)
        self.vsmax = self.data_array[19] if not self.data_array[6] else round(self.data_array[17] / 1.7, 2)
        self.rhomin = self.data_array[20] if not self.data_array[7] else round((0.31 * self.data_array[16] ** 0.25) * 1e3, 2)
        self.rhomax = self.data_array[21] if not self.data_array[7] else round((0.31 * self.data_array[17] ** 0.25) * 1e3, 2)
        self.parallel_plane_model_id = self.data_array[22]
        self.nx = self.data_array[23]
        self.nz = self.data_array[24]
        self.interfaces = self.data_array[25]
        self.vp_interfaces = self.data_array[26]
        self.vs_interfaces = self.data_array[27]
        self.rho_interfaces = self.data_array[28]

    # refator get()
    # manejar espaços vazios e utilizar o collection lib
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

    def __convert_to_list(self, data):
        return [int(element.strip()) for element in data.strip('[]').split(',')]

    def __check_if_parameter_is_bool(self, data):
        if data.upper() == 'TRUE':
            return True
        elif data.upper() == 'FALSE':
            return False

    def __check_parameter_type_append(self):
        if self.data_type in self.type_converter:
            self.data = self.type_converter[self.data_type](self.data)
            self.data_array.append(self.data)

