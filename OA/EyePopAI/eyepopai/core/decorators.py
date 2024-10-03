####################################################################################################
# Define decorators here.
####################################################################################################

import os
import logging
from functools import wraps
from typing import Callable, Tuple, Any


logger = logging.getLogger(__name__)


def validate_file(allowed_types: Tuple[str, ...]) -> Callable:
    """
    Decorator to validate the file type.
    """
    logger.info("validate_file: Validating file type.")
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            file_path = str(kwargs["file_path"])
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            _, file_extension = os.path.splitext(file_path)
            if file_extension.lower() not in allowed_types:
                raise ValueError(f"Invalid file type. Allowed types are: {', '.join(allowed_types)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator