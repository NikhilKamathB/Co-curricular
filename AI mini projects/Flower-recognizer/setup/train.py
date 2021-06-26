import time
import torch
import string
import random
from datetime import datetime


class Train:

    def __init__(self, model, train_loader, optimizer, criterion, scheduler, epochs, device, save_path_dir=None, verbose=True, verbose_step=50, run=None, misc=None):
        self.model = model
        self.train_loader = train_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.scheduler = scheduler
        self.epochs = epochs
        self.device = device
        self.save_path_dir = save_path_dir
        self.verbose = verbose
        self.verbose_step = verbose_step
        self.run=run
        self.misc=misc
        self.start_epoch = 0
        self.train_loss = []
        self.save_path = self.save_path_dir + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) + '.pth'
        self.save_log_path = 'model'
    
    def save(self):
        torch.save({
            'epoch': self.epochs,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            }, self.save_path)
        print(f"Model saved to -> {self.save_path}")
    
    def train(self):
        print(f"\nDEVICE - {self.device} || EPOCHS - {self.epochs} || LEARNING RATE - {self.optimizer.param_groups[0]['lr']}.\n")
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
                print(f'\tEPOCH - {epoch+1}/{self.epochs} || TRAIN LOSS - {(running_loss/len(self.train_loader)):.5f} || TIME ELAPSED - {(time.time() - start_epoch_time):.2f}s.\n')
        self.save()
        return self.train_loss, self.save_path