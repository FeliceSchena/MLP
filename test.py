import requests
import json
import numpy as np
#make 30 post request to localhost 8080 with random id and array of json data with 6 features with random values
for i in range(30):
    url = 'http://localhost:8080/api/v1.0/'+str(i)
    data = {'AccX': np.random.randint(0,100), 'AccY': np.random.randint(0,100), 'AccZ': np.random.randint(0,100), 'GyroX': np.random.randint(0,100), 'GyroY': np.random.randint(0,100), 'GyroZ': np.random.randint(0,100)}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.status_code)
    print(r.text)
