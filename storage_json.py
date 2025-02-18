import json
from file_handler import FileHandlerFactory
from istorage import IStorage


class StorageJson(IStorage):
    """Implements movie storage using JSON files via FileHandler."""

    def __init__(self, file_path):
        """Initializes JSON storage with a file handler."""
        self.file_path = file_path
        self.file_handler = FileHandlerFactory.get_handler(file_path)

    def list_movies(self):
        """
        Loads and returns all movies as a list of dictionaries.
        Extracts the "movies" key from the JSON structure.
        """
        data = self.file_handler.load_data()
        return data.get("movies", [])  # Ensure we return just the movie list

    def add_movie(self, title, year, rating, poster=None):
        """
        Adds a movie to the database and saves it.
        Ensures the poster is stored properly (None if not provided).
        """
        movies = self.list_movies()
        poster = poster.strip() if poster else None  # Prevents empty string posters

        movies.append({"title": title, "year": year, "rating": rating, "poster": poster})
        self.file_handler.save_data({"movies": movies})  # Store back in correct format

    def delete_movie(self, title):
        """
        Deletes a movie by title (case-insensitive) and saves the updated list.
        Prints a message if the movie is not found.
        """
        movies = self.list_movies()
        updated_movies = [movie for movie in movies if movie["title"].lower() != title.lower()]

        if len(updated_movies) == len(movies):
            print(f"{title} not found in database.")
        else:
            print(f"{title} has been deleted.")

        self.file_handler.save_data({"movies": updated_movies})  # Store back in correct format

    def update_movie(self, title, rating, poster=None):
        """
        Updates the rating and/or poster of a movie by title (case-insensitive).
        If a poster is provided, it updates it; otherwise, it remains unchanged.
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"].lower() == title.lower():
                movie["rating"] = rating
                if poster is not None:  # Update only if a new poster is provided
                    movie["poster"] = poster.strip() if poster else None
                self.file_handler.save_data({"movies": movies})  # Store back in correct format
                print(f"Movie {title} has been successfully updated.")
                return

        print(f"{title} not found in database.")


def main():
    """Creates a test instance of StorageJson and lists movies."""
    storage = StorageJson("test_movie_database.json")
    movies = storage.list_movies()
    # storage.delete_movie("Test Movie")
    for movie in movies:
        print(movie)
    storage.add_movie("Test Movie", 1999, 9.9)
    movies = storage.list_movies()
    for movie in movies:
        print(movie)
    storage.update_movie("Test Movie", 1.1,)
    movies = storage.list_movies()
    for movie in movies:
        print(movie)



if __name__ == "__main__":
    main()
