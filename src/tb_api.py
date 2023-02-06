import dash
import device
import customer
import user
import json
def create_all(username,tenant_user_email,tenant_user_password):
    deviceName = 'device_'+str(hash(user_name))
    user_name = username
    customerName = 'customer_'+str(hash(user_name))
    tenant_user=tenant_user_email
    tenant_password=tenant_user_password
    try:

        # 1) creating device; 1b) retrieving id and access token
        deviceId, accesstoken = device.createDevice(deviceName,tenant_user=tenant_user,tenant_password=tenant_password)
        # 2) creating dashboard
        dashboard_id,dashboard_state = dash.createDashboard(deviceId,tenant_user=tenant_user,tenant_password=tenant_password)

        # 3) Create a customer
        customer,customer_state = customer.createCustomer(customerName,deviceId,user_name,tenant_user=tenant_user,tenant_password=tenant_password,dashboard_id=dashboard_id)

        # 4) Create a user and assign dashboard to user
        user,link,user_state = user.createUser(user_name,customer,tenant_user=tenant_user,tenant_password=tenant_password,dashboard_id=dashboard_id)
        return json.dumps({"access_token":accesstoken,"link":link}),200
    except:
        return json.dumps({"error":"error"}),500
