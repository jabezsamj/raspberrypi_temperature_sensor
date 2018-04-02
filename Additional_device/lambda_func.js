'use strict'

const AWS = require('aws-sdk');
const request = require('request');
const docClient= new AWS.DynamoDB.DocumentClient({region: 'eu-west-1'});
const lambda = new AWS.Lambda({region: 'eu-west-1'});


exports.handler = (event, context, callback) => {
    
        var device_id = "2"
        var room_temperature = event.Temperature;
        var date_now = new Date();
        var formatted_date = date_now.getDate()+'-'+(date_now.getMonth()+1)+'-'+date_now.getFullYear();
        var formatted_time = date_now.getHours()+':'+date_now.getMinutes()+':'+date_now.getSeconds();
        var params = {
            TableName: 'device_new',
            Item: {
                date: Date.now(),
                split_date: formatted_date,
                split_time: formatted_time,
                room_temperature: 25
            }
        };
        
        docClient.put(params, function(err, data){
            if(err){
                callback(err, null);
            }else{
                callback(null, data);
            }
        
        });
        
        
        
        var params = {
        FunctionName: 'query_and_graph', 
        Payload: '{"device" :'+ device_id + ', "room_temperature" :' + room_temperature + '}'
        };
        
        console.log(params);
        lambda.invoke(params, function(err, data) {
        if (err) console.log(err, err.stack);
        else     console.log(data);         
        });
        

}