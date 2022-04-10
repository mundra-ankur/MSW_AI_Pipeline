import cv2 as cv
import numpy as np

from data_preprocessing import ImageResize
from upload_processed_data import UploadData


class Annotation:
    ADAPTIVE_THRESHOLD_CONTOUR = 0  # add this in meta file
    EDGE_DETECTION_CONTOUR = 1

    def find_contours(self, image, method=0):
        # Blur the image to remove noise
        blurred_image = cv.GaussianBlur(image, ksize=(5, 5), sigmaX=0)

        if method == self.EDGE_DETECTION_CONTOUR:
            # Apply canny edge detection
            binary = cv.Canny(blurred_image, threshold1=100, threshold2=160)
        else:
            gray = cv.cvtColor(blurred_image, cv.COLOR_BGR2GRAY)
            # Perform adaptive thresholding
            binary = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 11, 5)

        # Detect the contour using the edges
        contours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # cv.drawContours(image, contours, -1, (0, 255, 0), 2)
        return contours

    # Draw a bounding box around contour
    def draw_bounding_rectangle(self, contours, image, method=0):
        x, y, p, q = 5000, 5000, 0, 0
        area = 50
        for c in contours:
            x1, y1, w1, h1 = cv.boundingRect(c)
            x2 = x1 + w1
            y2 = y1 + h1

            if method == self.EDGE_DETECTION_CONTOUR or cv.contourArea(c) > area:
                x, y, p, q = min(x, x1), min(y, y1), max(p, x2), max(q, y2)

        cv.rectangle(image, (x, y), (p, q), (255, 0, 0), 2)
        return image, (x, y, p - x, q - y)

    # Draw a bounding box around largest contour
    @staticmethod
    def draw_bounding_rectangle_(contours, image):
        x, y, w, h = 0, 0, 0, 0
        area = 0
        for c in contours:
            if cv.contourArea(c) > area:
                area = cv.contourArea(c)
                x, y, w, h = cv.boundingRect(c)

        # draw rectangle on biggest contour
        cv.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return image, (x, y, w, h)

    @staticmethod
    def display_annotated_image(drawn_contour):
        cv.imshow('Contour with bounding box', drawn_contour)
        cv.waitKey(0)
        cv.destroyAllWindows()

    @staticmethod
    def display_images(image1, image2):
        concatenated = np.concatenate((image1, image2), axis=1)
        cv.imshow('Bounding Box: Edge Detection ---- Adaptive Threshold', concatenated)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def get_annotated_data(self):
        return self.annotated_data

    def __init__(self):
        self.annotated_data = []
        resize = ImageResize(416, 416, cv.INTER_LINEAR)
        metadata, data, labels = resize.get_resized_data()
        coordinates = []
        # for file in os.listdir('data'):
        for meta, image, label in zip(metadata, data, labels):
            # Make a copy
            new_image = image.copy()
            # contours_edge = self.find_contours(new_image, self.EDGE_DETECTION_CONTOUR)
            contours_adaptive = self.find_contours(new_image, self.ADAPTIVE_THRESHOLD_CONTOUR)
            # drawn_contour_edge, _ = self.draw_bounding_rectangle(contours_edge, image, self.EDGE_DETECTION_CONTOUR)
            drawn_contour_adaptive, coordinates_adaptive = self.draw_bounding_rectangle(contours_adaptive, new_image,
                                                                                        self.ADAPTIVE_THRESHOLD_CONTOUR)
            coordinates.append(coordinates_adaptive)
            # self.display_images(drawn_contour_edge, drawn_contour_adaptive)
            self.display_annotated_image(drawn_contour_adaptive)
            self.upload_processed_image(meta, new_image, label, coordinates_adaptive)
        self.annotated_data = (metadata, data, labels, coordinates)

    @staticmethod
    def upload_processed_image(metadata, image, label, coordinates):
        annotation_details = {
            "dimension": {
                "width": image.shape[1],
                "height": image.shape[0]
            },
            "annotations": [
                {
                    "label": label,
                    "coordinates": coordinates
                }
            ]
        }

        upload = UploadData()
        upload.upload_data(metadata, annotation_details)


# annotation = Annotation()
