class Parameters:
    def __init__(self, parameters: list):
        self.model_id = parameters[0]
        self.export_model_to_binary_file = parameters[1]
        self.plot_model_bool = parameters[2]
        self.model_smoothing_bool = parameters[3]
        self.smooth_level = parameters[4]
        self.binary_model_path = parameters[5]
        self.vs_velocity_approximation = parameters[6]
        self.rho_value_approximation = parameters[7]
        self.image_to_model_id = parameters[8]
        self.model_extra_routine = parameters[9]
        self.image_file_path = parameters[10]
        self.vp_velocity = parameters[11]
        self.vs_velocity = [round(i / 1.7, 2) for i in parameters[11]] if parameters[6] else parameters[12]
        self.rho_value = [round((0.31 * i ** 0.25) * 1e3, 2) for i in parameters[11]] if parameters[7] else parameters[13]
        self.complex_model_bool = parameters[14]
        self.inverse_velocity = parameters[15]
        self.vpmin = parameters[16]
        self.vpmax = parameters[17]
        self.vsmin = parameters[18] if not parameters[6] else round(parameters[16] / 1.7, 2)
        self.vsmax = parameters[19] if not parameters[6] else round(parameters[17] / 1.7, 2)
        self.rhomin = parameters[20] if not parameters[7] else round((0.31 * parameters[16] ** 0.25) * 1e3, 2)
        self.rhomax = parameters[21] if not parameters[7] else round((0.31 * parameters[17] ** 0.25) * 1e3, 2)
        self.parallel_plane_model_id = parameters[22]
        self.nx = parameters[23]
        self.nz = parameters[24]
        self.interfaces = parameters[25]
        self.vp_interfaces = parameters[26]
        self.vs_interfaces = parameters[27]
        self.rho_interfaces = parameters[28]
