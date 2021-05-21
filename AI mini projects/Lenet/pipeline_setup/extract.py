import os
import torch
import numpy as np
from easydict import EasyDict 

if __name__=='__main__':
    print("If you see this text/message, it means that the execution has happened successfully")
    print(f"Current working directory -> {os.getcwd()}")
    print(f"List of files in the current working directory ->\n{os.listdir(os.getcwd())}")