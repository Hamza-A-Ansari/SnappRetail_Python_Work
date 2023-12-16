import boto3
from boto3.s3.transfer import S3Transfer
import pandas as pd
import logging


def load(output_filename):
    df = pd.read_csv(output_filename)
    logging.info("Now started Loading in s3")
    client = boto3.client('s3')
    region='ap-southeast-1'
    bucket_name='snapp-olap'

    bucket_location = client.get_bucket_location(Bucket=bucket_name)
    url = "https://{1}.s3.{0}.amazonaws.com/{2}".format(bucket_location['LocationConstraint'], bucket_name, 'Snapp-Product-Backup')

    client = boto3.client('s3')
    transfer = S3Transfer(client)

    transfer.upload_file(output_filename, bucket_name, f'Snapp-Product-Backup/{output_filename}')
    logging.info("File uploaded in s3 bucket")

    file_url = '%s/%s/%s' % (client.meta.endpoint_url, bucket_name, f'Snapp-Product-Backup/{output_filename}')
    return file_url, url
