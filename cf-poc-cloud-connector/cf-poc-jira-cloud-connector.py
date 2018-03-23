import os
import requests
import imp

from flask import Flask, make_response, request
from cfenv import AppEnv

# from sap import xssec
# imp.load_source('sapjwt', './sap/xssec/sapjwt/__init__.py')
# imp.load_source('deps', './sap/xssec/sapjwt/deps/__init__.py')
imp.load_source('sapjwt', './sap/xssec/sapjwt/__init__.py')
imp.load_source('xssec', './sap/xssec/__init__.py') 

try:
    env = AppEnv()
    vs_uaa_service_credentials = env.get_service(label='xsuaa').credentials
    vs_connectivity_credentials = env.get_service(label='connectivity').credentials
    vs_destination_credentials = env.get_service(label='destination').credentials

except:
    pass

app = Flask(__name__)

@app.route('/', methods=['GET'])
def call_jira():
    try:
        auth_header = request.headers['Authorization']
    except KeyError:
        return 'Authorization header is missing', 401

    auth_header_parts = auth_header.split(' ')

    if len(auth_header_parts) != 2:
        return 'Authorization header is not correctly formated', 401

    if auth_header_parts[0] != 'Bearer':
        return 'Authorization header is not correctly formated', 401

    # Token comming from the approuter after user is authenticated
    # through the xsuaa service
    jwt_user_auth = auth_header_parts[1]
    # print('jwt_user_auth: ', jwt_user_auth '\n')

    # Decoding of the JWT token
    security_context = xssec.create_security_context(jwt_user_auth, vs_uaa_service_credentials)

    # >>> --- Get JWT from xsuaa service for the DESTINATION service ------------

    response = requests.post(vs_uaa_service_credentials["url"] + '/oauth/token?grant_type=client_credentials', headers={
        'Accept': 'application/json'
    }, auth=(vs_destination_credentials['clientid'], vs_destination_credentials['clientsecret']))

    jwt_destination = response.json()['access_token']
    # print('jwt_destination: ', jwt_destination, '\n')

    # <<< -----------------------------------------------------------------------

    # >>> --- Get destination for on premise service ----------------------------

    try:
        response = requests.get(vs_destination_credentials['uri'] + '/destination-configuration/v1/destinations/', headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + jwt_destination,
        })

        destination = response.json()['destinationConfiguration']
        # print('Destination: ', destination, '\n')

    except Exception as e:
        return "Something wrong reading data from the destination service: " + str(e), 500

    # <<< -----------------------------------------------------------------------  
    
    # >>> --- Get JWT from xsuaa service for the CONNECTIVITY service -----------

    response = requests.post(vs_uaa_service_credentials["url"] + '/oauth/token?grant_type=client_credentials', headers={
        'Accept': 'application/json'
    }, auth=(vs_connectivity_credentials['clientid'], vs_connectivity_credentials['clientsecret']))

    jwt_connectivity = response.json()['access_token']
    # print('jwt_connectivity: ', jwt_connectivity, '\n')

    # <<< -----------------------------------------------------------------------

    # >>> Access the on premise resource through the connectivity proxy
    proxies = {
        'http': vs_connectivity_credentials['onpremise_proxy_host'] + ':' + vs_connectivity_credentials['onpremise_proxy_port'],
    }

    try:
        response = requests.get(destination['URL'] + '/sap/opu/odata/SAP/Z_ASSET_MANAGEMENT_SRV', proxies=proxies, headers={
            'Accept': 'application/json',
            'SAP-Connectivity-Authentication': 'Bearer ' + jwt_user_auth,
            'Proxy-Authorization': 'Bearer ' + jwt_connectivity
        }, auth=(destination['User'], destination['Password']))

        return make_response(response.content, 200, {'Content-Type': response.headers['Content-Type']})

    except Exception as e:
        return "Something wrong accessing on premise resource: " + str(e), 500 

    # <<< --------------------------------------------------------------

    return "How did it reach this code?", 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)