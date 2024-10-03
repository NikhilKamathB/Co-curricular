####################################################################################################
# Define constants here.
####################################################################################################

from enum import Enum


IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".webp")
VIDEO_TYPES = (".mp4", ".mov", ".mkv", ".mpg")

class FileTypes(Enum):
    """
    Enum for file types.
    """
    IMAGE = "Image"
    VIDEO = "Video"