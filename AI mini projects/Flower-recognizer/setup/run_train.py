import os
import torch
import torch.optim as optim
from . import config, data, net, train


def main():
    os.environ['TORCH_HOME'] = config.config.model_dir_cloud
    DEVICE = torch.device(config.config.device)
    _data = data.Data(data_dir=config.config.data_dir_cloud, train_batch_size=config.config.train_batch_size, test_batch_size=config.config.test_batch_size)
    _data.visualize()
    TRAIN_LOADER, TEST_LOADER = _data.get_loaders()
    MODEL = net.Resnet18().get_model(num_classes=config.config.num_classes).to(DEVICE)
    OPTIMIZER = optim.SGD(MODEL.parameters(), lr=config.config.lr, momentum=config.config.momentum)
    CRITERION = torch.nn.CrossEntropyLoss()
    SCHEDULER = torch.optim.lr_scheduler.ReduceLROnPlateau(OPTIMIZER, 'min', patience=config.config.patience)
    train_loss, saved_path = train.Train(
        model=MODEL,
        train_loader=TRAIN_LOADER,
        optimizer=OPTIMIZER,
        criterion=CRITERION,
        scheduler=SCHEDULER,
        epochs=config.config.epochs,
        device=DEVICE,
        save_path_dir=config.config.save_path_dir_cloud,
        verbose=config.config.verbose,
        verbose_step=config.config.verbose_step
    ).train()


if __name__=="__main__":
    main()