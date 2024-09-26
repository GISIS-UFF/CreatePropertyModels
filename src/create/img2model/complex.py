from src import np, ImageDimensions

class CreateComplexModel(ImageDimensions):
    def __init__(self, image: np.array, pmin: float, pmax: float, inverse_velocity: bool) -> None:
        super().__init__(image)
        self.pmin = pmin
        self.pmax = pmax
        self.inverse_velocity = inverse_velocity
        self.model = np.zeros((self.height, self.width))

    def set_values(self):
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
