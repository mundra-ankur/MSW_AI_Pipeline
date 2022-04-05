from initialize_configuration import Configuration


class UploadData:

    def __init__(self):
        config = Configuration()
        self.cloudant, _, self.db = config.initialize_cloudant_configuration()

    def upload_data(self, metadata, annotation_meta):
        metadata = metadata['doc']
        del metadata['_id']
        del metadata['_rev']
        metadata['user_metadata']['data_details']['annotation_details'] = annotation_meta
        response = self.cloudant.post_document(db=self.db, document=metadata).get_result()
        return response
