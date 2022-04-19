import cv2 as cv

from download_data import get_data_ibm_cos


class ImageResize:

    def __init__(self, width, height, interpolation_method):
        self.meta, self.data, self.labels = get_data_ibm_cos(limit=30)
        self.width, self.height = width, height
        self.interpolation_method = interpolation_method

    # Resizing by Specifying Width, Height, and Interpolation Method
    @staticmethod
    def resize(image, width, height, interpolation):
        resize = cv.resize(image, dsize=(width, height), interpolation=interpolation)
        return resize

    def get_resized_data(self):
        resized_data = []
        for image in self.data:
            resized_data.append(self.resize(image, self.width, self.height, self.interpolation_method))
        return self.meta, resized_data, self.labels
