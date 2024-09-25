class Export2Binary:
    """
    Exports model to a binary file
    """
    def __init__(self, model: np.array, path: str) -> None:
        self.model = model
        self.path = path

    def export_model_to_binary(self) -> None:
        self.model.flatten('F').astype('float32', order='F').tofile(self.path)
