from src import np, ImageDimensions, ModelRoutine

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

    def set_values(self) -> np.array:
        for i in range(self.height):
            for j in range(self.width):
                brightness = self.image[i][j]
                self.model[i][j] = self.respective_value[brightness]

            self.__change_wrong_brightness_value_loop(brightness, i, j)
        if self.routine_bool: ModelRoutine(self.model).model_routine_loop()
        return self.model

    def __change_wrong_brightness_value_loop(self, brightness, i, j):
        if brightness not in self.respective_value:
            nearest_index = self.__closest_brightness_value(brightness, self.frequent_brightness)
            self.model[i][j] = self.respective_value[list(self.respective_value.keys())[nearest_index]]

    def __closest_brightness_value(self, brightness: int, frequent_brightness: list) -> int:
        """
        opencv automatically puts brightness values as int8, in this function I had to change it to int16
        to be sure it gets the right value
        """
        return np.argmin([abs(element - brightness.astype(np.uint16)) for element in frequent_brightness])

