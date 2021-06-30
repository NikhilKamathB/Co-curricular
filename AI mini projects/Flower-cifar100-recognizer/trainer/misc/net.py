import torchvision
from torch import nn


class Resnet18:

    def __init__(self):
        pass

    def get_model(self, pretrained=True, progress=True, num_classes=5):
        model_ft = torchvision.models.resnet18(pretrained=pretrained, progress=progress) 
        num_ftrs = model_ft.fc.in_features
        model_ft.fc = nn.Linear(num_ftrs, num_classes)
        return model_ft