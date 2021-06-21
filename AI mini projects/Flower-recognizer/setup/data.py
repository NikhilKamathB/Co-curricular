import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms


class Data:

    def __init__(self, transforms=None, train_batch_size=None, test_batch_size=None):
        self.resize = 220
        self.root = 'data'
        self.shuffle = True
        self.download = True
        self.mean, self.std = (0.4124234616756439, 0.3674212694168091, 0.2578217089176178), (0.3268945515155792, 0.29282665252685547, 0.29053378105163574)
        self.train_batch_size, self.test_batch_size = 32 if train_batch_size is None else train_batch_size, 32 if test_batch_size is None else test_batch_size
        self.transforms = self.get_transforms() if transforms is None or not isinstance(transforms, dict) else transforms

    def get_transforms(self):
        TRANSFORMS = {
            'train': transforms.Compose([
                transforms.Resize((self.resize, self.resize)),
                transforms.ToTensor(),
                transforms.Normalize(self.mean, self.std)
            ]),
            'test': transforms.Compose([
                transforms.Resize((self.resize, self.resize)),
                transforms.ToTensor(),
                transforms.Normalize(self.mean, self.std)
            ])
        }
        return TRANSFORMS

    def get_loaders(self):
        train_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=True, download=True, transform=self.transforms['train']), batch_size=self.train_batch_size, shuffle=self.shuffle)
        test_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=False, transform=self.transforms['test']), batch_size=self.test_batch_size, shuffle=self.shuffle)
        return train_loader, test_loader
    
    def imshow(self, image):
        npimage = image.numpy()
        plt.imshow(np.transpose(npimage, (1, 2, 0)))
        plt.show()

    def visualize(self):
        trainloader, _ = self.get_loaders()
        dataiter = iter(trainloader)
        images, _ = dataiter.next()
        self.imshow(torchvision.utils.make_grid(images))