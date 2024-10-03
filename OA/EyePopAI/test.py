####################################################################################################
# Test base
####################################################################################################

import sys
sys.path.append("./eyepopai")

import pytest
import numpy as np
from unittest.mock import patch
from eyepopai.core.decorators import validate_file
from eyepopai.core.constants import IMAGE_TYPES, VIDEO_TYPES
from eyepopai.core.utils import get_file_type, draw_on_frame
from eyepopai.core.validators import BaseObjectModel


@pytest.fixture
def mock_file_exists():
    with patch('os.path.exists') as mock:
        yield mock

@validate_file(list(IMAGE_TYPES) + list(VIDEO_TYPES))
def mock_file_processor(file_path: str):
    return f"Processing {file_path}"

def test_valid_image_file(mock_file_exists):
    mock_file_exists.return_value = True
    res = mock_file_processor(file_path="./data/images/sample.jpeg")
    assert res == "Processing ./data/images/sample.jpeg"

def test_valid_video_file(mock_file_exists):
    mock_file_exists.return_value = True
    res = mock_file_processor(file_path="./data/videos/sample.mp4")
    assert res == "Processing ./data/videos/sample.mp4"

def test_invalid_file_type(mock_file_exists):
    mock_file_exists.return_value = True
    with pytest.raises(ValueError):
        mock_file_processor(file_path="./data/images/sample.csv")

def test_file_not_found(mock_file_exists):
    mock_file_exists.return_value = False
    with pytest.raises(FileNotFoundError):
        mock_file_processor(file_path="./data/images/sample.jpeg")

def test_get_file_type_image():
    assert get_file_type("./data/images/sample.jpeg") == "Image"

def test_get_file_type_video():
    assert get_file_type("./data/videos/sample.mp4") == "Video"

def test_get_file_type_invalid():
    with pytest.raises(ValueError):
        get_file_type("./data/images/sample.csv")

def test_draw_on_frame():
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    objects = [BaseObjectModel(x=10, y=10, width=20, height=20, classLabel="Person", classId=1, confidence=0.9, category="Person", id=1, orientation=0)]
    img = draw_on_frame(img, objects)
    assert img.shape == (100, 100, 3)