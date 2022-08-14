from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError
import sys
import logging
import os
import argparse

def get_filepath(dir_path, list_name):
    for file in os.listdir(dir_path): 
        file_path = os.path.join(dir_path, file)
        if os.path.isdir(file_path):
            get_filepath(file_path, list_name)
        else:
            list_name.append(file_path)
    return list_name

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

parser = argparse.ArgumentParser()
parser.add_argument('secret_id', type=str, help='用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi')
parser.add_argument('secret_key', type=str, help='用户的 SecretId，请登录访问管理控制台进行查看和管理，https://console.cloud.tencent.com/cam/capi')
parser.add_argument('region', type=str, help='用户的 region，已创建桶归属的region可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket')
parser.add_argument('bucket', type=str, help='用户的 bucket，已创建桶的可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket')
args = parser.parse_args()

secret_id = args.secret_id
secret_key = args.secret_key
region = args.region
bucket = args.bucket

config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

os.chdir(os.getcwd() + '/source/')

path = 'images/'
files = get_filepath(path, [])
for file in files:
    file = file.replace('\\', '/')
    print(file)
    response = client.object_exists(
        Bucket=bucket,
        Key=file)
    if response:
        continue
    for i in range(0, 10):
        try:
            response = client.upload_file(
                Bucket=bucket,
                Key=file,
                LocalFilePath=file)
            break
        except CosClientError or CosServiceError as e:
            print(e)

