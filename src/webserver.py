from flask import Flask, request, jsonify, render_template
from main import predict
from tb_api import create_device
import torch
import torch.nn as nn
import torch.utils.data as data_utils
import numpy as np
import sys
import os
from pathlib import Path
import requests
import json


appname = "Driving Style Prediction"
app = Flask(appname)
device = torch.device('cpu')
num_lines_aggressive = sum(1 for line in open('aggressive.txt'))
num_lines_slow = sum(1 for line in open(os.path.join('slow.txt')))
num_lines_normal = sum(1 for line in open(os.path.join('normal.txt')))


# Flask API
# submitting jobs


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return "500 error"


@app.post('/api/v1.0/<serial_n>')
def post_problem(serial_n, methods=['POST']):
    if request.is_json:
        data = request.get_json()
        assert data['gps_id'] is not None
        assert data['imu_id'] is not None
        assert data['co2_id'] is not None
        assert data['predict_id'] is not None
        latitudes = data.pop('Lat')
        longitudes = data.pop('Lon')
        speeds = data.pop('Speed')
        co2 = data.pop('Co2')
        gps_id = data.pop('gps_id')
        imu_id = data.pop('imu_id')
        co2_id = data.pop('co2_id')
        predict_id = data.pop('predict_id')
        AccX = data['AccX']
        AccY = data['AccY']
        AccZ = data['AccZ']
        GyroX = data['GyroX']
        GyroY = data['GyroY']
        GyroZ = data['GyroZ']
        model=torch.load('model.pt')
        model.eval()
        model=model.to(device)
        ret=torch.from_numpy(np.array(list(data.values())))
        ret=ret.to(device)
        pred=torch.argmax(predict(model,ret))
        if pred.item()==0:
            pred_str=str("Normal")
            phrase = open('normal.txt').readlines()[np.random.randint(0, num_lines_normal)]
        elif pred.item()==1:
            pred_str=str("Aggressive")
            phrase = open('aggressive.txt').readlines()[np.random.randint(0, num_lines_aggressive)]
        else:
            pred_str=str("Slow")
            phrase = open('slow.txt').readlines()[np.random.randint(0, num_lines_slow)]
        url = 'https://iot.ing.unimore.it/api/v1/'+str(gps_id)+str('/telemetry')
        url1 = 'https://iot.ing.unimore.it/api/v1/'+str(imu_id)+str('/telemetry')
        url2 = 'https://iot.ing.unimore.it/api/v1/'+str(co2_id)+str('/telemetry')
        url3 = 'https://iot.ing.unimore.it/api/v1/'+str(predict_id)+str('/telemetry')
        data = {'Lat': latitudes, 'Lon': longitudes, 'Speed': speeds} 
        data1= {'AccX': AccX, 'AccY': AccY, 'AccZ': AccZ, 'GyroX': GyroX, 'GyroY': GyroY, 'GyroZ': GyroZ}
        data2= {'Co2': co2}
        data3= {'DrivingStyle': pred.item()}
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers,verify=False)
        r = requests.post(url1, data=json.dumps(data1), headers=headers,verify=False)
        r = requests.post(url2, data=json.dumps(data2), headers=headers,verify=False)
        r = requests.post(url3, data=json.dumps(data3), headers=headers,verify=False)
        return jsonify(id=serial_n,pred=pred_str,frase=phrase), 201
    return {'message': "Request must be JSON"}, 415


@app.route('/create_device', methods=['POST'])
def create_device():
    if request.is_json:
        data=request.get_json()
        assert data is not None
        assert data['username'] is not None
        assert data['password'] is not None
        assert data['asset_name'] is not None
        assert data['imu_name'] is not None
        assert data['gps_name'] is not None
        assert data['co2_name'] is not None
        ret,code=create_device(data['asset_name'],data['imu_name'],data['gps_name'],data['co2_name'])
        if code==500:
            return {'message': "Request must be JSON"}, 500
        else:
            return ret, 201
    return {'message': "Request must be JSON"}, 415
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)