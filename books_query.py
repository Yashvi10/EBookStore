#Author Saloni Raythatha

import boto3
import botocore.session
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAVVCE6YC6T32OQJGM',
                          aws_secret_access_key='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',
                          region_name='us-east-1')

table = dynamodb.Table('library_storage')
response = table.query(
    KeyConditionExpression=Key('year').eq(2019)
)
items = response['Items']
print(items)

data = response['Items']
print(response)

while 'LastEvaluatedKey' in response:
    response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

