const http = require('http');
const request = require('request');
const express = require('express');
const path = require('path');
const app = express();

app.get('/', (req, res) => {
    console.log('>>>>>>>>>>>>>>>>> Hello World >>>>>>>>>>>>>>>>>>>>>>');

    request({
        // url: serviceURL + '/sap/opu/odata/SAP/Z_ASSET_MANAGEMENT_SRV/orderSet?$format=json',
        url: '/service/sap/opu/odata/SAP/Z_ASSET_MANAGEMENT_SRV/orderSet?$format=json',
        headers: {
            'Authorization': 'Basic TFVIQU5JV0FMOmUyZGhzZWFzaHVAQUtMJA==',
            'X-CSRF-Token': 'Fetch'
        }
    }, (error, response, body) => {
        /*if (!error && response.statusCode == 200) {
            // csrfToken = response.headers['x-csrf-token'];
            // console.log('CSRF Token: ' + csrfToken);
            console.log('Error: ---------------------------> ', JSON.stringify(error));
            console.log('Response: -------------------------> ', JSON.stringify(response));
            console.log('Body:------------------------> ', JSON.stringify(body));
            // res.json(body);
            // bot.sendMessage(msg.chat.id, 'Error: ' + error);
            // bot.sendMessage(msg.chat.id, 'Response: ' + response);
            // bot.sendMessage(msg.chat.id, 'Body: ' + body);
        } else {
            console.log('If error occurs, then the Error: ------------------> ', JSON.stringify(error));
            console.log('If error occurs, then the Response: ---------------> ', JSON.stringify(response));
            console.log('If error occurs, then the Body: ->>>>>>>>>>>>>>>>>>>> ', JSON.stringify(body));
        }*/
        console.log('If error occurs, then the Error: ------------------> ', JSON.stringify(error));
            console.log('If error occurs, then the Response: ---------------> ', JSON.stringify(response));
            console.log('If error occurs, then the Body: ->>>>>>>>>>>>>>>>>>>> ', JSON.stringify(body));
    });
});

app.listen(process.env.PORT || 3000, () => {
    // console.log('App running on port 3000');
});