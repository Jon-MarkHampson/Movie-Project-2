from utils import FileHandlerFactory
from storage import IStorage


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
        movies = data.get("movies", [])
        return movies

    def add_movie(self, title, year, rating, poster=None, media_type="movie", country=None, note=""):
        """
        Adds a movie to the database and saves it.
        Ensures the poster is stored properly (None if not provided).
        """
        movies = self.list_movies()

        # Prevents empty string posters
        poster = poster.strip() if poster else None

        movies.append(
            {"title": title, "year": year, "rating": rating, "poster": poster or "", "media_type": media_type,
             "country": country or None, "note": note or None})
        # Store back in correct format
        self.file_handler.save_data({"movies": movies})

    def delete_movie(self, title):
        """
        Deletes a movie by title (case-insensitive) and saves the updated list.
        Prints a message if the movie is not found.
        """
        movies = self.list_movies()
        updated_movies = [movie for movie in movies if movie["title"].lower() != title.lower()]

        if len(updated_movies) == len(movies):
            print(f"{title} not found in database.")

        # Store back in correct format
        self.file_handler.save_data({"movies": updated_movies})

    def update_movie(self, title, note=None):
        """
        Updates the note of a movie by title (case-insensitive).
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"].lower() == title.lower():
                movie["note"] = note
                # Only update note if provided
                if note is not None:
                    movie["note"] = note if note else None
                self.file_handler.save_data({"movies": movies})
                return


def main():
    """Creates a test instance of StorageJson and performs CRUD operations."""
    storage = StorageJson("../data/movie_database.json")

    # List movies before any modifications
    print("\n🎬 Initial Movie List:")
    movies = storage.list_movies()
    for movie in movies:
        print(movie)

    # Add a new test movie
    print("\n➕ Adding Test Movie:")
    storage.add_movie("Test Movie", 1999, 9.9)
    movies = storage.list_movies()
    for movie in movies:
        print(movie)

    # Update the test movie's rating
    print("\n🔄 Updating Test Movie Rating:")
    storage.update_movie("Test Movie", "My Favourite Movie")
    movies = storage.list_movies()
    for movie in movies:
        print(movie)

    # Delete the test movie
    print("\n❌ Deleting Test Movie:")
    storage.delete_movie("Test Movie")
    movies = storage.list_movies()
    for movie in movies:
        print(movie)


if __name__ == "__main__":
    main()
