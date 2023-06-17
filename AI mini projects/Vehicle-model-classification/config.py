from easydict import EasyDict 


config = EasyDict()

# Data.
config.DATA_DIR_RAW = "../../../data/cars-dataset/"
config.DATA_DIR_RAW_TRAIN = f'{config.DATA_DIR_RAW}/train'
config.DATA_DIR_RAW_TEST = f'{config.DATA_DIR_RAW}/test'

# Data augmentation and related entities.
config.RESIZE = (225, 225)