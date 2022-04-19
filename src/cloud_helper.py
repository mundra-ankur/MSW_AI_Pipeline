import configparser

import ibm_boto3
from ibm_botocore.config import Config
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant import CloudantV1

config = configparser.ConfigParser()
config.read('config/ibm_config.ini')

# Credentials to authenticate COS
cos_credentials = config['cos.credentials.writer']
bucket_upload = config['cos.credentials']['bucket_processed']

# Credentials to authenticate Cloudant
cloudant_credentials = config['cloudant.credentials']

# Create COS client resource
cos_resource = ibm_boto3.resource(service_name='s3',
                                  ibm_api_key_id=cos_credentials['api_key'],
                                  ibm_service_instance_id=cos_credentials['instance_crn'],
                                  config=Config(signature_version="oauth"),
                                  endpoint_url=cos_credentials['service_endpoint']
                                  )

# Create COS client
cos_client = ibm_boto3.client(service_name='s3',
                              ibm_api_key_id=cos_credentials['api_key'],
                              ibm_service_instance_id=cos_credentials['instance_crn'],
                              ibm_auth_endpoint=cos_credentials['auth_endpoint'],
                              config=Config(signature_version='oauth'),
                              endpoint_url=cos_credentials['service_endpoint']
                              )


def get_cos_client():
    return cos_client


def get_cos_resource():
    return cos_resource


def get_upload_bucket():
    return bucket_upload


def get_cloudant_client():
    authenticator = IAMAuthenticator(apikey=cloudant_credentials['api_key'])
    cloudant_client = CloudantV1(authenticator)
    cloudant_client.set_service_url(cloudant_credentials['url'])
    return cloudant_client, cloudant_credentials['db']


def get_cloudant_processed_db():
    return cloudant_credentials['processed_db']
