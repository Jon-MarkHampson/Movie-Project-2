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

from storage_json import StorageJson
from movie_app import MovieApp


def main():
    """Initializes storage and runs the MovieApp."""
    storage = StorageJson('movie_database.json')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()