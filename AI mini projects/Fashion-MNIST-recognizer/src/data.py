import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms as T


class Data:

    def __init__(self, resize=64, data_dir=None, transforms=None, train_batch_size=None, test_batch_size=None, is_cifar100=False):
        self.resize = resize
        self.shuffle = True
        self.data_dir = data_dir
        self.is_cifar100 = is_cifar100
        self.train_batch_size, self.test_batch_size = 32 if train_batch_size is None else train_batch_size, 32 if test_batch_size is None else test_batch_size
        self.transforms = self.get_transforms() if transforms is None or not isinstance(transforms, dict) else transforms

    def get_transforms(self):
        TRANSFORMS = {
            'train': T.Compose([
                T.Resize((self.resize, self.resize)),
                T.ToTensor()
            ]),
            'test': T.Compose([
                T.Resize((self.resize, self.resize)),
                T.ToTensor()
            ])
        }
        return TRANSFORMS

    def get_loaders(self):
        train_loader = torch.utils.data.DataLoader(torchvision.datasets.FashionMNIST(self.data_dir, train=True, download=True, transform=self.transforms['train']), batch_size=self.train_batch_size, shuffle=self.shuffle)
        test_loader = torch.utils.data.DataLoader(torchvision.datasets.FashionMNIST(self.data_dir, train=False, download=True, transform=self.transforms['test']), batch_size=self.test_batch_size, shuffle=self.shuffle)
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