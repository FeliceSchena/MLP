 # Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException
import json
import requests


def createUser(user_email, customerId,tenant_user,tenant_password,dashboard_id):
    url = "https://iot.ing.unimore.it"
    username = tenant_user
    password =tenant_password 

    config = {
        "customerId": {
            "id": customerId,
            "entityType": "CUSTOMER"
        },
        "email": user_email,
        "authority": "CUSTOMER_USER",
        "firstName": "",
        "lastName": "",
        "additional_info": {
                "defaultDashboardId": dashboard_id,
                "defaultDashboardFullscreen": True
            }
    }

    with RestClientCE(base_url=url) as rest_client:
        try:
            rest_client.login(username=username, password=password)
            r=requests.post(url=url+"/api/user?sendActivationMail=false",headers={"X-Authorization":"Bearer "+rest_client.token_info.get("token")}, json= config)
            r1=requests.get( url=url+"/api/user/"+str(r.json()["id"]["id"]+"/activationLink"),headers={"X-Authorization":"Bearer "+rest_client.token_info.get("token")})
            return r.json()['id']['id'],r1.content,r.status_code
        except:
            return False,500