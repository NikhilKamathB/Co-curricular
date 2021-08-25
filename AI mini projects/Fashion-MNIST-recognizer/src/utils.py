import os
import wandb
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def display_images(image_set, label_set, pred_set, rows=None, columns=None, wandb_needed=False, wandb_title=None):
    fig = plt.figure(figsize=(17, 25))
    for i in range(1, rows * columns + 1):
        image = np.transpose(image_set[i-1], (1, 2, 0))
        true_val = int(label_set[i-1])
        pred_val = np.argmax(pred_set[i-1])
        fig.add_subplot(rows, columns, i)
        plt.title(f"Actual val = {true_val}\nPredicted val = {pred_val}")
        plt.xticks([])
        plt.yticks([])
        np.clip(image, 0, 1, out=image)
        plt.imshow(image)
    fig.tight_layout(pad=3.0)
    if wandb_needed:
        wandb.log({wandb_title: fig})
    plt.show()

def plot_output(image_set, label_set, pred_set, wandb_needed=False, wandb_title=None):
    for i in range(len(image_set)):
        image = image_set[i].to("cpu").numpy()
        label = label_set[i].to("cpu").numpy()
        pred = pred_set[i].to("cpu").numpy()
        if image.shape[0] % 4 == 0:
            rows, columns = image.shape[0] // 4, 4
            display_images(image, label, pred, rows=rows, columns=columns, wandb_needed=wandb_needed, wandb_title=wandb_title)