import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url="http://localhost:8000")
    table = dynamodb.Table('temperature')
    
    response = table.query(
        KeyConditionExpression=Key('split_date').eq(5-3-2018)
    )
    
    var result = null
    for i in response['Items']:
        result = i['year'], ":", i['title']
        print(i['year'], ":", i['title'])
    
    return result