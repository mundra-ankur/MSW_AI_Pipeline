import os
from pathlib import Path

import cv2
from pywget import wget
from sklearn.model_selection import train_test_split
from download_data import get_preprocessed_data


class PrepareTrainingData:

    def split_train_test_data(self, parent_dir, metadata, data, labels, coordinates):
        train_dir, test_dir = parent_dir + "/train/", parent_dir + "/test/"

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

            filename = directory + meta['doc']['_id']
            cv2.imwrite(filename + ".jpg", image)
            self.create_yolo_label_file(annotation, filename, image, index)
        self.create_class_names_file(classes, parent_dir)

    @staticmethod
    def get_yolo_format_annotations(coordinates, img_width, img_height):
        dw = 1.0 / img_width
        dh = 1.0 / img_height

        x, y, w, h = coordinates
        x = (x + w / 2) * dw
        y = (y + h / 2) * dh
        w = w * dw
        h = h * dh

        return [x, y, w, h]

    def create_yolo_label_file(self, annotation, filename, image, label_id):
        x, y, w, h = self.get_yolo_format_annotations(annotation, image.shape[1], image.shape[0])
        with open(filename + '.txt', 'w') as f:
            f.write("{} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label_id, x, y, w, h))

    @staticmethod
    def create_class_names_file(classes, path):
        for label in classes:
            with open(path + '/obj.names', 'a') as names:
                names.write(label + '\n')

        with open(path + '/obj.data', 'a') as data:
            data.write("classes = {:d}\n".format(len(classes)))

    @staticmethod
    def append_dir_content_in_file(content_path, filename):
        print("Listing item from path: {0}, in file: {1}.txt".format(content_path, filename))
        image_files = []
        current_dir = os.getcwd()
        os.chdir(content_path)
        for file in os.listdir(os.getcwd()):
            if file.endswith(".jpg"):
                image_files.append(content_path + "/" + file)
        os.chdir(current_dir)

        with open(filename + ".txt", "w") as outfile:
            for image in image_files:
                outfile.write(image)
                outfile.write("\n")
            outfile.close()

    def append_training_details(self, darknet_data_dir, training_backup_dir):
        Path(training_backup_dir).mkdir(parents=True, exist_ok=True)
        with open(darknet_data_dir + '/obj.data', 'a') as data:
            data.write("train = {0}/train.txt\n".format(darknet_data_dir))
            data.write("valid = {0}/test.txt\n".format(darknet_data_dir))
            data.write("names = {0}/obj.names\n".format(darknet_data_dir))
            data.write("backup = {0}".format(training_backup_dir))

    def download_pretrained_weights(self, model_dir):
        print('Downloading Pretrained weights for training...')
        url = 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137'
        wget.download(url, model_dir+"/yolov4.conv.137")

    @staticmethod
    def get_data_from_cos(data_size):
        return get_preprocessed_data(limit=data_size)

    def __init__(self, data_limit, darknet_data_dir, training_backup_dir):
        metadata, data, labels, annotations = self.get_data_from_cos(data_limit)
        self.split_train_test_data(darknet_data_dir, metadata, data, labels, annotations)
        self.append_dir_content_in_file(darknet_data_dir + "/train", "train")
        self.append_dir_content_in_file(darknet_data_dir + "/test", "test")
        self.append_training_details(darknet_data_dir, training_backup_dir)
        self.download_pretrained_weights(darknet_data_dir)


PrepareTrainingData(30, 'model/testY/data', 'model/train_backup')
