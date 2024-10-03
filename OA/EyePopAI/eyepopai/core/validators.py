####################################################################################################
# Define validators here.
####################################################################################################

from typing import List
from pydantic import BaseModel, Field


class BaseObjectModel(BaseModel):
    """
    A pydantic model base for objects.
    """
    category: str = Field(..., description="The category of the object.")
    classId: int = Field(..., description="Class ID of the detected object")
    classLabel: str = Field(..., description="The class label of the object.")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score of the detection")
    height: float = Field(..., description="Height of the bounding box")
    id: int = Field(..., ge=0, description="Unique identifier for the detected object")
    orientation: float = Field(..., description="Orientation of the object in degrees")
    width: float = Field(..., description="Width of the bounding box")
    x: float = Field(..., description="X-coordinate of the top-left corner of the bounding box")
    y: float = Field(..., description="Y-coordinate of the top-left corner of the bounding box")


class ImageProcessModel(BaseModel):
    """
    A pydantic model for storing the results of an image processing task.
    """
    objects: List[BaseObjectModel] = Field(description="The list of objects detected in the image.", default=[])
    seconds: float = Field(..., description="Time in seconds")
    source_height: int = Field(..., description="The height of the source image.")
    source_id: str = Field(..., description="The ID of the source image.")
    source_width: int = Field(..., description="The width of the source image.")
    system_timestamp: int = Field(..., description="The system timestamp.")
    timestamp: int = Field(..., description="Timestamp.")


class VideoProcessModel(BaseModel):
    """
    A pydantic model for storing the results of a video processing task.
    """
    frames: List[ImageProcessModel] = Field(description="The list of frames processed in the video.")