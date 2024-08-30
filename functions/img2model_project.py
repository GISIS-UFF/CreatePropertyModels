import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class ErrorHandling:
    """
    Class for management of error messages
    """
    @staticmethod
    def verify_image_existence() -> None:
        print("Image not found. Please verify the file path.")
        exit()

    @staticmethod
    def wrong_image_format() -> None:
        print("Please use a valid image format. [png, jpg, jpeg]")
        exit()

    @staticmethod
    def could_not_open_file() -> None:
        print("Can't open/read file. Make sure your file path is right.")
        exit()

class ImageDimensions:
    def __init__(self, image: np.array) -> None:
        self.image = image
        self.height, self.width = self.image.shape

class ImageLoader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.format_values = {'.png': 255, '.jpg': 1, '.jpeg': 1}

    def load_image(self) -> np.array:
        try: 
            return (self.rgb2gray(mpimg.imread(self.path)) * self.image_format_multiplier(self.path)).astype(np.uint16)
        except:
            ErrorHandling.verify_image_existence()

    def rgb2gray(self, rgb):
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

        return gray   
    
    def image_format_multiplier(self, path: str):
        image_format_index = path.find('.')
        image_format = path[image_format_index:]
        try:
            return self.format_values[image_format]
        except:
            ErrorHandling.wrong_image_format()


class FindPredominantBrightness(ImageDimensions):
    """
    Get frequent brightness values of the image
    """
    def __init__(self, image: np.array):
        super().__init__(image)
        self.unique_brightness_values = self.image.flatten()

    def get_image_predominant_brightness(self, tolerance=1000):
        self.count = self.__get_predominant_color_loop()
        return [int(brightness_value) for brightness_value, occurrence in self.count.items() if occurrence > tolerance]

    def __get_predominant_color_loop(self):
        count = {}
        for brightness_value in self.unique_brightness_values:
            count[brightness_value] = count.get(brightness_value, 0) + 1
        return count        

class CreateModel(ImageDimensions):
    """
    Image -> Model conversion 
    """
    def __init__(self, image: np.array, frequent_brightness: list, value_interfaces: list, routine_bool: bool) -> None:
        super().__init__(image)
        self.frequent_brightness = frequent_brightness
        self.value_interfaces = value_interfaces
        self.respective_value = dict(zip(frequent_brightness, value_interfaces))
        self.model = np.zeros((self.height, self.width))
        self.routine_bool = routine_bool

    def set_model_values(self) -> np.array:
        for i in range(self.height):
            for j in range(self.width):
                brightness = self.image[i][j]
                self.model[i][j] = self.respective_value[brightness]

        self.__change_wrong_brightness_value_loop()
        if self.routine_bool: ModelRoutine(self.model).model_routine_loop()
        return self.model

    def __change_wrong_brightness_value_loop(self):
        for i in range(self.height):
            for j in range(self.width):
                brightness = self.image[i][j]
                if brightness not in self.respective_value:
                    nearest_index = self.__closest_brightness_value(brightness, self.frequent_brightness)
                    self.model[i][j] = self.respective_value[list(self.respective_value.keys())[nearest_index]]

    def __closest_brightness_value(self, brightness: int, frequent_brightness: list) -> int:
        """
        opencv automatically puts brightness values as int8, in this function I had to change it to int16
        to be sure it gets the right value
        """
        return np.argmin([abs(element - brightness.astype(np.uint16)) for element in frequent_brightness])

class CreateComplexModel(ImageDimensions):
    def __init__(self, image: np.array, pmin: float, pmax: float, inverse_velocity: bool) -> None:
        super().__init__(image)
        self.pmin = pmin
        self.pmax = pmax
        self.inverse_velocity = inverse_velocity
        self.model = np.zeros((self.height, self.width))

    def set_model_values(self):
        min_brightness = np.min(self.image)
        max_brightness = np.max(self.image)
        v_ratio = (self.pmax - self.pmin) / (max_brightness - min_brightness)
        for i in range(self.height):
            for j in range(self.width):
                brightness = self.image[i][j]
                self.model[i][j] = self.__get_velocity_order(brightness, v_ratio, min_brightness)
        return self.model

    def __get_velocity_order(self, brightness, v_ratio, min_brightness):
        arg = (brightness - min_brightness) * v_ratio
        return self.pmax - arg if self.inverse_velocity else self.pmin + arg 
    
