import os

import cv2 as cv
import numpy as np


class ModelPrediction:
    model = None
    colors = None
    classes = None
    width = 416
    height = 416

    def detect(self, file_path, conf):
        try:
            img = cv.imread(file_path)
            classIds, scores, boxes = self.model.detect(img, confThreshold=conf, nmsThreshold=0.45)

            for (classId, score, box) in zip(classIds, scores, boxes):
                print(self.classes[classId], score)
                color = [int(c) for c in self.colors[classId]]
                cv.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                             color=color, thickness=2)

                text = '%s: %.2f' % (self.classes[classId], score)
                cv.putText(img, text, (box[0], box[1] - 5), cv.FONT_HERSHEY_SIMPLEX, 1,
                           color=color, thickness=2)
            print('-----------------------------------')
            cv.imshow('Prediction', img)
            cv.waitKey(0)
            cv.destroyAllWindows()
        except:
            print(file_path, "not able to detect")

    def load_model(self):
        # Load names of classes and get random colors
        self.classes = open('model/yolov4/coco.names').read().strip().split('\n')
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')
        # Give the configuration and weight files for the model and load the network.
        net = cv.dnn.readNetFromDarknet('model/yolov4/yolov4_custom.cfg', 'model/yolov4/yolov4_new.weights')
        self.model = cv.dnn_DetectionModel(net)
        self.model.setInputParams(scale=1 / 255, size=(self.width, self.height), swapRB=True)

    def __init__(self):
        self.load_model()
        for file in os.listdir('data'):
            self.detect('data/' + file, 0.2)


model = ModelPrediction()
