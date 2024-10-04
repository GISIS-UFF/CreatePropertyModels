from src import np

class PredominantBrightness():
    """
    Get frequent brightness values of the image
    """
    def __init__(self, img: np.array, interface_occurence: int):
        self.img = img
        self.interface_occurence = interface_occurence
        self.unique_brightness_values = img.flatten()
        self.brightness = self.get() 

    def get(self):
        brightness, counts = np.unique(self.unique_brightness_values, return_counts=True)
        
        sorted_counts = np.sort(counts)[:self.interface_occurence]
        
        idx = []
        for i, n in enumerate(counts):
            if n in sorted_counts:
                idx.append(i)
        
        return brightness[idx]

        

