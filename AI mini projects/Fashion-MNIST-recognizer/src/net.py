import torch.nn.functional as F
from torch import nn


class LeNet5(nn.Module):

    def __init__(self):
        super(LeNet5, self).__init__()
        self.conv_layer_1 = nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5)
        self.sub_1 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.conv_layer_2 = nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5)
        self.sub_2 = nn.AvgPool2d(kernel_size=2, stride=2)
        self.fc_1 = nn.Linear(in_features=13*13*16, out_features=1024)
        self.fc_2 = nn.Linear(in_features=1024, out_features=512)
        self.fc_3 = nn.Linear(in_features=512, out_features=10)

    def forward(self, x):
        x = self.sub_1(F.relu(self.conv_layer_1(x)))
        x = self.sub_2(F.relu(self.conv_layer_2(x)))
        x = x.view(-1, 13*13*16)
        x = F.relu(self.fc_1(x))
        x = F.relu(self.fc_2(x))
        x = F.log_softmax(self.fc_3(x), dim=1)
        return x