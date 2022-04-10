import argparse
import os


def parser():
    arg_parser = argparse.ArgumentParser(description="YOLO Object Detection")
    arg_parser.add_argument("--data_directory", default="data",
                            help="path to data directory")
    arg_parser.add_argument("--filename", type=str, default="",
                            help="name of the file which contains the list of images")
    return arg_parser.parse_args()


def check_arguments_errors(args):
    if not os.path.exists(args.data_directory):
        raise (ValueError("Invalid data directory path {}".format(os.path.abspath(args.data_directory))))
    if args.filename.find('.') != -1:
        raise (ValueError("Invalid file name, please provide a valid file name without any extension. eg. train"))


def generate_file(path, filename):
    image_files = []
    os.chdir(path)
    for file in os.listdir(os.getcwd()):
        if file.endswith(".jpg"):
            image_files.append(path + "/" + file)
    os.chdir("..")

    with open(filename + ".txt", "w") as outfile:
        for image in image_files:
            outfile.write(image)
            outfile.write("\n")
        outfile.close()
    os.chdir("..")


def main():
    args = parser()
    check_arguments_errors(args)
    generate_file(args.data_directory, args.filename)


if __name__ == "__main__":
    main()
