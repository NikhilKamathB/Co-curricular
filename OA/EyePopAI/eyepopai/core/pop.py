####################################################################################################
# Define a custom top layer for the eyepop sdk here.
####################################################################################################

import os
import logging
from typing import Tuple
from eyepop import EyePopSdk
from eyepopai.core.decorators import validate_file
from eyepopai.core.constants import IMAGE_TYPES, VIDEO_TYPES
from eyepopai.core.validators import ImageProcessModel, VideoProcessModel
from eyepopai.core.utils import draw_on_image, draw_on_video, get_image_stats, get_video_stats, get_detailed_video_stats


logger = logging.getLogger(__name__)


class EyePop:
    
    """
    EyePop is a wrapper class over the eyepop sdk addressing multiple usecases.
    Supported usecases:
        1. Process image using the eyepop sdk
        2. Process video using the eyepop sdk
    """

    __LOG_PREFIX__ = "EyePop"

    def __init__(self) -> None:
        """
        Initialize the EyePop class.
        """
        logger.info(f"{self.__LOG_PREFIX__}: Initializing EyePop class.")
        self.endpoint = EyePopSdk.endpoint(
            pop_id=os.getenv("EYEPOP_POP_ID"),
            secret_key=os.getenv("EYEPOP_SECRET_KEY")
        )
    
    @validate_file(IMAGE_TYPES)
    def process_image(self, file_path: str) -> Tuple[str, dict]:
        """
        Process an image using the eyepop sdk.
        Input:
            image_path (str): The path to the image.
        Returns:
            Tuple[str, dict]: The path to the processed image and the image analytics.
        """
        logger.info(f"{self.__LOG_PREFIX__}: Processing image.")
        with self.endpoint as pop:
            result = pop.upload(file_path).predict()
            image_process_result = ImageProcessModel(**result)
        stats = get_image_stats(image_process_result)
        out = draw_on_image(file_path, image_process_result, os.path.join(os.path.dirname(file_path), "output"))
        return (out, stats)
    
    @validate_file(VIDEO_TYPES)
    def process_video(self, file_path: str) -> Tuple[str, dict, dict]:
        """
        Process a video using the eyepop sdk.
        Input:
            video_path (str): The path to the video.
        Returns:
            Tuple[str, dict, dict]: The path to the processed video, the video analytics and the detailed video analytics.
        """
        logger.info(f"{self.__LOG_PREFIX__}: Processing video.")
        with self.endpoint as pop:
            job = pop.upload(file_path)
            results = []
            while True:
                result = job.predict()
                if not result:
                    break
                results.append(result)
            video_process_result = VideoProcessModel(frames=results)
        raw_stats = get_video_stats(video_process_result)
        detailed_stats = get_detailed_video_stats(raw_stats)
        out = draw_on_video(file_path, video_process_result, os.path.join(os.path.dirname(file_path), "output"))
        return (out, raw_stats, detailed_stats)
    