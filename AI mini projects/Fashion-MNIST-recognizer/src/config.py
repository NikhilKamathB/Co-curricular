import torch
from easydict import EasyDict 

config = EasyDict()

config.lr = 1e-3
config.momentum = 0.9
config.epochs = 10
config.verbose = True
config.verbose_step = 500
config.test_run = 1
config.patience = 10
config.test_batch_size = 32
config.train_batch_size = 32
config.num_classes = 10
config.model_dir = "./__models__/"
config.save_path_dir = "./__models__/saved_models/"
config.data_dir = "./__data__/fashion_mnist/"
config.device = "cuda" if torch.cuda.is_available() else "cpu"