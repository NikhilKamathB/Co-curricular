import os
import time
import torch
import string
import random
import argparse
import mlflow
import mlflow.pytorch
import torch.optim as optim
from datetime import datetime
from azureml.core import Run
from config import config
from net import LeNet5
from data import Data


class Train:

    def __init__(self, model, train_loader, optimizer, criterion, scheduler, epochs, device, verbose=True, verbose_step=50, run=None, misc=None):
        self.model = model
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.scheduler = scheduler
        self.epochs = epochs
        self.device = device
        self.verbose = verbose
        self.verbose_step = verbose_step
        self.run=run
        self.misc=misc
        self.start_epoch = 0
        self.train_loss = []
        self.save_path = './__outputs__/' + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) + '.pth'
        self.save_log_path = './__output_model_logs__'
    
    def make_model_dir(self):
        if not os.path.exists('./outputs'):
            os.mkdir('./__outputs__')
    
    def save(self):
        torch.save({
            'epoch': self.epochs,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            }, self.save_path)
        print(f"Model saved to -> {self.save_path}")
        if self.misc["mlflow"]:
            mlflow.pytorch.log_model(pytorch_model=self.model, artifact_path=self.save_log_path)

    def train(self):
        self.make_model_dir()
        print(f"\nDEVICE - {self.device} || EPOCHS - {self.epochs} || LEARNING RATE - {self.optimizer.param_groups[0]['lr']}.\n")
        if self.misc["mlflow"]:
            mlflow.log_metric('Learning_rate', float(self.misc["learning_rate"]))
            mlflow.log_metric('momentum', float(self.misc["momentum"]))
        else:
            self.run.log('Learning_rate', float(self.misc["learning_rate"]))
            self.run.log('momentum', float(self.misc["momentum"]))
        self.model.train()
        for epoch in range(self.start_epoch, self.epochs):
            start_epoch_time = time.time()
            if self.verbose:
                _start_at = datetime.now().strftime('%H:%M:%S %d|%m|%Y')
                _lr = self.optimizer.param_groups[0]['lr']
                print(f'\nEPOCH - {epoch+1}/{self.epochs} || START AT - {_start_at} || LEARNING RATE - {_lr}\n')
            running_loss, step_running_loss = 0, 0
            start_step_time = time.time()
            for step, (images, labels) in enumerate(self.train_loader):     
                images, labels = images.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(images)
                loss = self.criterion(output, labels)
                loss.backward()
                self.optimizer.step()
                running_loss += loss.item()
                step_running_loss += loss.item()
                if self.verbose:
                    if (step+1) % self.verbose_step == 0:
                        print(
                            f'\tTrain Step - {step+1}/{len(self.train_loader)} | ' + \
                            f'Train Step Loss: {(step_running_loss/self.verbose_step):.5f} | ' + \
                            f'Time: {(time.time() - start_step_time):.2f}s.\n'
                            )
                        step_running_loss = 0   
                        start_step_time = time.time()
            self.train_loss.append(running_loss/len(self.train_loader))
            self.scheduler.step(running_loss/len(self.train_loader))
            if self.verbose:
                if self.misc["mlflow"]:
                    mlflow.log_metric("Loss", running_loss/len(self.train_loader))
                else:
                    self.run.log('Loss', running_loss/len(self.train_loader))
                print(f'\tEPOCH - {epoch+1}/{self.epochs} || TRAIN LOSS - {(running_loss/len(self.train_loader)):.5f} || TIME ELAPSED - {(time.time() - start_epoch_time):.2f}s.\n')
        self.save()
        return self.train_loss


def main(model, train_loader, optimizer, criterion, scheduler, epochs, device, verbose, verbose_step, run, misc):
    train_loss = Train(
        model=model,
        train_loader=train_loader,
        optimizer=optimizer,
        criterion=criterion,
        scheduler=scheduler,
        epochs=epochs,
        device=device,
        verbose=verbose,
        verbose_step=verbose_step,
        run=run,
        misc=misc
    ).train()

if __name__ == '__main__':
    # fetching arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--learning_rate', type=float, default=config.lr, help='learning rate')
    parser.add_argument('--momentum', type=float, default=config.momentum, help='momentum')
    parser.add_argument('--mlflow', type=bool, default=False, help='using Mlflow?')
    args = parser.parse_args()

    # initializing parameters
    DEVICE = torch.device(config.device)
    _data = Data(train_batch_size=config.train_batch_size, test_batch_size=config.test_batch_size)
    _data.visualize()
    TRAIN_LOADER, _ = _data.get_loaders()
    MODEL = LeNet5().to(DEVICE)
    OPTIMIZER = optim.SGD(MODEL.parameters(), lr=args.learning_rate, momentum=args.momentum)
    CRITERION = torch.nn.NLLLoss()
    SCHEDULER = torch.optim.lr_scheduler.ReduceLROnPlateau(OPTIMIZER, 'min', patience=config.patience)
    RUN = Run.get_context() if not args.mlflow else None

    # running model
    main(
        model=MODEL,
        train_loader=TRAIN_LOADER,
        optimizer=OPTIMIZER,
        criterion=CRITERION,
        scheduler=SCHEDULER,
        epochs=config.epochs,
        device=DEVICE,
        verbose=config.verbose,
        verbose_step=config.verbose_step,
        run=RUN,
        misc={
            'learning_rate': args.learning_rate,
            'momentum': args.momentum,
            'mlflow': args.mlflow
        }
    )
