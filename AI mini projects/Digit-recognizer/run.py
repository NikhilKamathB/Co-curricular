#%%
import sys
sys.path.append('..')

import cv2
import torch
import string
import random
import torch.optim as optim
import config
import numpy as np
from utils import *
from data import Data
from net import LeNet5
from train import Train
from test import Test
from config import config

# %%
DEVICE = torch.device(config.device)
_data = Data(train_batch_size=config.train_batch_size, test_batch_size=config.test_batch_size)
_data.visualize()
TRAIN_LOADER, TEST_LOADER = _data.get_loaders()
MODEL = LeNet5().to(DEVICE)
OPTIMIZER = optim.SGD(MODEL.parameters(), lr=config.lr, momentum=config.momentum)
CRITERION = torch.nn.NLLLoss()
SCHEDULER = torch.optim.lr_scheduler.ReduceLROnPlateau(OPTIMIZER, 'min', patience=config.patience)

# %%
dataiter = iter(TRAIN_LOADER)
images, _ = dataiter.next()
for i in range(images.size(0)):
    image = np.transpose(images[i].numpy(), (1, 2, 0))
    image *= 255.0
    save_path = './data/tmp/' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) + '.png'
    cv2.imwrite(f'{save_path}', image)

# %%
train_loss = Train(
    model=MODEL,
    train_loader=TRAIN_LOADER,
    optimizer=OPTIMIZER,
    criterion=CRITERION,
    scheduler=SCHEDULER,
    epochs=config.epochs,
    device=DEVICE,
    save_path=config.save_path,
    verbose=config.verbose,
    verbose_step=config.verbose_step
).train()

# %%
image_set, label_set, pred_set, model = Test(
    model=MODEL,
    test_loader=TEST_LOADER,
    device=DEVICE,
    save_path=config.save_path,
    test_run=config.test_run
).test()

# %%
plot_output(image_set, label_set, pred_set)
