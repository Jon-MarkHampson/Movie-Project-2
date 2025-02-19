from file_handler import FileHandlerFactory
from istorage import IStorage


class StorageCsv(IStorage):
    """Implements movie storage using CSV files via FileHandler."""

    def __init__(self, file_path):
        """Initializes CSV storage with a file handler."""
        self.file_path = file_path
        self.file_handler = FileHandlerFactory.get_handler(file_path)

    def list_movies(self):
        """
        Loads and returns all movies as a list of dictionaries.
        Reads from CSV and ensures consistent output format.
        """
        movies = self.file_handler.load_data()
        return [
            {
                "title": movie["title"],
                "year": int(movie["year"]),
                "rating": float(movie["rating"]),
                "poster": movie["poster"] if movie["poster"] else None
            }
            for movie in movies
        ]

    def add_movie(self, title, year, rating, poster=None, media_type="movie"):
        """
        Adds a movie to the CSV database.
        Saves movie with an empty string if poster is None.
        """
        movies = self.list_movies()
        movies.append(
            {"title": title, "year": year, "rating": rating, "poster": poster or "", "media_type": media_type})
        self.file_handler.save_data(movies)

    def delete_movie(self, title):
        """
        Deletes a movie by title (case-insensitive) and saves the updated list.
        Prints a message if the movie is not found.
        """
        movies = self.list_movies()
        updated_movies = [movie for movie in movies if movie["title"].lower() != title.lower()]

        if len(updated_movies) == len(movies):
            print(f"{title} not found in database.")

        self.file_handler.save_data(updated_movies)

    def update_movie(self, title, rating, poster=None):
        """
        Updates the rating and/or poster of a movie by title (case-insensitive).
        If a poster is provided, it updates it; otherwise, it remains unchanged.
        """
        movies = self.list_movies()

        for movie in movies:
            if movie["title"].lower() == title.lower():
                movie["rating"] = rating
                if poster is not None:  # Only update poster if provided
                    movie["poster"] = poster if poster else None
                self.file_handler.save_data(movies)
                print(f"Movie {title} has been successfully updated.")
                return

        print(f"{title} not found in database.")


def main():
    """Creates a test instance of StorageCsv and lists movies."""
    storage = StorageCsv("test_movie_database.csv")

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
