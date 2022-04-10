import json

import ibm_boto3
from ibm_botocore.config import Config
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibmcloudant import CloudantV1


def initialize_cos_configuration():
    ibm_config = open('config/ibm_config.json')
    config = json.load(ibm_config)
    cos_credentials = config['cos']
    api_key = cos_credentials['apikey']
    service_instance_id = cos_credentials['resource_instance_id']
    auth_endpoint = cos_credentials['auth_endpoint']
    service_endpoint = cos_credentials['service_endpoint']
    bucket = cos_credentials['bucket']

    cos_client = ibm_boto3.client(service_name='s3',
                                  ibm_api_key_id=api_key,
                                  ibm_service_instance_id=service_instance_id,
                                  ibm_auth_endpoint=auth_endpoint,
                                  config=Config(signature_version='oauth'),
                                  endpoint_url=service_endpoint)
    ibm_config.close()
    return cos_client, bucket


def initialize_cloudant_configuration():
    ibm_config = open('config/ibm_config.json')
    config = json.load(ibm_config)
    cloudant = config['cloudant']
    authenticator = IAMAuthenticator(apikey=cloudant['apikey'])
    cloudant_client = CloudantV1(authenticator)
    cloudant_client.set_service_url(cloudant['url'])
    ibm_config.close()
    return cloudant_client, cloudant['db'], cloudant['processed_db']