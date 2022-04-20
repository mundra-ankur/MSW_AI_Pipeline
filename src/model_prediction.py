import os

import cv2 as cv
import numpy as np
import logging


class ModelPrediction:
    model = None
    colors = None
    classes = None
    width = 416
    height = 416

    def detect(self, file_path, conf):
        try:
            logging.debug('Making inference on file %s', file_path)
            img = cv.imread(file_path)
            classIds, scores, boxes = self.model.detect(img, confThreshold=conf, nmsThreshold=0.45)

            logging.info('Inference detected:')
            logging.info('class, confidence, coordinates')
            for (classId, score, box) in zip(classIds, scores, boxes):
                color = [int(c) for c in self.colors[classId]]
                cv.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]),
                             color=color, thickness=2)

                text = '%s: %.2f' % (self.classes[classId], score)
                cv.putText(img, text, (box[0], box[1] - 5), cv.FONT_HERSHEY_SIMPLEX, 1, color=color, thickness=2)
                logging.info('%s, %f, [%s, %s]', self.classes[classId], score, (box[0], box[1]),
                             (box[0] + box[2], box[1] + box[3]))
            logging.info('-----------------------------------')
            cv.imshow('Prediction', img)
            cv.waitKey(0)
            cv.destroyAllWindows()
        except:
            logging.error("%s not able to detect", file_path)

    def load_model(self):
        # Load names of classes and get random colors
        logging.info('loading pretrained model from model/yolov4')
        self.classes = open('model/yolov4/coco.names').read().strip().split('\n')
        self.colors = np.random.randint(0, 255, size=(len(self.classes), 3), dtype='uint8')
        # Give the configuration and weight files for the model and load the network.
        net = cv.dnn.readNetFromDarknet('model/yolov4/yolov4_custom.cfg', 'model/yolov4/yolov4_new.weights')
        self.model = cv.dnn_DetectionModel(net)
        logging.debug('Model input width: %d, height: %d, and scale: %f', self.width, self.height, 1 / 255)
        self.model.setInputParams(scale=1 / 255, size=(self.width, self.height), swapRB=True)
        logging.info('pretrained model is loaded successfully!')

    def __init__(self):
        formatter = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename='log/inference.log', format=formatter, level=logging.DEBUG)
        logging.info('Starting Model Inference')
        self.load_model()
        for file in os.listdir('data'):
            self.detect('data/' + file, 0.2)


model = ModelPrediction()
