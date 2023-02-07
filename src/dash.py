# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException
import json
import requests
from pathlib import Path
#TODO return dashboard id, for customer association(?)

script_path = Path(__file__, '..').resolve()

"""
create a json configuration equal to CarLO_dashboard, with alias single entity of the entity id passed as parameter

devideId: string of the Device Id 

return: a json object
"""
def createConfigDashboard(deviceId): 
    with open(script_path.joinpath("dashConfiguration.json")) as f:
        config = json.load(f)
        config["title"] = f'CarLO Dashboard of device {deviceId}'
        config["configuration"]["entityAliases"]["f2963f99-ab9b-a327-7e2d-f850c012a580"]["filter"]["singleEntity"]["id"] = deviceId
        return config
  
        


"""
 create a CarLO_dashboard given the device id
 api 'saveDashboard' (see https://thingsboard.cloud/swagger-ui/)
 
 devideId: string of the Device Id 

 return: false if http requests failed
"""
def createDashboard(deviceId,tenant_user,tenant_password):
    url = "https://iot.ing.unimore.it"
    username = tenant_user
    password = tenant_password
    
    
    # Creating the REST client object with context manager to get auto token refresh
    with RestClientCE(base_url=url) as rest_client:
        try:
            # Auth with credentials
            rest_client.login(username=username, password=password)
            dashboard_json=createConfigDashboard(deviceId)
            r=requests.post(url+"/api/dashboard",json=dashboard_json,headers={"X-Authorization":"Bearer "+rest_client.token_info.get("token")})
            dashboard_id=r.json()["id"]["id"]
            return dashboard_id, True
        except:
            return False
            