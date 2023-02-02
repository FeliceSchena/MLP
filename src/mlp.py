import torch
import torch.nn as nn

class MLP(nn.Module):
  
  def __init__(self, num_fin: int, num_hidden: int, num_classes: int):
    super(MLP, self).__init__()
    self.net = nn.Sequential(
                    nn.Linear(num_fin, num_hidden),
                    nn.ReLU(),
                    nn.Linear(num_hidden,num_hidden),
                    nn.ReLU(),
                    nn.Linear(num_hidden, num_classes)
    )
  
  def forward(self, x: torch.Tensor):
    x = x.to(torch.float32)
    return self.net(x)