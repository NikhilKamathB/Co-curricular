__version__ = "0.1.5"

import os
import logging
from eyepopai.main import main
from eyepopai.core.logger import __setup_logger__

__LOGGING_LEVEL__ = os.getenv("LOGGING_LEVEL", logging.INFO)
__setup_logger__(level=__LOGGING_LEVEL__)
