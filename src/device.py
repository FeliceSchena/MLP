# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException



"""
 create a CarLO device

 params:
    -string name: name of the device, MUST BE UNIQUE

 return: 
    -boolean False: if http requests failed.
    -(string, string): device id, access token.
"""
def createDevice(name,tenant_user,tenant_password):
    url = "https://iot.ing.unimore.it"
    username = tenant_user
    password = tenant_password
    deviceconfig = {
        "name": name,
        "type": "DEVICE",
        "label": "CarLO device",
        "deviceProfileId": {
            "id": '3cb2a570-a63d-11ed-96dc-f9674745d790',
            "entityType": "DEVICE_PROFILE"
        },
        "additionalInfo": {}
    }
    
    # Creating the REST client object with context manager to get auto token refresh
    with RestClientCE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            
            deviceCreated = rest_client.save_device(deviceconfig)
            credentials = rest_client.get_device_credentials_by_device_id(device_id=deviceCreated.id)
            
            deviceId = getIdFromDevice(deviceCreated)
            accessToken = credentials.credentials_id
            
            return deviceId, accessToken
        
        except:
            return False


def getIdFromDevice(device):
    return str(device.id).split(sep='\'')[len(str(device.id).split(sep='\''))-2]    
            
