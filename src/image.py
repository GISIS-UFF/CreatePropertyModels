from src import np, mpimg, ErrorHandling

class Image():
    def __init__(self, image_file_path: str) -> None:
        self.image_file_path = image_file_path
        self.format_values = {'.png': 255, '.jpg': 1, '.jpeg': 1}
        self.img = self.load()
        self.dimensions = self.get_dimension()  

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

    def get_dimension(self) -> tuple:
        return self.img.shape[:2]

