# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException
from json import dumps
import logging
import requests
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')



# Creating the REST client object with context manager to get auto token refresh
def createCustomer(customer_title,deviceId,email,dashboard_id,tenant_user,tenant_password):
    # Default Tenant Administrator credentials
    url = "https://iot.ing.unimore.it"
    username = tenant_user
    password = tenant_password
    parent="38646e00-a49d-11ed-a8d5-e9eba22b9df6"
    
    with RestClientCE(base_url=url) as rest_client:
        # ThingsBoard REST API URL 
        try:
            # Auth with credentials
            rest_client.login(username=username, password=password)
            current_user = rest_client.get_user()
            customer=Customer(title=customer_title,tenant_id=current_user.tenant_id,country="",state="",city="",address="",address2="",zip="",phone="",email=email)
            customer = rest_client.save_customer(customer)
            r=requests.post(url+"/api/customer/"+str(customer.id.id)+"/dashboard/"+dashboard_id,headers={"X-Authorization":"Bearer "+rest_client.token_info.get("token")})
            r=requests.post(url+"/api/customer/"+str(customer.id.id)+"/device/"+deviceId,headers={"X-Authorization":"Bearer "+rest_client.token_info.get("token")})
            return customer.id.id, True
        except ApiException as e:
            logging.exception(e)
