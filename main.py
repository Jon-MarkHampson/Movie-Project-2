"""
Main entry point for the MovieApp.

This script initializes the movie storage and starts the MovieApp interface.

Usage:
    Run this script to launch the MovieApp, which allows users to manage a
    movie database through a command-line interface.

Features:
- Loads movie data from a JSON file.
- Provides a menu for listing, adding, deleting, updating, and filtering movies.
- Supports fuzzy search for better movie lookup.
- Includes statistics and random movie selection.

Author: Jon-Mark
Date: February 2025
"""

import argparse
import os
from storage import StorageJson, StorageCsv
from movie_app import MovieApp

# Define the data directory
DATA_DIR = "data"
DEFAULT_STORAGE_FILE = "movie_database.json"


def parse_arguments():
    """Parses command-line arguments to get the storage file."""
    parser = argparse.ArgumentParser(description="Start the MovieApp with a specified storage file.")

    parser.add_argument(
        "storage_file",
        type=str,
        nargs="?",
        default=DEFAULT_STORAGE_FILE,
        help=f"The storage file (e.g., movies.json or movies.csv). Defaults to {DEFAULT_STORAGE_FILE}"
    )

    return parser.parse_args()


def get_storage_handler(storage_file):
    """Determines the correct storage handler based on the file extension."""
    # Ensure the file path is inside the `data/` directory
    storage_path = os.path.join(DATA_DIR, storage_file)

    # Extract file extension
    file_extension = os.path.splitext(storage_file)[-1].lower()

    if file_extension == ".json":
        return StorageJson(storage_path)
    elif file_extension == ".csv":
        return StorageCsv(storage_path)
    else:
        raise ValueError("Unsupported file type! Please use a .json or .csv file.")


def main():
    """Main entry point for MovieApp."""
    args = parse_arguments()
    storage_handler = get_storage_handler(args.storage_file)

    app = MovieApp(storage_handler)
    app.run()


if __name__ == "__main__":
    main()
