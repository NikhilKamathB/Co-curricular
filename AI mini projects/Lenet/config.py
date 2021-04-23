from easydict import EasyDict 

config = EasyDict()

config.seed = 2021
config.lr = 1e-3
config.batch_size = 32
config.verbose = True
config.verbose_step = 50
config.test_run = 1