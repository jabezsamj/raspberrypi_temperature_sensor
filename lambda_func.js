'use strict'

const AWS = require('aws-sdk');
const request = require('request');
const docClient= new AWS.DynamoDB.DocumentClient({region: 'eu-west-1'});


exports.handler = (event, context, callback) => {
    
    
    function addValue(out_temp)
    {
        var date_now = new Date();
        var formatted_date = date_now.getDate()+'-'+(date_now.getMonth()+1)+'-'+date_now.getFullYear();
        var formatted_time = date_now.getHours()+':'+date_now.getMinutes()+':'+date_now.getSeconds();
        var params = {
            TableName: 'temperature',
            Item: {
                date: Date.now(),
                split_date: formatted_date,
                split_time: formatted_time,
                room_temperature: event.Temperature,
                outside_temperature: out_temp
            }
        };
        
        docClient.put(params, function(err, data){
            if(err){
                callback(err, null);
            }else{
                callback(null, data);
            }
        
        });
    }
    
    request({
    url: 'http://api.openweathermap.org/data/2.5/weather?lat=53.415195&lon=-6.388535&appid=',
    method: 'GET',
    headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
    }
    }, function (error, response, body) {
    if (!error && response.statusCode == 200) {
    var jsonResponse = JSON.parse(body); // turn response into JSON
    var out_temp_kelvin = parseInt(jsonResponse.main.temp);
    var out_temp = out_temp_kelvin-273.15;
    console.log(out_temp);
    addValue(out_temp);
    }
    });


}