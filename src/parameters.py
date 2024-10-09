import re

class Parameters:
    """
    Get parameters from data_array.txt
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

        self.type_converter = {
            'int': int,
            'bool': self.__check_if_parameter_is_bool,
            'str': str,
            'float': float,
            'list': self.__convert_to_list
        }

        self.get()

        self.print_parameters = self.data.get('Print_Parameters')
        self.algorithm_type = self.data.get('Algorithm')
        self.model_id = self.data.get('Model_ID')
        self.export_model_to_binary_file = self.data.get('Export_Model_to_Binary_File')
        self.plot_model_bool = self.data.get('Plot_Model')
        self.model_smoothing_bool = self.data.get('Model_Smoothing')
        self.smooth_level = self.data.get('Smooth_Level')
        self.binary_model_path = self.data.get('Binary_Model_Path')
        self.vs_velocity_approximation = self.data.get('VS_Velocity')
        self.rho_value_approximation = self.data.get('Density_Value')
        self.image_to_model_id = self.data.get('Image_To_Model_ID')
        self.model_extra_routine = self.data.get('Model_Extra Routine')
        self.image_file_path = self.data.get('Image_File_Path')
        self.vp_velocity = self.data.get('VP_Velocity')
        self.vs_velocity = (
            [round(i / 1.7, 2) for i in self.data.get('VS_Velocity')] 
            if self.data.get('VS_Velocity') else self.data.get('Density_Value')
        )
        self.rho_value = (
            [round((0.31 * i ** 0.25) * 1e3, 2) for i in self.data.get('VP_Velocity')] 
            if self.data.get('Density_Value') else self.data.get('Density_Value')
        )
        self.complex_model_bool = self.data.get('Complex_Model_ID')
        self.inverse_velocity = self.data.get('Inverse_Velocity')
        self.vpmin = self.data.get('Minimum_VP_Velocity')
        self.vpmax = self.data.get('Maximum_VP_Velocity')
        self.vsmin = (
            self.data.get('Minimum_VS_Velocity') 
            if not self.data.get('VS_Velocity') else round(self.data.get('Minimum_VP_Velocity') / 1.7, 2)
        )
        self.vsmax = (
            self.data.get('Maximum_VS_Velocity') 
            if not self.data.get('VS_Velocity') else round(self.data.get('Maximum_VP_Velocity') / 1.7, 2)
        )
        self.rhomin = (
            self.data.get('Minimum_Density') 
            if not self.data.get('Density_Value') else round((0.31 * self.data.get('Minimum_VP_Velocity') ** 0.25) * 1e3, 2)
        )
        self.rhomax = (
            self.data.get('Maximum_Density') 
            if not self.data.get('Density_Value') else round((0.31 * self.data.get('Maximum_VP_Velocity') ** 0.25) * 1e3, 2)
        )
        self.parallel_plane_model_id = self.data.get('Parallel_Plane_Model_ID')
        self.nx = self.data.get('Nx')
        self.nz = self.data.get('Nz')
        self.interfaces = self.data.get('Interfaces')
        self.vp_velocity_parallel = self.data.get('VP_Velocity_Parallel')
        self.vs_velocity_parallel = (
            [round(i / 1.7, 2) for i in self.data.get('VS_Velocity')] 
            if self.data.get('VS_Velocity') else self.data.get('Density_Value')

        )
        self.density_value_parallel = (
            [round((0.31 * i ** 0.25) * 1e3, 2) for i in self.data.get('VP_Velocity')] 
            if self.data.get('Density_Value') else self.data.get('Density_Value')
        )

    def get(self):
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    for line in file.readlines():
                        key_value_m = re.search(r"(\w+)\s*=\s*(.+?)(\s*#|\s*$)", line)

                        type_m = re.search(r"\((.*?)\)", line)
                        try:
                            if key_value_m and type_m and type_m.group(1) in self.type_converter:
                                key = key_value_m.group(1)
                                value = key_value_m.group(2).strip()

                                self.data[key] = self.type_converter[type_m.group(1)](value)
                        except:
                            raise ValueError(f"Check the syntax of line: \n{line}") 
            except:
                raise IOError("Could not find parameters file.")

    def __convert_to_list(self, data):
        return [int(element.strip()) for element in data.strip('[]').split(',') if element]

    def __check_if_parameter_is_bool(self, data):
        if data.upper() == 'TRUE':
            return True
        elif data.upper() == 'FALSE':
            return False
