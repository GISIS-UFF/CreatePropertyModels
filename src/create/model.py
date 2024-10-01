from src import np, Image

class CreateModel():
    """
    Image -> Model conversion 
    """
    def __init__(self, image: Image, frequent_brightness: list, value_interfaces: list, routine_bool: bool) -> None:
        self.image = image.img  
        self.height, self.width = image.dimensions 
        self.frequent_brightness = frequent_brightness
        self.value_interfaces = value_interfaces
        self.respective_value = dict(zip(frequent_brightness, value_interfaces))
        self.routine_bool = routine_bool
        self.model = np.zeros((self.height, self.width))

    def set_values(self) -> np.array:
        img = self.image  
        for i in range(self.height):
            for j in range(self.width):
                brightness = img[i, j]  
                self.model[i, j] = self.respective_value.get(brightness, 0)

                self.__change_wrong_brightness_value_loop(brightness, i, j)
                
        # if self.routine_bool: 
        #     routine = ModelRoutine(self.model) 
        #     routine.loop()
        return self.model

    def __change_wrong_brightness_value_loop(self, brightness, i, j):
        if brightness not in self.respective_value:
            nearest_index = self.__closest_brightness_value(brightness, self.frequent_brightness)
            self.model[i, j] = self.respective_value[self.frequent_brightness[nearest_index]]

    def __closest_brightness_value(self, brightness: int, frequent_brightness: list) -> int:
        """
        opencv automatically puts brightness values as int8, in this function I had to change it to int16
        to be sure it gets the right value
        """
        return np.argmin([abs(element - brightness.astype(np.uint16)) for element in frequent_brightness])
