from src import np, plt, mpimg, ErrorHandling
from scipy.ndimage import gaussian_filter

class Image():
    def __init__(self, p) -> None:
        self.Parameters = p
        self.image_file_path = p.image_file_path
        self.format_values = {'.png': 255, '.jpg': 1, '.jpeg': 1}
        if p.algorithm_type != 3:
            self.img = self.load()

    def load(self) -> np.array:
            try:
                self.img = mpimg.imread(self.image_file_path)
                img_gray = self.__rgb2gray()
                return (img_gray * self.__image_format_multiplier()).astype(np.uint16)
            except:
                ErrorHandling.verify_image_existence()

    def __rgb2gray(self):
        r, g, b = self.img[:, :, 0], self.img[:, :, 1], self.img[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray

    def __image_format_multiplier(self):
        image_format_index = self.image_file_path.find('.')
        image_format = self.image_file_path[image_format_index:]
        try:
            return self.format_values[image_format]
        except:
            ErrorHandling.wrong_image_format()

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

    def export_model_to_binary(self) -> None:
        path = self.Parameters.binary_model_path
        if self.Parameters.model_id == 1:
            self.__export_single_model(path)
        elif self.Parameters.model_id == 2:
            self.__export_multi_model(path)

    def __export_single_model(self, path):
        self.model.flatten('F').astype('float32', order='F').tofile(path + f"model_vp_2d_{self.width}x{self.height}.bin")

    def __export_multi_model(self, path):
        file_names = ["vp", "vs", "rho"]
        for i in range(3):
            self.model[i].flatten('F').astype('float32', order='F').tofile(path + f"model_{file_names[i]}_2d_{self.width}x{self.height}.bin")

    def plot_acoustic(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, self.width - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, self.height - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax.imshow(self.model, cmap="jet", aspect="auto")
        ax.set_title("VP Model", fontsize=15)
        ax.set_xlabel("Distance [m]", fontsize=12)
        ax.set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, label='VP [m/s]')
        cax.set_ticks(np.linspace(self.model.min(), self.model.max(), num=5))

        ax.set_xticks(xloc)
        ax.set_xticklabels(xlab)

        ax.set_yticks(zloc)
        ax.set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()

    def plot_elastic(self):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, self.width - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, self.height - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax[0].imshow(self.model[0], cmap="jet", aspect="auto")
        ax[0].set_title("VP Model", fontsize=13)
        ax[0].set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, ax=ax[0], label='VP [m/s]')
        cax.set_ticks(np.linspace(self.model[0].min(), self.model[0].max(), num=5))

        im2 = ax[1].imshow(self.model[1], cmap="jet", aspect="auto")
        ax[1].set_title("VS Model", fontsize=13)
        ax[1].set_ylabel("Depth [m]", fontsize=12)
        cax2 = fig.colorbar(im2, ax=ax[1], label='VS [m/s]')
        cax2.set_ticks(np.linspace(self.model[1].min(), self.model[1].max(), num=5))

        im3 = ax[2].imshow(self.model[2], cmap="jet", aspect="auto")
        ax[2].set_title("Density Model", fontsize=13)
        ax[2].set_xlabel("Distance [m]", fontsize=12)
        ax[2].set_ylabel("Depth [m]", fontsize=12)
        cax3 = fig.colorbar(im3, ax=ax[2], label='Density [kg/m$^3$]')
        cax3.set_ticks(np.linspace(self.model[2].min(), self.model[2].max(), num=5))

        for i in range(len(ax)):
            ax[i].set_xticks(xloc)
            ax[i].set_xticklabels(xlab)

            ax[i].set_yticks(zloc)
            ax[i].set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()

class Img2Model(Image):
    def __init__(self, p):
        super().__init__(p)
        self.properties = p.vp_velocity
        self.model_extra_routine = p.model_extra_routine
        self.interface_occurence = len(p.vp_velocity)
        self.height, self.width = self.img.shape[:2]
        self.model = self.img
        self.unique_brightness = np.unique(self.img)
        self.frequent_brightness = self.get_predominant_brightness()
        self.respective_value = dict(zip(self.frequent_brightness, self.properties))

    def set_values(self) -> np.array:
        for brightness in self.unique_brightness:
            nearest_value = self.__get_nearest_value(brightness)
            self.model = np.where(self.model == brightness, nearest_value, self.model)

        if self.model_extra_routine:
            self.extra_routine()

    def set_elastic_values(self, p) -> None:
        self.model_elastic = [[] for _ in range(3)] 
        self.properties = [
            p.vp_velocity,
            p.vs_velocity, 
            p.rho_value
        ]
        for i in range(3):
            self.respective_value = dict(zip(self.frequent_brightness, self.properties[i]))
            self.set_values()
            self.model_elastic[i] = self.model
            self.model = self.img  

        self.model = self.model_elastic

    def __get_nearest_value(self, brightness):
        if brightness not in self.frequent_brightness:
            nearest_index = np.argmin(abs(self.frequent_brightness - brightness.astype(np.uint16)))
            return self.respective_value[self.frequent_brightness[nearest_index]]
        return self.respective_value[brightness]

    def get_predominant_brightness(self):
        brightness, counts = np.unique(self.img, return_counts=True)
        idx_sorted_by_count = np.argsort(-counts)[:self.interface_occurence]
        return brightness[idx_sorted_by_count]

