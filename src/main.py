import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.utils.data as data_utils
from torch.utils.data import DataLoader
import os
from argparse import ArgumentParser
from mlp import MLP
from sklearn import preprocessing
from pathlib import Path

number_workers = 0
epochs=100
batch_size = 64
validation_size = 0.039
device = torch.device('cpu')
learning_rate = 0.01
MLP_criterion = nn.CrossEntropyLoss().to(device)



def eval_acc(mlp: nn.Module, data_loader: torch.utils.data.DataLoader, 
             device: torch.device):

  correct = 0
  total = 0
  
  with torch.no_grad():
    for x, y in data_loader:
      y=y.type(torch.float64)
      x, y = x.to(device), y.to(device)
      y_pred = mlp(x)
      y_pred_discr = torch.argmax(y_pred, dim=1)
      acc = torch.sum((y_pred_discr == y).float()) 
      correct += acc
      total += y_pred.size(0) 
  return correct/total 


def fit(data):
        pathdir = Path.cwd()
        Path(pathdir).parent
        df=pd.read_csv(os.path.join(str(Path(pathdir).parent)+'\\datasets',data))
        Y=np.array(df.pop('Class'))
        df=df.drop('Timestamp',axis=1)
        X=np.array(df.values)
        X=preprocessing.normalize(X)
        train_dataset = torch.utils.data.TensorDataset(torch.from_numpy(X), torch.from_numpy(Y))
        train_set_size = int(len(X) * 0.8)
        test_set_size = len(X) - train_set_size
        train_set, test_set = data_utils.random_split(train_dataset, [train_set_size, test_set_size])
        train_loader_batch=DataLoader(train_set,batch_size=batch_size,num_workers=number_workers,shuffle=True,drop_last=False)
        testing_loader_batch = DataLoader(test_set, batch_size = batch_size, num_workers = number_workers,shuffle=False,drop_last=False)
        MLP_model=MLP(6,4,3).to(device)
        Model_optimizer = torch.optim.SGD(MLP_model.parameters(),lr =learning_rate)
        for epoch in range(epochs):
          print(f"Epoch {epoch} train acc.: {eval_acc(MLP_model, train_loader_batch, device):.3f} "
                        f"test acc.: {eval_acc(MLP_model, testing_loader_batch, device):.3f}")
          for data,label in train_loader_batch:
            Model_optimizer.zero_grad()
            out=MLP_model(data)
            loss=MLP_criterion(out,label)
            loss.backward()
            Model_optimizer.step()
        return MLP_model


def predict(model,data):
  return model(data)

if __name__=="__main__":
    parser = ArgumentParser()
    parser.add_argument('-data', type=str, default='train_motion_data.csv')
    parser.add_argument('-save', type=bool, default=False)
    parser.add_argument('-file', type=str, default='model.pt')
    parser.add_argument('-fit', type=bool, default=False)
    parser.add_argument('-predict', type=bool, default=False)
    parser.add_argument('-x', type=str, default='x_test.csv')
    args=parser.parse_args()
    if args.fit==True:
        model=fit(args.data)
        if args.save==True:
            torch.save(model, args.file)
    if args.predict==True and args.fit==False:
        model=torch.load(args.file)
        model.eval()
        predict(model, args.data)
    elif args.predict==True and args.fit==True:
      model=fit(args.data)
      predict(model, args.data)
      if args.save==True:
        torch.save(model, args.file)

        