from src import np

class ImageDimensions:
    def __init__(self, image: np.array) -> None:
        self.image = image
        self.height, self.width = self.image.shape

class ImageLoader:
    def __init__(self, path: str) -> None:
        self.path = path
        self.format_values = {'.png': 255, '.jpg': 1, '.jpeg': 1}
    def load(self) -> np.array:
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
