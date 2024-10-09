from src import np, mpimg, ErrorHandling

# TODO: elastic case
class Image():
    def __init__(self, p) -> None:
        self.Parameters = p
        self.image_file_path = p.image_file_path
        self.format_values = {'.png': 255, '.jpg': 1, '.jpeg': 1}
        self.img = self.load()

        # algorithm_type = 1 (img2model); algorithm_type = 2 (complex); algorithm_type = 3 (parallel)
        if p.algorithm_type == 1:
            self.properties = p.vp_velocity
            self.routine_bool = p.model_extra_routine # temporary
            self.interface_occurence = len(p.vp_velocity)
            self.height, self.width = self.img.shape[:2]
            self.unique_brightness = np.unique(self.img)
            self.frequent_brightness = self.get_predominant_brightness()
            self.respective_value = dict(zip(self.frequent_brightness, self.properties))

        elif p.algorithm_type == 2:
            self.height, self.width = self.img.shape[:2]
            self.inverse_velocity = p.inverse_velocity
            self.min_brightness = np.min(self.img)
            self.max_brightness = np.max(self.img)
            self.v_ratio = (p.vpmax - p.vpmin) / (self.max_brightness - self.min_brightness)
            self.brightness = self.img[:, :]

        elif p.algorithm_type == 3:
            self.properties = p.vp_velocity_parallel
            self.interface_occurence = len(p.vp_velocity_parallel)
            self.height, self.width = p.nz, p.nx
            self.interfaces = p.interfaces
            self.value_interfaces = [
                p.vp_velocity_parallel,
                p.vs_velocity_parallel, 
                p.density_value_parallel
            ]

        if p.model_id == 1:
            self.model = self.img 

            if p.algorithm_type == 1:
                self.set_values()
            elif p.algorithm_type == 2:
                self.pmin, self.pmax = p.vpmin, p.vpmax
                self.set_values_complex()
            elif p.algorithm_type == 3:
                self.parallel_acoustic()

        # TODO: apply logic to elastic models
        elif p.model_id == 2:
            self.model_vp = np.zeros((self.height, self.width))
            self.model_vs = np.zeros((self.height, self.width))
            self.model_rho = np.zeros((self.height, self.width))

        if p.export_model_to_binary_file:
            self.export_model_to_binary(p.binary_model_path)

    # ======================== Load Image =======================
    def load(self) -> np.array:
            try:
                self.img = mpimg.imread(self.image_file_path)
                img_gray = self.rgb2gray()
                return (img_gray * self.image_format_multiplier()).astype(np.uint16)
            except:
                ErrorHandling.verify_image_existence()

    def rgb2gray(self):
        r, g, b = self.img[:, :, 0], self.img[:, :, 1], self.img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

    def image_format_multiplier(self):
        image_format_index = self.image_file_path.find('.')
        image_format = self.image_file_path[image_format_index:]
        try:
            return self.format_values[image_format]
        except:
            ErrorHandling.wrong_image_format()

    # ======================== Predominant Brightness ===========
    def get_predominant_brightness(self):
        brightness, counts = np.unique(self.img, return_counts=True)

        idx_sorted_by_count = np.argsort(-counts)[:self.interface_occurence]
        
        return brightness[idx_sorted_by_count]

    # ========================= Img2Model ========================
    def set_values(self) -> np.array:
        for brightness in self.unique_brightness:
            if brightness not in self.frequent_brightness:
                nearest_index = np.argmin(abs(self.frequent_brightness - brightness.astype(np.uint16)))
                self.model = np.where(self.model == brightness, self.respective_value[self.frequent_brightness[nearest_index]], self.model)
            else:
                self.model = np.where(self.model == brightness, self.respective_value[brightness], self.model)

        if self.routine_bool: 
            self.extra_routine() 

    # =========================== Parallel ==========================
    def parallel_acoustic(self):
        self.__create_model_loop(self.value_interfaces[0])

    def parallel_elastic(self):
        aux_model = []
        for i in range(len(self.value_interfaces)):
            self.__create_model_loop(self.value_interfaces[i])
            aux_model.append(self.model)
        self.model = aux_model

    def __create_model_loop(self, value_interfaces) -> None:
        self.model[:self.interfaces[0], :] = value_interfaces[0]
        for layer, velocity in enumerate(value_interfaces[1:]):
            self.model[self.interfaces[layer]:, :] = velocity

    # =========================== Complex ==========================
    def set_values_complex(self):
        arg = (self.brightness - self.min_brightness) * self.v_ratio
        right_property = self.pmax - arg if self.inverse_velocity else self.pmin + arg
        self.model = right_property 

    # ============================ Extra Routine ====================
    def extra_routine(self):
        for i in range(self.height):
            for j in range(self.width):
                adj_values = self.__get_adjacent(self.model, i, j)
                arr_condition = self.__check_diff_brightness_condition(adj_values)
                if len(arr_condition) > 0:
                    self.model[i][j] = arr_condition[0]
        return self.model

    def __get_adjacent(self, arr: list, i: int, j: int) -> list:
        # I may or may not had a little help on this one
        rows = len(arr)
        cols = len(arr[0])

        v = []
        for k in range(max(0, i-1), min(i+2, rows)):
            for l in range(max(0, j-1), min(j+2, cols)):
                if (k != i or l != j) and arr[k][l] != arr[i][j]:
                    v.append(arr[k][l])
        return v

    def __check_diff_brightness_condition(self, adj_arr: list):
        unique_values, counts = np.unique(adj_arr, return_counts=True)
        arr_brightness_condition = unique_values[counts > 4]
        return arr_brightness_condition if len(arr_brightness_condition) > 0 else []

    # =============================== Export Model ====================
    # Change to Elastic Case
    def export_model_to_binary(self, path) -> None:
        self.model.flatten('F').astype('float32', order='F').tofile(path + f"model_vp_2d_{self.width}x{self.height}.bin")
