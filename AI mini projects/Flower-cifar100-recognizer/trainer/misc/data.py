import os
import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import torchvision.transforms as T
from torch.utils.data import Dataset


class FlowersDataset(Dataset):

    def __init__(self, data_dir=None, transform=None):
        super().__init__()
        self.data_dir = data_dir
        self.files = []
        self.classes = [fname for fname in os.listdir(self.data_dir) if '.' not in fname]
        self.classes.sort()
        for classes in self.classes:                         
            for file in os.listdir(self.data_dir + '/' + classes): 
                if file.endswith('jpg'):
                    self.files.append(file)
        self.transform = transform
    
    def __len__(self):
        return len(self.files)

    def __getitem__(self, i):
        fname = self.files[i]
        species = fname.split('_')[0]
        fpath = os.path.join(self.data_dir, species, fname)
        img = self.transform(self.open_image(fpath))
        class_idx = self.classes.index(species)
        return img, class_idx
    
    def open_image(self, path):
        with open(path, 'rb') as f:
            img = Image.open(f)
            return img.convert('RGB')


class Data:

    def __init__(self, resize=64, data_dir=None, data_dir_cifar100=None, transforms=None, train_batch_size=None, test_batch_size=None, is_cifar100=False):
        self.resize = resize
        self.shuffle = True
        self.data_dir = data_dir
        self.data_dir_cifar100 = data_dir_cifar100
        self.is_cifar100 = is_cifar100
        self.stats = ((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
        self.train_batch_size, self.test_batch_size = 32 if train_batch_size is None else train_batch_size, 32 if test_batch_size is None else test_batch_size
        self.transforms = self.get_transforms() if transforms is None or not isinstance(transforms, dict) else transforms

    def get_transforms(self):
        TRANSFORMS = {
            'train': T.Compose([
                T.Resize((self.resize, self.resize)),
                # T.RandomHorizontalFlip(),
                # T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
                T.ToTensor(),
                # T.Normalize(*self.stats,inplace=True)
            ]),
            'test': T.Compose([
                T.Resize((self.resize, self.resize)),
                T.ToTensor(),
                # T.Normalize(*self.stats,inplace=True)
            ])
        }
        return TRANSFORMS

    def get_loaders(self):
        if self.is_cifar100:
            train_loader = torch.utils.data.DataLoader(torchvision.datasets.CIFAR10(self.data_dir_cifar100, train=True, download=True, transform=self.transforms['train']), batch_size=self.train_batch_size, shuffle=self.shuffle)
            test_loader = torch.utils.data.DataLoader(torchvision.datasets.CIFAR10(self.data_dir_cifar100, train=False, download=True, transform=self.transforms['test']), batch_size=self.test_batch_size, shuffle=self.shuffle)
        else:
            train_loader = torch.utils.data.DataLoader(FlowersDataset(self.data_dir, transform=self.transforms['train']), batch_size=self.train_batch_size, shuffle=self.shuffle)
            test_loader = torch.utils.data.DataLoader(FlowersDataset(self.data_dir, transform=self.transforms['test']), batch_size=self.test_batch_size, shuffle=self.shuffle)
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