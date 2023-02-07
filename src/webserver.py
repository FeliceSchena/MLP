from flask import Flask, request, jsonify, render_template
from main import predict
from tb_api import create_all
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
    return "500 error",500


@app.post('/api/v1.0/<serial_n>')
def post_problem(serial_n, methods=['POST']):
    if request.is_json:
        data = request.get_json()
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
        return jsonify(id=serial_n,pred=pred_str,frase=phrase), 201
    return {'message': "Request must be JSON"}, 415


@app.route('/create_device', methods=['POST'])
def create_element():
    if request.is_json:
        data=request.get_json()
        assert data is not None
        assert data['username'] is not None
        assert data['tenant_user_email'] is not None
        assert data['tenant_user_password'] is not None
        access_token,user_id,code=create_all(data['username'],data['tenant_user_email'],data['tenant_user_password'])
        if code==200:
            return jsonify(access_token=access_token,user_id=user_id), code
        else: 
            return jsonify(message="Error while creating user"), 500
    return {'message': "Request must be JSON"}, 415
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)