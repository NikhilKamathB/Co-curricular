import os
import torch
import pandas as pd
import torch.optim as optim
from datetime import datetime
from google.cloud import aiplatform
from trainer.misc.config import *
from trainer.misc.data import *
from trainer.misc.net import *
from trainer.misc.train import *


def main():
    print("Making data directory...")
    os.system(f"mkdir -p {config.data_dir_cloud}")
    print("Making model directory...")
    os.system(f"mkdir -p {config.model_dir_cloud}")
    print("Making saved model directory...")
    os.system(f"mkdir -p {config.save_path_dir_cloud}")
    print("List root directories...")
    print(os.listdir('/'))
    print("Listing buckets...")
    os.system("gsutil ls gs://vertexai_bucket")
    print("Downloading data...")
    os.system(f"gsutil -m cp -r gs://vertexai_bucket/datasets/flower_photos/ {config.data_dir_cloud}")
    os.environ['TORCH_HOME'] = config.model_dir_cloud
    DEVICE = torch.device(config.device)
    _data = Data(data_dir=config.data_dir_cloud + "flower_photos/", train_batch_size=config.train_batch_size, test_batch_size=config.test_batch_size)
    TRAIN_LOADER, TEST_LOADER = _data.get_loaders()
    print(f"Length of Train Loader -> {len(TRAIN_LOADER)}\nLength of Test Loader -> {len(TEST_LOADER)}")
    MODEL = Resnet18().get_model(num_classes=config.num_classes).to(DEVICE)
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
        device=DEVICE,
        save_path_dir=config.save_path_dir_cloud,
        verbose=config.verbose,
        verbose_step=config.verbose_step
    ).train()
    print(saved_path)
    df_log = pd.DataFrame({"Training Loss": training_loss})
    df_param = pd.DataFrame({"Epoch": [config.epochs], "Learning Rate": [config.lr]})
    file_name = saved_path.split('/')[-1]
    csv_file_log = file_name.split('.')[0]+'_log.csv'
    csv_file_param = file_name.split('.')[0]+'_param.csv'
    df_log.to_csv(csv_file_log, index=False)
    df_param.to_csv(csv_file_param, index=False)
    os.system(f"gsutil cp {saved_path} gs://vertexai_bucket{config.save_path_dir_cloud}")
    os.system(f"gsutil cp {csv_file_log} gs://vertexai_bucket{config.save_path_dir_cloud}")
    os.system(f"gsutil cp {csv_file_param} gs://vertexai_bucket{config.save_path_dir_cloud}")


if __name__=="__main__":
    main()