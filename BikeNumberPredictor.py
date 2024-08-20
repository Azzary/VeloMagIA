import torch
import torch.nn as nn

class BikeNumberPredictor(nn.Module):
    def __init__(self, input_dim):
        super(BikeNumberPredictor, self).__init__()
        self.layer1 = nn.Linear(input_dim, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.relu(self.layer2(x))
        x = self.layer3(x)
        x = self.sigmoid(x) * 20
        return x

class AsymmetricMSELoss(nn.Module):
    def __init__(self, beta=1.2):
        super(AsymmetricMSELoss, self).__init__()
        self.beta = beta

    def forward(self, pred, target):
        loss = torch.where(pred > target, 
                           self.beta * (pred - target) ** 2,
                           (pred - target) ** 2)
        return loss.mean()