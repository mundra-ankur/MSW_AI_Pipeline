import argparse
import os

import cv2
from pywget import wget
from sklearn.model_selection import train_test_split

from download_data import get_preprocessed_data


def parser():
    arg_parser = argparse.ArgumentParser(description="YOLO Object Detection")
    arg_parser.add_argument("--darknet_data_directory", default="data",
                            help="path to darknet data directory")
    arg_parser.add_argument("--train_backup", type=str, default="",
                            help="path to backup directory which will take backup during training")
    arg_parser.add_argument("--data_limit", type=int, default=1000,
                            help="Number of data files to be fetched for training")
    return arg_parser.parse_args()


def check_arguments_errors(args):
    if not os.path.exists(args.darknet_data_directory):
        raise (ValueError("Invalid data directory path {}".format(os.path.abspath(args.darknet_data_directory))))
    if not os.path.exists(args.train_backup):
        os.makedirs(args.train_backup, exist_ok=True)
        print("Backup directory created {}".format(os.path.abspath(args.train_backup)))


def split_train_test_data(metadata, data, labels, coordinates):
    train_dir, test_dir = "train/", "test/"

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

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
        create_yolo_label_file(annotation, filename, image, index)
    create_class_names_file(classes)


def get_yolo_format_annotations(coordinates, img_width, img_height):
    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x, y, w, h = coordinates
    x = (x + w / 2) * dw
    y = (y + h / 2) * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]


def create_yolo_label_file(annotation, filename, image, label_id):
    x, y, w, h = get_yolo_format_annotations(annotation, image.shape[1], image.shape[0])
    with open(filename + '.txt', 'w') as f:
        f.write("{} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label_id, x, y, w, h))


def create_class_names_file(classes):
    for label in classes:
        with open('obj.names', 'a') as names:
            names.write(label + '\n')

    with open('obj.data', 'a') as data:
        data.write("classes = {:d}\n".format(len(classes)))


def append_dir_content_in_file(content_path, filename):
    print("Listing item from path: {0}, in file: {1}.txt".format(content_path, filename))
    image_files = []
    os.chdir(content_path)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".jpg"):
            image_files.append("data/" + content_path + "/" + file)
    os.chdir('..')

    with open(filename + ".txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()


def append_training_details(training_backup_dir):
    with open('obj.data', 'a') as data:
        data.write("train = data/train.txt\n")
        data.write("valid = data/test.txt\n")
        data.write("names = data/obj.names\n")
        data.write("backup = {0}".format(training_backup_dir))


def download_pretrained_weights():
    print('Downloading Pretrained weights for training...')
    url = 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137'
    wget.download(url, "yolov4.conv.137")


def get_data_from_cos(data_size):
    return get_preprocessed_data(limit=data_size)


def main():
    args = parser()
    check_arguments_errors(args)
    darknet_data_dir = args.darknet_data_directory
    os.chdir(darknet_data_dir)
    metadata, data, labels, annotations = get_data_from_cos(args.data_limit)
    split_train_test_data(metadata, data, labels, annotations)
    append_dir_content_in_file("train", "train")
    append_dir_content_in_file("test", "test")
    append_training_details(args.train_backup)
    download_pretrained_weights()
    print('\nModel is ready for Training!')
    print('Note: Change the configuration file available in cfg folder as per your needs.')


if __name__ == "__main__":
    main()

# python src/prepare_yolo_training.py --darknet_data_directory model/data --data_limit 30 --train_backup
# model/train_backup2
