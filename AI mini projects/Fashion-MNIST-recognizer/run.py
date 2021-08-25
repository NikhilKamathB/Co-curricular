import torch
import argparse
import torch.optim as optim
from dotenv import load_dotenv 
from src.config import *
from src.data import *
from src.net import *
from src.train import *
load_dotenv()


def str2bool(v):
    return v.lower() in ("yes", "Yes", "YES", "y", "true", "True", "TRUE", "t", "1")

def main(args=None):
    _data = Data(data_dir=config.data_dir, train_batch_size=config.train_batch_size, test_batch_size=config.test_batch_size)
    if args.display_graphs:
        _data.visualize()
    TRAIN_LOADER, TEST_LOADER = _data.get_loaders()
    MODEL = LeNet5().to(config.device)
    OPTIMIZER = optim.SGD(MODEL.parameters(), lr=config.lr, momentum=config.momentum)
    CRITERION = torch.nn.CrossEntropyLoss()
    SCHEDULER = torch.optim.lr_scheduler.ReduceLROnPlateau(OPTIMIZER, 'min', patience=config.patience)
    training_loss, saved_path = Train(
        model=MODEL,
        train_loader=TRAIN_LOADER,
        optimizer=OPTIMIZER,
        criterion=CRITERION,
        scheduler=SCHEDULER,
        epochs=config.epochs,
        device=config.device,
        save_path_dir=config.save_path_dir,
        verbose=config.verbose,
        verbose_step=config.verbose_step,
        display_graphs=args.display_graphs
    ).train()


if __name__=="__main__":
    # Fetching arguments
    parser = argparse.ArgumentParser(description='Annotate images')
    parser.add_argument('-dg', '--display_graphs', type=str2bool, default='n', metavar="\b", help='Verbosity')
    args = parser.parse_args()
    main(args=args)