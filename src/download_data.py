import types
from io import BytesIO

import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from initialize_configuration import initialize_cos_configuration


# Method to read image from cos into numpy.ndarray
def read_image(client, bucket, file):
    def __iter__():
        return 0

    # Download file from COS into a 'ibm_botocore.response.StreamingBody' object
    try:
        streaming_body_response = client.get_object(Bucket=bucket, Key=file)
        # Extract the image data from the 'Body' slot into a byte array
        image = streaming_body_response['Body']

        if not hasattr(image, "__iter__"):
            image.__iter__ = types.MethodType(__iter__, image)
        # Convert the image data into a numpy.ndarray of size rRows*cCols*nColorChannels
        img = mpimg.imread(BytesIO(image.read()), 'jpg')
        return img
    except:
        print(file, 'is not available!')
        return None


# Method to display data fetched from object storage
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
def get_data_ibm_cos(limit, cloudant, cloudant_db, processed=False):
    image_data, labels, annotation = [], [], []
    cos, _ = initialize_cos_configuration()
    # print('Database', cloudant.get_all_dbs().get_result())
    documents = cloudant.post_all_docs(db=cloudant_db, include_docs=True, limit=limit).get_result()
    metadata = documents['rows']

    # fetch image data for each metadata file
    for item in metadata:
        bucket = item['doc']['system_metadata']['bucket']
        file = item['doc']['system_metadata']['filename']
        # print(item['doc']['_id'], bucket, file)
        if processed:
            annotation_detail = item['doc']['user_metadata']['data_details']['annotation_details']['annotations']
            labels.append(annotation_detail[0]['label'])
            annotation.append(annotation_detail[0]['coordinates'])
        else:
            labels.append(file.split("/")[1])

        image = read_image(cos, bucket, file)
        if image is not None:
            image_data.append(image)

    if processed:
        return metadata, image_data, labels, annotation
    return metadata, image_data, labels
