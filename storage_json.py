from file_handler import FileHandlerFactory
from istorage import IStorage

MOVIE_JSON_FILE = "movie_database.json"
MOVIE_JSON_HANDLER = FileHandlerFactory.get_handler(MOVIE_JSON_FILE)


class StorageJson(IStorage):
    """Inherits from this IStorage and implements its functions."""

    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """Loads and returns a list of movies from the JSON file."""
        # movies = load_data()
        # Load movie JSON
        data = MOVIE_JSON_HANDLER.load_data()
        return data.get("movies", [])
        # chronological_order = input(
        #     "\nWould you like to view the movies in chronological order? (Y / N) ").strip().lower()
        # if chronological_order in POSITIVE_RESPONSES:
        #     sorted_movies = sorted(movies, key=lambda m: (m["year"], (-m["rating"])))
        # else:
        #     sorted_movies = sorted(movies, key=lambda m: ((-m["rating"]), m["title"]))
        # print(f"\n{len(movies)} movies in total:\n")
        # for movie in sorted_movies:
        #     print(f'{movie["title"]} ({movie["year"]}): {movie["rating"]}')
        # return sorted_movies

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movies' database.
        Loads the information from the JSON file, add the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = MOVIE_JSON_HANDLER.load_data()
        movies.append({"title": title, "year": year, "rating": rating, "poster": poster})
        MOVIE_JSON_HANDLER.save_data(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the movies' database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = MOVIE_JSON_HANDLER.load_data()
        for i, movie in enumerate(movies):
            if movie['title'].lower() == title.lower():
                del movies[i]
                print(f"{movie['title']} has been deleted.")
                break
        else:
            print(f"{title} not found in database.")
        MOVIE_JSON_HANDLER.save_data(movies)

    def update_movie(self, title, rating):
        """
        Updates a movie from the movies' database.
        Loads the information from the JSON file, updates the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = MOVIE_JSON_HANDLER.load_data()
        for movie in movies:
            if movie['title'].lower() == title.lower():
                movie['rating'] = rating
                print(f"Movie {title} has been successfully updated")
                MOVIE_JSON_HANDLER.save_data(movies)
                return
        print(f"{title} not found in database.")


def main():
    """Testing an instance of the JSON storage class can be created and used."""
    storage = StorageJson('movies.json')
    print(storage.list_movies())
    # storage.add_movie(...)


if __name__ == "__main__":
    main()
