import boto3
import botocore.session
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
                          aws_secret_access_key='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',
                          region_name='us-east-1')

client= boto3.client(
    's3',
    aws_access_key_id = 'AKIAVVCE6YC6UVS63U5J',
    aws_secret_access_key = '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',
    region_name = 'us-east-1'
)
s3 = boto3.resource('s3')
session = boto3.Session(
    aws_access_key_id="AKIAVVCE6YC6UVS63U5J",
    aws_secret_access_key="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",
)
session1=session.client('s3')
print(session1)
response = session1.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
    print(f'  {bucket["Name"]}')

for key in session1.list_objects(Bucket='librarybucket2021')['Contents']:
    print(key['Key'])
