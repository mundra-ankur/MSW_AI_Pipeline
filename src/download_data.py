import types
from io import BytesIO

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from ibm_botocore.exceptions import ClientError

from cloud_helper import get_cos_client, get_cloudant_client, get_cloudant_processed_db, get_cos_resource


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
def get_data_ibm_cos(limit):
    image_data, labels, annotation = [], [], []
    cos = get_cos_client()
    cloudant, db = get_cloudant_client()
    documents = cloudant.post_all_docs(db=db, include_docs=True, limit=limit).get_result()
    metadata = documents['rows']

    # fetch image data for each metadata file
    for item in metadata:
        bucket = item['doc']['system_metadata']['bucket']
        file = item['doc']['system_metadata']['filename']
        labels.append(file.split("/")[1])
        # print("Fetching image", file, "from bucket", bucket, "with label", labels[-1])
        image = read_image(cos, bucket, file)

        if image is not None:
            image_data.append(image)
    return metadata, image_data, labels


# method to access cos data based on search query (currently - bucket name)
def get_preprocessed_data(limit):
    image_data, labels, annotation = [], [], []
    cos = get_cos_client()
    cloudant, _ = get_cloudant_client()
    db = get_cloudant_processed_db()
    documents = cloudant.post_all_docs(db=db, include_docs=True, limit=limit).get_result()
    metadata = documents['rows']

    # fetch image data for each metadata file
    for item in metadata:
        bucket = item['doc']['system_metadata']['bucket']
        file = item['doc']['system_metadata']['filename']
        annotation_detail = item['doc']['user_metadata']['data_details']['annotation_details']['annotations']

        # For Single Object
        labels.append(annotation_detail[0]['label'])
        annotation.append(annotation_detail[0]['coordinates'])

        image = read_image(cos, bucket, file)
        if image is not None:
            image_data.append(image)
    return metadata, image_data, labels, annotation


def download_file_from_cos(bucket, key_name, local_file_path):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket, key_name))
    try:
        cos_resource = get_cos_resource()
        cos_resource.Object(bucket, key_name).download_file(local_file_path)
    except ClientError as be:
        print("CLIENT ERROR while retrieving file contents: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))
