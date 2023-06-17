import os
import pandas as pd


def get_data(data_dir: str):
    df = pd.DataFrame()
    classes = os.listdir(data_dir)
    for class_memeber in classes:
        images = os.listdir(f'{data_dir}/{class_memeber}')
        for image in images:
            df = df.concat({
                'image': image,
                'class': class_memeber
            }, ignore_index=True)
    return df