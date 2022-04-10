from pathlib import Path

import cv2
from sklearn.model_selection import train_test_split
from data_annotation import Annotation
from initialize_configuration import initialize_cloudant_configuration
from download_data import get_data_ibm_cos


class PrepareTrainingData:

    @staticmethod
    def convert_yolo_format(coordinates, img_width, img_height):
        dw = 1.0 / img_width
        dh = 1.0 / img_height

        x, y, w, h = coordinates
        x = (x + w / 2) * dw
        y = (y + h / 2) * dh
        w = w * dw
        h = h * dh

        return [x, y, w, h]

    def make_train_test_folder(self, parent_dir, metadata, data, labels, coordinates):
        train_dir, test_dir = parent_dir + "/train", parent_dir + "/test"

        Path(train_dir).mkdir(parents=True, exist_ok=True)
        Path(test_dir).mkdir(parents=True, exist_ok=True)

        x_train, _, _, _ = train_test_split(metadata, labels, test_size=0.2, random_state=40)

        classes = []
        for meta, image, label, annotation in zip(metadata, data, labels, coordinates):
            directory = train_dir if meta in x_train else test_dir
            index = len(classes)
            if label in classes:
                index = classes.index(label)
            else:
                classes.append(label)

            filename = meta['doc']['_id']
            cv2.imwrite(directory + "/" + filename + ".jpg", image)
            x, y, w, h = self.convert_yolo_format(annotation, image.shape[1], image.shape[0])
            with open(directory + '/' + filename + '.txt', 'w') as f:
                f.write("{} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(index, x, y, w, h))

        for label in classes:
            with open(parent_dir + '/obj.names', 'a') as names:
                names.write(label + '\n')

    def prepare_annotated_data(self, parent_dir):
        annotation = Annotation()
        metadata, data, labels, coordinates = annotation.get_annotated_data()
        self.make_train_test_folder(parent_dir, metadata, data, labels, coordinates)

    def prepare_data_from_cos(self, parent_dir):
        cloudant, _, db = initialize_cloudant_configuration()
        metadata, data, labels, annotations = get_data_ibm_cos(limit=30, cloudant=cloudant, cloudant_db=db,
                                                               processed=True)
        self.make_train_test_folder(parent_dir, metadata, data, labels, annotations)


prep = PrepareTrainingData()
prep.prepare_data_from_cos('model/testY')
