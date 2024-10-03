####################################################################################################
# Define utils here - Utils are functions that are used across the application.
####################################################################################################

import os
import cv2
import numpy as np
import pandas as pd
from typing import List
from eyepopai.core.decorators import validate_file
from eyepopai.core.constants import VIDEO_TYPES, IMAGE_TYPES, FileTypes
from eyepopai.core.validators import BaseObjectModel, ImageProcessModel, VideoProcessModel


@validate_file(VIDEO_TYPES)
def view_video(file_path: str, title: str = "Video") -> None:
    """
        View a video.
        Input:
            file_path (str): The path to the video.
            title (str): The title of the video window.
        Returns:
            None
    """
    video = cv2.VideoCapture(file_path)
    if not video.isOpened():
        raise RuntimeError(f"Failed to open video: {file_path}")
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        cv2.imshow(title, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

@validate_file(IMAGE_TYPES)
def view_image(file_path: str, title: str = "Image") -> None:
    """
        View an image.
        Input:
            file_path (str): The path to the image.
            title (str): The title of the image window.
        Returns:
            None
    """
    img = cv2.imread(file_path)
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

def get_file_type(file_path: str) -> str:
    """
        Get the file type of a file.
        Input:
            file_path (str): The path to the file.
        Returns:
            str: The file type.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() in VIDEO_TYPES:
        return FileTypes.VIDEO.value
    elif file_extension.lower() in IMAGE_TYPES:
        return FileTypes.IMAGE.value
    else:
        raise ValueError(f"Invalid file type: {file_extension}")
    
def draw_on_frame(img: np.ndarray, objects: List[BaseObjectModel] = None, offset_x: int = 10, offset_y: int = 10) -> np.ndarray:
    """
        Draw on a frame -> bounding boxes, text, etc.
        Input:
            img (np.ndarray): The image to draw on.
            objects (List[BaseObjectModel]): The list of objects detected.
            offset_x (int): The x-offset for the text.
            offset_y (int): The y-offset for the text.
        Returns:
            np.ndarray: The new annotated image.
    """
    if not objects: return img
    for obj in objects:
        x, y, w, h = int(obj.x), int(obj.y), int(obj.width), int(obj.height)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, f"{obj.classLabel} {obj.classId} - {obj.confidence:.2f}", (x+offset_x, y-offset_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    return img

def draw_on_image(file_path: str, image_process_model: ImageProcessModel, output_dir: str = "./data/output") -> str:
    """
        Draw on an image.
        Input:
            file_path (str): The path to the image.
            image_process_model (ImageProcessModel): The image processing model.
        Returns:
            str: The path to the new annotated image.
    """
    img = cv2.imread(file_path)
    img = draw_on_frame(img, image_process_model.objects)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    cv2.imwrite(output_path, img)
    return output_path

def draw_on_video(file_path: str, video_process_model: VideoProcessModel, output_dir: str = "./data/output") -> str:
    """
        Draw on a video.
        Input:
            file_path (str): The path to the video.
            video_process_model (VideoProcessModel): The video processing model.
        Returns:
            str: The path to the new annotated video.
    """
    video = cv2.VideoCapture(file_path)
    if not video.isOpened():
        raise RuntimeError(f"Failed to open video: {file_path}")
    os.makedirs(output_dir, exist_ok=True)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in video_process_model.frames:
        frame_number = int(frame.seconds * fps)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, f = video.read()
        if not ret:
            continue
        f = draw_on_frame(f, frame.objects)
        out.write(f)
    video.release()
    out.release()
    return output_path
        
def get_image_stats(image_process_model: ImageProcessModel) -> dict:
    """
        Get the image stats.
        Input:
            image_process_model (ImageProcessModel): The image processing model.
        Returns:
            dict: The image stats.
    """
    total_objects = len(image_process_model.objects)
    source_width = image_process_model.source_width
    source_height = image_process_model.source_height
    unique_objects = set(obj.classLabel for obj in image_process_model.objects)
    unique_categories = set(obj.category for obj in image_process_model.objects)
    return {
        "Total objects": total_objects,
        "Source width": source_width,
        "Source height": source_height,
        "Unique objects": " , ".join(unique_objects),
        "Number of unique objects": len(unique_objects),
        "Unique categories": " , ".join(unique_categories),
        "Number of unique categories": len(unique_categories)
    }

def get_video_stats(video_process_model: VideoProcessModel) -> dict:
    """
        Get the video stats.
        Input:
            video_process_model (VideoProcessModel): The video processing model.
        Returns:
            dict: The video stats.
    """
    info = {}
    for idx, frame in enumerate(video_process_model.frames):
        info[f"Frame {idx}"] = {}
        info[f"Frame {idx}"]["Frame number"] = idx
        info[f"Frame {idx}"].update(get_image_stats(frame))

    return pd.DataFrame(info.values())

def get_detailed_video_stats(raw_video_stats: pd.DataFrame) -> dict:
    """
        Get the detailed video stats.
        Input:
            raw_video_stats (pd.DataFrame): The raw video stats.
        Returns:
            dict: The detailed video stats.
    """
    return {
        "Total frames processed": len(raw_video_stats),
        "Unique categories found": ' , '.join(raw_video_stats["Unique categories"].unique().tolist())
    }
