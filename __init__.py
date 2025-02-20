"""
Movie-Project-2: A Movie Storage and Management Application
"""

__version__ = "1.0.0"
__author__ = "Jon-Mark"

# Expose key components
from .storage.storage_json import StorageJson
from .utils.file_handler import FileHandlerFactory
from .utils.text_colour_helper import TextColors
from .utils.user_input_handler import UserInputHandler