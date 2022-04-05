import types
from io import BytesIO

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from initialize_configuration import Configuration


class ReadImageData:
    def __init__(self):
        self.configuration = Configuration()

    # Method to read image from cos into numpy.ndarray
    @staticmethod
    def read_image(client, bucket, file):
        def __iter__():
            return 0

        # Download file from COS into a 'ibm_botocore.response.StreamingBody' object
        streaming_body_response = client.get_object(Bucket=bucket, Key=file)
        # Extract the image data from the 'Body' slot into a byte array
        image = streaming_body_response['Body']

        if not hasattr(image, "__iter__"):
            image.__iter__ = types.MethodType(__iter__, image)
        # Convert the image data into a numpy.ndarray of size rRows*cCols*nColorChannels
        img = mpimg.imread(BytesIO(image.read()), 'jpg')
        return img

    # Method to display data fetched from object storage
    @staticmethod
    def display_sample_date(data, items):
        plt.figure(figsize=(10, 10))
        print('data size', len(data))
        for i in range(items):
            plt.subplot(3, 3, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(data[i])
        plt.show()

    # method to access cos data based on search query (currently - bucket name)
    def read_data_ibm_cos(self, limit):
        image_data, labels = [], []
        cos, _ = self.configuration.initialize_cos_configuration()
        cloudant, db, _ = self.configuration.initialize_cloudant_configuration()
        # print('Database', cloudant.get_all_dbs().get_result())
        documents = cloudant.post_all_docs(db=db, include_docs=True, limit=limit).get_result()
        metadata = documents['rows']

        # fetch image data for each metadata file
        for item in metadata:
            bucket_ = item['doc']['system_metadata']['bucket']
            file = item['doc']['system_metadata']['filename']
            labels.append(file.split("/")[1])
            image_data.append(self.read_image(cos, bucket_, file))
        # print(metadata[-1]['doc'])
        # objects = cos.list_objects(Bucket=bucket, MaxKeys=10)['Contents']
        # for obj in objects:
        #     data.append(self.read_image(cos, bucket, obj['Key']))
        return metadata, image_data, labels
