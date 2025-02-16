from load_and_save_data import load_data
from load_and_save_data import save_data


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    movies.append({"title": title, "year": year, "rating": rating})
    save_data(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    for i, movie in enumerate(movies):
        if movie['title'].lower() == title.lower():
            del movies[i]
            print(f"{movie['title']} has been deleted.")
            break
    else:
        print(f"{title} not found in database.")
    save_data(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    for movie in movies:
        if movie['title'].lower() == title.lower():
            movie['rating'] = rating
            print(f"Movie {title} has been successfully updated")
            save_data(movies)
            return
    print(f"{title} not found in database.")
