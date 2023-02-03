import logging
# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
url = "https://iot.ing.unimore.it/"
# Default Tenant Administrator credentials
def create_device(username,password,asset_name, imu_name,gps_name,co2_name):
    with RestClientCE(base_url=url) as rest_client:
        try:
            # Auth with credentials
            rest_client.login(username=username, password=password)

            # Creating an Asset
            asset = Asset(name=asset_name, type="IoT Device")
            asset = rest_client.save_asset(asset)

            logging.info("Asset was created:\n%r\n", asset)

            # creating a Device
            device = Device(name=imu_name, type="Imu")
            device = rest_client.save_device(device)
            device1 = Device(name=gps_name, type="Gps")
            device1 = rest_client.save_device(device1)
            device2 = Device(name=co2_name, type="Co2")
            device2 = rest_client.save_device(device2)

            logging.info(" Devices was created:\n%r, %r, %r\n", device,device1,device2)

            # Creating relations from device to asset
            relation = EntityRelation(_from=asset.id, to=device.id, type="Contains")
            relation1 = EntityRelation(_from=asset.id, to=device1.id, type="Contains")
            relation2 = EntityRelation(_from=asset.id, to=device2.id, type="Contains")
            relation = rest_client.save_relation(relation)
            relation1 = rest_client.save_relation(relation1)
            relation2 = rest_client.save_relation(relation2)

            logging.info(" Relation was created:\n%r\n", relation)
        except ApiException as e:
            return "Error 500",500