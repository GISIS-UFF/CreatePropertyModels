
class CreateComplexModel():
    def __init__(self, pmin: float, pmax: float, inverse_velocity: bool) -> None:
        self.pmin = pmin
        self.pmax = pmax
        self.inverse_velocity = inverse_velocity
        self.model = np.zeros((height, width))

    def set_values(self):
        min_brightness = np.min(img)
        max_brightness = np.max(img)
        v_ratio = (self.pmax - self.pmin) / (max_brightness - min_brightness)
        for i in range(height):
            for j in range(width):
                brightness = img[i][j]
                self.model[i][j] = self.__get_velocity_order(brightness, v_ratio, min_brightness)
        return self.model

    def __get_velocity_order(self, brightness, v_ratio, min_brightness):
        arg = (brightness - min_brightness) * v_ratio
        return self.pmax - arg if self.inverse_velocity else self.pmin + arg 