class ModelRoutine(CreateModel):
    """
    Extra routine for images not made in MS Paint
    """
    def __init__(self, model):
        self.model = model
        self.height, self.width = self.model.shape

    def model_routine_loop(self):
        for i in range(self.height):
            for j in range(self.width):
                adj_values = self.__get_adjacent(self.model, i, j)
                arr_condition = self.__check_diff_brightness_condition(adj_values)
                if len(arr_condition) > 0:
                    self.model[i][j] = arr_condition[0]
        return self.model

    def __get_adjacent(self, arr: list, i: int, j: int) -> list:
        # I may or may not had a little help on this one :running:
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
        arr_brightness_condition = unique_values[counts > 5]
        return arr_brightness_condition if len(arr_brightness_condition) > 0 else []

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

class AcousticModelPlot:

    @staticmethod
    def acoustic_plot(model: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax.imshow(model, cmap="jet", aspect="auto")
        ax.set_title("VP Model", fontsize=15)
        ax.set_xlabel("Distance [m]",fontsize=12)
        ax.set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, label='VP [m/s]')
        cax.set_ticks(np.linspace(model.min(), model.max(), num=5))

        ax.set_xticks(xloc)
        ax.set_xticklabels(xlab)

        ax.set_yticks(zloc)
        ax.set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()
        return fig

class ElasticModelPlot:
    
    @staticmethod
    def elastic_model_plot(model_vp: list, model_vs: list, model_rho: list, Nx: int, Nz: int):
        fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(10,8))

        xloc = np.linspace(0, Nx - 1, 7, dtype=int)
        xlab = np.array(xloc, dtype=int)

        zloc = np.linspace(0, Nz - 1, 7, dtype=int)
        zlab = np.array(zloc, dtype=int)

        im = ax[0].imshow(model_vp, cmap="jet", aspect="auto")
        ax[0].set_title("VP Model", fontsize=13)
        #ax[0].set_xlabel("Distance [m]",fontsize=12)
        ax[0].set_ylabel("Depth [m]", fontsize=12)
        cax = fig.colorbar(im, ax=ax[0], label='VP [m/s]')
        cax.set_ticks(np.linspace(model_vp.min(), model_vp.max(), num=5))

        im2 = ax[1].imshow(model_vs, cmap="jet", aspect="auto")
        ax[1].set_title("VS Model", fontsize=13)
        #ax[1].set_xlabel("Distance [m]",fontsize=12)
        ax[1].set_ylabel("Depth [m]", fontsize=12)
        cax2 = fig.colorbar(im2, ax=ax[1], label='VS [m/s]')
        cax2.set_ticks(np.linspace(model_vs.min(), model_vs.max(), num=5))

        im3 = ax[2].imshow(model_rho, cmap="jet", aspect="auto")
        ax[2].set_title("Density Model", fontsize=13)
        ax[2].set_xlabel("Distance [m]",fontsize=12)
        ax[2].set_ylabel("Depth [m]", fontsize=12)
        cax3 = fig.colorbar(im3, ax=ax[2], label='Density [kg/m$^3$]')
        cax3.set_ticks(np.linspace(model_rho.min(), model_rho.max(), num=5))

        for i in range(len(ax)):
            ax[i].set_xticks(xloc)
            ax[i].set_xticklabels(xlab)

            ax[i].set_yticks(zloc)
            ax[i].set_yticklabels(zlab)

        plt.tight_layout()
        plt.show()
        return fig

class Export2Binary:
    """
    Exports model to a binary file
    """
    def __init__(self, model: np.array, path: str) -> None:
        self.model = model
        self.path = path

    def export_model_to_binary(self) -> None:
        self.model.flatten('F').astype('float32', order='F').tofile(self.path)

class ModelCreator:
    @staticmethod
    def create_model(image: np.array, frequent_brightness: list, interfaces: list, routine_bool: bool) -> np.array:
        model_creator = CreateModel(image, frequent_brightness, interfaces, routine_bool)
        return model_creator.set_model_values()