class Complex(Image):
    def __init__(self, p):
        super().__init__(p)
        self.height, self.width = self.img.shape[:2]
        self.model = self.img
        self.inverse_velocity = p.inverse_velocity
        self.min_brightness = np.min(self.img)
        self.max_brightness = np.max(self.img)
        self.v_ratio = (p.vpmax - p.vpmin) / (self.max_brightness - self.min_brightness)
        self.brightness = self.img[:, :]
        self.pmin, self.pmax = p.vpmin, p.vpmax 

    def set_values(self):
        arg = (self.brightness - self.min_brightness) * self.v_ratio
        right_property = self.pmax - arg if self.inverse_velocity else self.pmin + arg
        self.model = right_property

    def set_elastic_values(self, p) -> None:
        self.model_elastic = [[] for _ in range(3)]
        self.pmin = [p.vpmin, p.vsmin, p.rhomin]
        self.pmax = [p.vpmax, p.vsmax, p.rhomax]

        for i in range(3):
            self.pmin, self.pmax = self.pmin[i], self.pmax[i]
            self.set_values()  
            self.model_elastic[i] = self.model
            self.model = self.img  

        self.model = self.model_elastic

class Parallel(Image):
    def __init__(self, p):
        super().__init__(p)
        self.properties = p.vp_velocity_parallel
        self.interface_occurence = len(p.vp_velocity_parallel)
        self.height, self.width = p.nz, p.nx
        self.model = np.zeros((self.height, self.width))
        self.interfaces = p.interfaces
        self.value_interfaces = p.vp_velocity_parallel

        self.set_values()

    def set_values(self) -> None:
        if not len(self.interfaces): 
            self.model[:, :] = self.value_interfaces[0] 

        else: 
            self.model[:self.interfaces[0], :] = self.value_interfaces[0]

            for layer, velocity in enumerate(self.value_interfaces[1:]):
                self.model[self.interfaces[layer]:, :] = velocity

    def set_elastic_values(self, p) -> None:
        self.model_elastic = [[] for _ in range(3)]
        self.temp_value_interfaces = [
            p.vp_velocity_parallel,
            p.vs_velocity_parallel, 
            p.density_value_parallel
        ]
        for i in range(3):
            self.value_interfaces = self.temp_value_interfaces[i]
            self.set_values()
            self.model_elastic[i] = self.model
            self.model = np.zeros((self.height, self.width))

        self.model = self.model_elastic

class ModelFactory:
    def __init__(self, p):
        self.p = p
        self.model_id = p.model_id
        self.algorithm_type = p.algorithm_type
        self.plot_model_bool = p.plot_model_bool
        self.model_smoothing_bool = p.model_smoothing_bool
        self.smooth_level = p.smooth_level
        self.model = None  

    def create_model(self):
        self.model = self.__create_model() 
       
        if self.model_smoothing_bool:
            self.__apply_gaussian_smooth()

        if self.p.export_model_to_binary_file:
            self.model.export_model_to_binary()

        return self.model

    def __create_model(self):
        model_class = self.__get_model_class()
        model_instance = model_class(self.p)

        if self.model_id == 1:
            model_instance.set_values()
        elif self.model_id == 2:
            model_instance.set_elastic_values(self.p)
        else:
            raise KeyError("Invalid Model_ID. Choose a valid key [1, 2].")

        return model_instance

    def __get_model_class(self):
        model_classes = {
            1: Img2Model,
            2: Complex,
            3: Parallel
        }

        if self.algorithm_type not in model_classes:
            raise KeyError("Invalid Algoriyhm_Type. Choose a valid key [1, 2, 3].")
        
        return model_classes[self.algorithm_type]

    def __apply_gaussian_smooth(self):
        if self.model_id == 1:
            self.model.model = gaussian_filter(self.model.model, sigma=self.smooth_level)
        elif self.model_id == 2:
            for i in range(3):
                self.model.model[i] = gaussian_filter(self.model.model[i], sigma=self.smooth_level)

    def plot_model(self):
        if self.plot_model_bool:
            
            if self.model_id == 1:
                self.model.plot_acoustic()  
            elif self.model_id == 2:
                self.model.plot_elastic()   
            else:
                raise ValueError("Invalid Model_ID. Choose a valid key [1, 2]")

