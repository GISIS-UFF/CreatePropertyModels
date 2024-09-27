
class FindPredominantBrightness():
    """
    Get frequent brightness values of the image
    """
    def __init__(self, img):
        self.img = img
        self.unique_brightness_values = img.flatten()

    def get(self, tolerance=1000):
        self.count = self.__get_color_loop()
        return [int(brightness_value) for brightness_value, occurrence in self.count.items() if occurrence > tolerance]

    def __get_color_loop(self):
        count = {}
        for brightness_value in self.unique_brightness_values:
            count[brightness_value] = count.get(brightness_value, 0) + 1
        return count  
