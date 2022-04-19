from PIL import Image
import io as libio

from cloud_helper import get_cloudant_client, get_cloudant_processed_db, get_cos_client, get_upload_bucket


class UploadData:

    def __init__(self, metadata, annotation_meta, image):
        file = self.upload_metadata(metadata, annotation_meta)
        self.write_image_cos(get_cos_client(), get_upload_bucket(), file, image)

    @staticmethod
    def upload_metadata(metadata, annotation_meta):
        cloudant, _ = get_cloudant_client()
        db = get_cloudant_processed_db()
        metadata = metadata['doc']
        del metadata['_id']
        del metadata['_rev']
        metadata['user_metadata']['data_details']['annotation_details'] = annotation_meta
        metadata['system_metadata']['bucket'] = get_upload_bucket()
        response = cloudant.post_document(db=db, document=metadata).get_result()
        return metadata['system_metadata']['filename']

    def write_image_cos(self, client, bucket, file, image):
        # Convert numpy.ndarray into PIL.Image.Image object. This features a 'save' method that will be used below
        n = image.ndim
        if n == 3:
            img = Image.fromarray(image, 'RGB')
        # Binary or gray level image
        else:
            # Binary
            if image.max() == 1:
                img = Image.fromarray(image, '1').convert('RGB')
            else:
                img = Image.fromarray(image, 'L').convert('RGB')

        # Create buffer to hold jpeg representation of image in 'io.BytesIO' object
        bufImage = libio.BytesIO()
        # Store jpeg representation of image in buffer
        img.save(bufImage, self.get_file_extension(file))
        # Rewind the buffer to beginning
        bufImage.seek(0)
        # Provide the jpeg object to the Body parameter of put_object to write image to COS
        client.put_object(Bucket=bucket, Body=bufImage, Key=file, ContentType='image/jpeg')
        print("WriteImage: \n\tBucket=%s \n\tFile=%s \n\tArraySize=%d %s RawSize=%d\n" % (
            bucket, file, image.size, image.shape, bufImage.getbuffer().nbytes))

    @staticmethod
    def get_file_extension(filename):
        ext = filename.split('.')[1]
        if ext == 'png':
            return 'PNG'
        return 'JPEG'
