import os
import numpy as np
import matplotlib.pyplot as plt

def rename_files(data_dir=None):
    classes = [fname for fname in os.listdir(data_dir) if '.' not in fname]
    for classes in classes:
        for file in os.listdir(data_dir + '/' + classes): 
            if file.endswith('jpg'):
                os.rename((data_dir + '/' + classes + '/' + file), (data_dir + '/' + classes + '/' + classes + "_" + file))

def display_images(image_set, label_set, pred_set, rows=None, columns=None):
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
    plt.show()

def plot_output(image_set, label_set, pred_set):
    for i in range(len(image_set)):
        image = image_set[i].to("cpu").numpy()
        label = label_set[i].to("cpu").numpy()
        pred = pred_set[i].to("cpu").numpy()
        if image.shape[0] % 4 == 0:
            rows, columns = image.shape[0] // 4, 4
            display_images(image, label, pred, rows=rows, columns=columns)