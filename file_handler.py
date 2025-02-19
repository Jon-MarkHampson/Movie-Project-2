import json
import csv
import os
from abc import ABC, abstractmethod
from text_colour_helper import TextColors as TxtClr


class BaseFileHandler(ABC):
    """Abstract base class for file handling."""

    def __init__(self, file_path):
        self._file_path = file_path
        self._file_extension = os.path.splitext(file_path)[1].lower()

    @abstractmethod
    def load_data(self):
        """Abstract method for loading data."""
        pass

    @abstractmethod
    def save_data(self, data):
        """Abstract method for saving data."""
        pass

    def _file_exists(self):
        """Check if file exists."""
        return os.path.exists(self._file_path)


class HTMLFileHandler(BaseFileHandler):
    """Handles HTML file operations."""

    def load_data(self):
        """Loads HTML content as a single string."""
        if not self._file_exists():
            return ""

        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to read HTML file {self._file_path}. {e}{TxtClr.RESET}")
            return ""

    def save_data(self, data):
        """Saves HTML content."""
        if not isinstance(data, str):
            raise ValueError("HTML data must be a string.")
        try:
            with open(self._file_path, "w", encoding="utf-8") as handle:
                handle.write(data)
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to write HTML file {self._file_path}. {e}{TxtClr.RESET}")


class JSONFileHandler(BaseFileHandler):
    """Handles JSON file operations."""

    def load_data(self):
        """Loads JSON data. Returns an empty dictionary on error."""
        if not self._file_exists():
            return {}

        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError) as e:
            print(f"{TxtClr.LR}Error: Unable to read JSON file {self._file_path}. {e}{TxtClr.RESET}")
            return {}

    def save_data(self, data):
        """Saves data as JSON."""
        try:
            with open(self._file_path, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=4, ensure_ascii=False)
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to write JSON file {self._file_path}. {e}{TxtClr.RESET}")


class CSVFileHandler(BaseFileHandler):
    """Handles CSV file operations."""

    def load_data(self):
        """Loads CSV data. Returns a list of dictionaries."""
        if not self._file_exists():
            return []

        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                return list(reader) if reader.fieldnames else []
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to read CSV file {self._file_path}. {e}{TxtClr.RESET}")
            return []

    def save_data(self, data):
        """Saves CSV data."""
        if not data:
            return  # Avoid saving empty data
        try:
            with open(self._file_path, "w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to write CSV file {self._file_path}. {e}{TxtClr.RESET}")


class TXTFileHandler(BaseFileHandler):
    """Handles TXT file operations."""

    def load_data(self):
        """Loads TXT data. Returns a list of lines."""
        if not self._file_exists():
            return []

        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                return [line.strip() for line in handle if line.strip()]
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to read TXT file {self._file_path}. {e}{TxtClr.RESET}")
            return []

    def save_data(self, data):
        """Saves TXT data."""
        try:
            with open(self._file_path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(data) + "\n")
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to write TXT file {self._file_path}. {e}{TxtClr.RESET}")


class BinaryFileHandler(BaseFileHandler):
    """Handles Binary file operations."""

    def load_data(self):
        """Loads binary data as bytes."""
        if not self._file_exists():
            return b""

        try:
            with open(self._file_path, "rb") as handle:
                return handle.read()
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to read binary file {self._file_path}. {e}{TxtClr.RESET}")
            return b""

    def save_data(self, data):
        """Saves binary data."""
        if not isinstance(data, bytes):
            raise ValueError("Binary data must be of type 'bytes'")
        try:
            with open(self._file_path, "wb") as handle:
                handle.write(data)
        except OSError as e:
            print(f"{TxtClr.LR}Error: Unable to write binary file {self._file_path}. {e}{TxtClr.RESET}")


class FileHandlerFactory:
    """Factory class to return the correct file handler based on extension."""

    _handlers = {
        ".html": HTMLFileHandler,
        ".htm": HTMLFileHandler,
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

    @staticmethod
    def get_handler(file_path):
        """Public factory method to create a handler based on the file type."""

        ext = os.path.splitext(file_path)[1].lower()
        if ext in FileHandlerFactory._handlers:
            return FileHandlerFactory._handlers[ext](file_path)
        raise ValueError(
            f"Unsupported file type: {ext}. Supported types: {', '.join(FileHandlerFactory._handlers.keys())}"
        )


def main():
    """Main function for testing file handlers."""

    # Test HTML Handling
    html_file = "test.html"
    html_handler = FileHandlerFactory.get_handler(html_file)
    html_handler.save_data("<html><body><h1>Hello World</h1></body></html>")
    print("✅ HTML Loaded:", html_handler.load_data())

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
