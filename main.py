# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
# import boto3
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#     session = boto3.Session(
#         aws_access_key_id='ASIAU5CJUCXJWISV44XZ',
#         aws_secret_access_key='S5XbI57lswhws1g9U47b3BJty11Mqhux3AX24+Yy',
#     )
#     s3 = session.resource('s3')
#     print(session)
#
#     # s3.Bucket('tagsb00882283').upload_file('C:/Users/RIA/Downloads/20211205_014832.jpg', 'keyfile.jpg')
#     s3.meta.client.upload_file(Filename='C:/Users/RIA/Downloads/20211205_014832.jpg', Bucket='tagsb00882283',
#                                Key='s3_output_key')
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

# import boto3
# from botocore.exceptions import NoCredentialsError
#
# ACCESS_KEY = 'ASIAU5CJUCXJWISV44XZ'
# SECRET_KEY = 'S5XbI57lswhws1g9U47b3BJty11Mqhux3AX24+Yy'
#
#
# def upload_to_aws(local_file, bucket, s3_file):
#     client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,
#                           aws_secret_access_key=SECRET_KEY)
#     s3 = boto3.resource('s3')
#
#     try:
#         s3.upload_file(local_file, bucket, s3_file)
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False
#
#
# uploaded = upload_to_aws('C:/Users/RIA/Downloads/20211205_014832.jpg', 'tagsb00882283', 'image')
import boto3
import botocore.session
from boto3.dynamodb.conditions import Key

# dynamodb = boto3.resource('dynamodb',
                          # aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
#                           aws_secret_access_key='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',
#                           region_name='us-east-1')
#
# client= boto3.client(
#     's3',
#     aws_access_key_id = 'ASIAU5CJUCXJVFIUXPOA',
#     aws_secret_access_key = '/NjU1KLQLcn/mO/tAOJ6b4awdfS72CPvhswB2rDV',
#     region_name = 'us-east-1'
# )
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
session = boto3.Session(
    aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
    aws_secret_access_key='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',
)
session1=session.client('s3')
print(session1)
response = session1.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')
objects=[]
for key in session1.list_objects(Bucket='librarybucket2021')['Contents']:
    print(key['Key'])
    objects.append(key['Key'])
print(objects)


def list_files():
    contents = []
    try:
        response1 = session1.list_objects_v2(Bucket='librarybucket2021')
        if 'Contents' in response1:
            for item in response1['Contents']:
                # print(item)
                contents.append(item)
        else:
            print('Bucket is empty')
    except ClientError as e:
        print(e)

    return contents
# my_bucket = s3.Bucket('')
#
# for file in my_bucket.objects.all():
#     print(file.key)

# table = dynamodb.Table('library_storage')
# response = table.query(
#     KeyConditionExpression=Key('year').eq(2019)
# )
# items = response['Items']
# print(items)
#
# data = response['Items']
# print(response)

# while 'LastEvaluatedKey' in response:
#     response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
#     data.extend(response['Items'])


def download_file(file_name):
    destination = f'download/{file_name}'
    try:
        session1.download_file('librarybucket2021', file_name, destination)
        print('File downloaded successfully')
    except ClientError as e:
        print(e)

    return destination