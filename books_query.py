#Author Saloni Raythatha

import boto3
import botocore.session
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAVVCE6YC6UVS63U5J',
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

