#Author Saloni Raythatha

import boto3
import botocore.session
from boto3.dynamodb.conditions import Key

from flask import Flask, render_template, redirect, url_for, request
import boto3

app=Flask(__name__)

# # displaying image content from s3 bucket
#
# client= boto3.client(
#     's3',
#     aws_access_key_id = 'AKIAVVCE6YC6UVS63U5J',
#     aws_secret_access_key = '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',
#     region_name = 'us-east-1'
# )
# s3 = boto3.resource('s3')
# session = boto3.Session(
#     aws_access_key_id="AKIAVVCE6YC6UVS63U5J",
#     aws_secret_access_key="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",
# )
# session1=session.client('s3')
# print(session1)
# response = session1.list_buckets()
#
# # Output the bucket names
# print('Existing buckets:')
# for bucket in response['Buckets']:
#     print(f'  {bucket["Name"]}')
#
# for key in session1.list_objects(Bucket='librarybucket2021')['Contents']:
#     print(key['Key'])
#
#
#
#
#
#
#
# # connecting all dynamo db connect to website
#
# def list_files():
#     # contents = []
#     # response1 = session1.list_objects_v2(Bucket='tagsb00882283')
#     # for image in response1.objects.all():
#     #     contents.append(image.key)
#     # return contents
#     contents = []
#     try:
#         response1 = session1.list_objects_v2(Bucket='librarybucket2021')
#         if 'Contents' in response1:
#             for item in response1['Contents']:
#                 # print(item)
#                 contents.append(item)
#         else:
#             print('Bucket is empty')
#     except ClientError as e:
#         print(e)
#
#     return contents
#
#
# @app.route('/', methods=['GET', 'POST'])
# def files():
#     list_of_files = list_files()
#     return render_template('welcome.html', my_bucket='tagsb00882283', list_of_files=list_of_files)
#
#
#
