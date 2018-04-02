import boto3
import decimal
import base64
import json
import datetime
import os
import urllib
import logging

from urllib import request, parse
from io import BytesIO
from boto3.dynamodb.conditions import Key, Attr


TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/$$$$$$$$$$/Messages.json"
TWILIO_ACCOUNT_SID = "$$$$$$$$$$$$$"
TWILIO_AUTH_TOKEN = "$$$$$$$$$$$$$$"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    '''
    logger.info(event['device'])
    logger.info(event['room_temperature'])
    logger.info(event['out_temperature'])
    '''
    
    def sendText(msg):
        to_number = +353852768444
        from_number = +353861801376
        body = msg
     
        if not TWILIO_ACCOUNT_SID:
            return "Unable to access Twilio Account SID."
        elif not TWILIO_AUTH_TOKEN:
            return "Unable to access Twilio Auth Token."
        elif not to_number:
            return "The function needs a 'To' number in the format +12023351493"
        elif not from_number:
            return "The function needs a 'From' number in the format +19732644156"
        elif not body:
            return "The function needs a 'Body' message to send."
     
        # insert Twilio Account SID into the REST API URL
        populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
        post_params = {"To": to_number, "From": from_number, "Body": body}
     
        # encode the parameters for Python's urllib
        data = parse.urlencode(post_params).encode()
        req = request.Request(populated_url)
     
        # add authentication header to request based on Account SID + Auth Token
        authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        base64string = base64.b64encode(authentication.encode('utf-8'))
        req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
     
        try:
            # perform HTTP POST request
            with request.urlopen(req, data) as f:
                print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
        except Exception as e:
            # something went wrong!
            return e
     
        return "SMS sent successfully!"
        
    
    
    #Enter the value for persistance
    dynamodb = boto3.client('dynamodb', region_name='eu-west-1')
    
    if event['device'] == 1:
        device_id = str(event['device'])
        reading = str(event['room_temperature'])
        out_temp = str(event['out_temperature'])
        dynamodb.put_item(TableName='compare', Item={'device':{'S':device_id},'key2':{'N':reading}})
        dynamodb.put_item(TableName='compare', Item={'device':{'S':"out_temp"},'key2':{'N':out_temp}})
    
    elif event['device'] == 2:
        device_id = str(event['device'])
        reading = str(event['room_temperature'])
        dynamodb.put_item(TableName='compare', Item={'device':{'S':device_id},'key2':{'N':reading}})

    
    
    response_dev_1 = dynamodb.get_item(TableName='compare', Key={'device':{'S':"1"}})
    response_dev_2 = dynamodb.get_item(TableName='compare', Key={'device':{'S':"2"}})
    response_out_temp = dynamodb.get_item(TableName='compare', Key={'device':{'S':"out_temp"}})
    
    response_dev_1_float = float(response_dev_1['Item']['key2']['N'])
    response_dev_2_float = float(response_dev_2['Item']['key2']['N'])
    response_out_temp_float = float(response_out_temp['Item']['key2']['N'])
    
    # Analyze the inter-room difference
    response_counter = dynamodb.get_item(TableName='compare', Key={'device':{'S':"counter"}})
    response_counter_int = int(response_counter['Item']['key2']['S'])
    
    
    if abs(response_dev_1_float - response_dev_2_float) > 5 :
        response_counter_int = response_counter_int + 1
        if response_counter_int < 3 :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter"},'key2':{'S':str(response_counter_int)}})
        else :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter"},'key2':{'S':str(0)}})
            sendText('Difference in Room temperatures Room1: ' + str(response_dev_1_float) + ' Room2: ' + str(response_dev_2_float))
            
    
    
    
    # Analyze the room1-outside difference
    response_counter2 = dynamodb.get_item(TableName='compare', Key={'device':{'S':"counter2"}})
    response_counter2_int = int(response_counter['Item']['key2']['S'])
    
    if abs(response_dev_1_float - response_out_temp_float) < 20 :
        response_counter2_int = response_counter2_int + 1
        if response_counter_int < 2 :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter2"},'key2':{'S':str(response_counter2_int)}})
        else :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter2"},'key2':{'S':str(0)}})
            sendText('Room temperature is less Room1: ' + str(response_dev_1_float) + ' Outside temperature: ' + str(response_out_temp_float))
    
    
    
    # Analyze the room2-outside difference
    response_counter3 = dynamodb.get_item(TableName='compare', Key={'device':{'S':"counter3"}})
    response_counter3_int = int(response_counter['Item']['key2']['S'])
    
    if abs(response_dev_2_float - response_out_temp_float) < 20 :
        response_counter3_int = response_counter3_int + 1
        if response_counter_int < 2 :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter3"},'key2':{'S':str(response_counter3_int)}})
        else :
            dynamodb.put_item(TableName='compare', Item={'device':{'S':"counter3"},'key2':{'S':str(0)}})
            sendText('Room temperature is less Room2: ' + str(response_dev_2_float) + ' Outside temperature: ' + str(response_out_temp_float))
    
    
    '''
    #reading_float = float(response['Item']['key2']['N'])
    #if reading_float == 20 :
     
    '''
    '''
    to_number = +353852768444
    from_number = +353861801376
    body = event['val']
 
    if not TWILIO_ACCOUNT_SID:
        return "Unable to access Twilio Account SID."
    elif not TWILIO_AUTH_TOKEN:
        return "Unable to access Twilio Auth Token."
    elif not to_number:
        return "The function needs a 'To' number in the format +12023351493"
    elif not from_number:
        return "The function needs a 'From' number in the format +19732644156"
    elif not body:
        return "The function needs a 'Body' message to send."
 
    # insert Twilio Account SID into the REST API URL
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    post_params = {"To": to_number, "From": from_number, "Body": body}
 
    # encode the parameters for Python's urllib
    data = parse.urlencode(post_params).encode()
    req = request.Request(populated_url)
 
    # add authentication header to request based on Account SID + Auth Token
    authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))
 
    try:
        # perform HTTP POST request
        with request.urlopen(req, data) as f:
            print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
    except Exception as e:
        # something went wrong!
        return e
 
    return "SMS sent successfully!"
    '''
    
    
    '''
    Upload to S3 bucket
    s3 = boto3.resource('s3')
    #plt.savefig(img_data, format='png')
    data = 'MY BASE64-ENCODED STRING'
    img_data = base64.b64encode(bytes('your string', 'utf-8'))
    
    bucket = s3.Bucket('storetemperaturegraph')
    #bucket.upload_file('output2.csv', key)
    fileName = "new_name"
    bucket.put_object(Body=img_data, ContentType='image/png', Key=fileName)
    '''
    
    '''
    Code to get visualization 
    
    now = datetime.datetime.now()
    formatted_date = str(now.day)+'-'+str(now.month)+'-'+str(now.year)
    response = table.scan(
        FilterExpression = Attr('split_date').eq('15-3-2018')
    )
    
    
    
    df = pd.DataFrame()
    Time = []
    Celcius = []
    Farenheit = []
    
    for i in response['Items']:
        Time.append(i['split_time'])
        Celcius.append(i['room_temperature'])
        Farenheit.append(i['outside_temperature'])
        
    df['Time'] = Time
    df['Celcius'] = Celcius
    df['Farenheit'] = Farenheit
    
    print (df)
    
    ret = "worked"
    return ret
    '''
    