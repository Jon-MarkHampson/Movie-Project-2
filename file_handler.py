import json
import csv
import os
from abc import ABC, abstractmethod


class BaseFileHandler(ABC):
    """Abstract base class for file handling."""

    def __init__(self, file_path):
        self._file_path = file_path
        self._file_extension = self._get_extension()

    @abstractmethod
    def load_data(self):
        """Abstract method for loading data."""
        pass

    @abstractmethod
    def save_data(self, data):
        """Abstract method for saving data."""
        pass

    def _get_extension(self):
        """Internal method to get the file extension."""
        return os.path.splitext(self._file_path)[1].lower()


class JSONFileHandler(BaseFileHandler):
    """Handles JSON file operations."""

    def load_data(self):
        """Public method to load JSON data."""
        # Return an empty dictionary if the file does not exist
        if not os.path.exists(self._file_path):
            return {}

        try:
            return self._load_json()
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self._file_path}")
            return {}

    def save_data(self, data):
        """Public method to save data as JSON."""
        self._save_json(data)

    def _load_json(self):
        """Private method to load JSON file."""
        with open(self._file_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def _save_json(self, data):
        """Private method to save data as JSON."""
        with open(self._file_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=4, ensure_ascii=False)


class CSVFileHandler(BaseFileHandler):
    """Handles CSV filer operations."""

    def load_data(self):
        """Public method to load CSV data."""
        # Return an empty list if the file does not exist
        if not os.path.exists(self._file_path):
            return []
        return self._load_csv()

    def save_data(self, data):
        """Public method to save CSV data."""
        # Don't save an empty dataset
        if not data:
            return
        self._save_csv(data)

    def _load_csv(self):
        """Private method to load CSV data."""
        with open(self._file_path, "r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return list(reader) if reader.fieldnames else []

    def _save_csv(self, data):
        """Private method to save CSV data."""
        with open(self._file_path, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


class TXTFileHandler(BaseFileHandler):
    """Handles TXT filer operations."""

    def load_data(self):
        """Public method to load TXT data."""
        # Return an empty list if the file does not exist
        if not os.path.exists(self._file_path):
            return []
        return self._load_txt()

    def save_data(self, data):
        """Public method to save TXT data"""
        self._save_txt(data)

    def _load_txt(self):
        """Private method to load TXT file."""
        with open(self._file_path, "r", encoding="utf-8") as handle:
            return [line.strip() for line in handle if line.strip()]

    def _save_txt(self, data):
        """Private method to save TXT file."""
        with open(self._file_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(data))


class BinaryFileHandler(BaseFileHandler):
    """Handles Binary file operations."""

    def load_data(self):
        """Loads binary data as bytes."""
        if not os.path.exists(self._file_path):
            return b""  # Empty bytes object
        return self._load_binary()

    def save_data(self, data):
        """Saves binary data."""
        if not isinstance(data, bytes):
            raise ValueError("Binary data must be of type 'bytes'")
        self._save_binary(data)

    def _load_binary(self):
        """Loads binary file."""
        with open(self._file_path, "rb") as handle:
            return handle.read()

    def _save_binary(self, data):
        """Saves binary file."""
        with open(self._file_path, "wb") as handle:
            handle.write(data)


class FileHandlerFactory:
    """Factory class to return the correct file handler based on extension."""

    @staticmethod
    def get_handler(file_path):
        """Public factory method to create a handler based on the file type."""
        ext = os.path.splitext(file_path)[1].lower()
        handlers = {
            ".json": JSONFileHandler,
            ".csv": CSVFileHandler,
            ".txt": TXTFileHandler,
            ".bin": BinaryFileHandler,
            ".dat": BinaryFileHandler,
            ".png": BinaryFileHandler,
            ".jpg": BinaryFileHandler,
            ".mp3": BinaryFileHandler,
            ".wav": BinaryFileHandler,
            ".pdf": BinaryFileHandler,
        }

        if ext in handlers:
            return handlers[ext](file_path)
        else:
            supported_types = ", ".join(handlers.keys())
            raise ValueError(f"Unsupported file type: {ext}. Supported types: {supported_types}")


def main():
    """Main function for testing file handlers."""

    # Test JSON Handling
    json_file = "test.json"
    json_handler = FileHandlerFactory.get_handler(json_file)

    dummy_json = {"movies": [{"title": "Matrix", "year": 1999}, {"title": "Dune", "year": 2021}]}
    json_handler.save_data(dummy_json)
    loaded_json = json_handler.load_data()
    print("✅ JSON Loaded:", loaded_json)

    loaded_json["movies"].append({"title": "Interstellar", "year": 2014})
    json_handler.save_data(loaded_json)

    # Test CSV Handling
    csv_file = "test.csv"
    csv_handler = FileHandlerFactory.get_handler(csv_file)

    dummy_csv = [
        {"name": "Alice", "age": "30", "city": "London"},
        {"name": "Bob", "age": "25", "city": "Berlin"},
    ]
    csv_handler.save_data(dummy_csv)
    loaded_csv = csv_handler.load_data()
    print("✅ CSV Loaded:", loaded_csv)

    loaded_csv.append({"name": "Charlie", "age": "35", "city": "Paris"})
    csv_handler.save_data(loaded_csv)

    # Test TXT Handling
    txt_file = "test.txt"
    txt_handler = FileHandlerFactory.get_handler(txt_file)

    dummy_txt = ["hello", "world", "python", "file handling"]
    txt_handler.save_data(dummy_txt)
    loaded_txt = txt_handler.load_data()
    print("✅ TXT Loaded:", loaded_txt)

    loaded_txt.append("extra line")
    txt_handler.save_data(loaded_txt)

    # Test Binary File Handling
    binary_file = "test.bin"
    binary_handler = FileHandlerFactory.get_handler(binary_file)

    dummy_binary_data = b"\x00\x01\x02\x03\x04\x05HelloBinary"
    binary_handler.save_data(dummy_binary_data)
    loaded_binary = binary_handler.load_data()
    print("✅ Binary Loaded:", loaded_binary)

    print("\n🎉 All file handlers tested successfully!")


if __name__ == "__main__":
    main()
