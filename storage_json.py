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
        return data.get("movies", [])

    def add_movie(self, title, year, rating, poster=None, media_type="movie"):
        """
        Adds a movie to the database and saves it.
        Ensures the poster is stored properly (None if not provided).
        """
        movies = self.list_movies()

        # Prevents empty string posters
        poster = poster.strip() if poster else None

        movies.append({"title": title, "year": year, "rating": rating, "poster": poster or "", "media_type": media_type})
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
        else:
            print(f"{title} has been deleted.")

        self.file_handler.save_data({"movies": updated_movies})  # Store back in correct format

    def update_movie(self, title, rating, poster=None, media_type="movie"):
        """
        Updates the rating and/or poster of a movie by title (case-insensitive).
        If a poster is provided, it updates it; otherwise, it remains unchanged.
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"].lower() == title.lower():
                movie["rating"] = rating
                # Update only if a new poster is provided
                if poster is not None:
                    movie["poster"] = poster.strip() if poster else None
                movie["media_type"] = media_type
                # Store back in correct format
                self.file_handler.save_data({"movies": movies})
                print(f"Movie {title} has been successfully updated.")
                return

        print(f"{title} not found in database.")


def main():
    """Creates a test instance of StorageJson and performs CRUD operations."""
    storage = StorageJson("test_movie_database.json")

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
    storage.update_movie("Test Movie", 1.1)
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