import sys
import datetime
import random
import statistics
import movie_storage

positive_responses = {"yes", "y", "yeah"}


def print_menu(dispatcher_menu):
    """ Print a numbered menu based on the dispatcher dictionary. """
    print("\nMenu:")
    for number, func_name in dispatcher_menu.items():
        formatted_function = func_name.__name__.replace('_', ' ').capitalize()
        print(f"{number}.\t{formatted_function}")


def get_user_function_choice(dispatcher_dict):
    """ Prompt the user to select a menu option. """
    total_commands = len(dispatcher_dict)
    while True:
        try:
            user_command_input = int(input("\nEnter choice (0-10): ").strip())
            if user_command_input < 0 or user_command_input > total_commands:
                raise ValueError("\nInvalid choice - Try again")
            break
        except ValueError as e:
            print(f"\nInvalid input - {e}.")
    return user_command_input


def exit_program():
    """ Exit the program. """
    print("Exiting program. Bye!\n")
    sys.exit(0)


def list_movies():
    """ Print the list of movies """
    movies = movie_storage.load_data()

    chronological_order = input("\nWould you like to view the movies in chronological order? (Y / N) ").strip().lower()
    if chronological_order in positive_responses:
        sorted_movies = sorted(movies, key=lambda m: (m["year"], (-m["rating"])))
    else:
        sorted_movies = sorted(movies, key=lambda m: ((-m["rating"]), m["title"]))
    print(f"\n{len(movies)} movies in total:\n")
    for movie in sorted_movies:
        print(f'{movie["title"]} ({movie["year"]}): {movie["rating"]}')


def add_movie():
    """ Add a new movie to the movies' database. """
    movies = movie_storage.load_data()
    existing_titles = [movie["title"].lower() for movie in movies]

    while True:
        title = input("\nEnter new movie name: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a valid movie name.")
            try_again = input("Would you like to try adding a movie title again? (Y / N) ").strip().lower()
            if try_again not in positive_responses:
                return
        elif title.lower() in existing_titles:
            print(f"\n{title} is already in the database")
            try_again = input("Would you like to add a different movie title? (Y / N) ").strip().lower()
            if try_again not in positive_responses:
                return
        else:
            break

    current_year = datetime.datetime.now().year

    while True:
        try:
            year = int(input("Enter new movie year: ").strip())
            if year < 1800 or year > current_year:
                raise ValueError(f"Year must be between 1800 and {current_year}.")
            break
        except ValueError as e:
            print(f"Invalid year - {e}")

    while True:
        try:
            rating = float(input("Enter new movie rating (0-10): ").strip())
            if rating < 0 or rating > 10:
                raise ValueError("Rating must be between 0 and 10.")
            rating = round(rating, 1)
            break
        except ValueError as e:
            print(f"Invalid rating - {e}")
    movie_storage.add_movie(title, year, rating)
    print(f"\nMovie '{title}' ({year}) with rating {rating} successfully added!")


def delete_movie():
    """ Remove a movie from the database by title. """
    title = input("\nEnter movie name to delete: ").strip()
    movie_storage.delete_movie(title)


def update_movie():
    """ Update the rating of an existing movie. """
    movies = movie_storage.load_data()
    movie_titles = [movie["title"].lower() for movie in movies]
    while True:
        title = input("\nEnter movie name to update: ").strip()
        if title.lower() in movie_titles:
            break
        request_list_movies = input(
            "\nMovie title not in database. Would you like to display the list of movies? (Y / N) ").strip().lower()
        if request_list_movies in positive_responses:
            list_movies()

    while True:
        try:
            rating = float(input("Enter new movie rating: ").strip())
            if rating < 0 or rating > 10:
                raise ValueError("Rating must be between 0 and 10.")
            rating = round(rating, 1)
            break
        except ValueError as e:
            print(f"Invalid rating - {e}")
    movie_storage.update_movie(title, rating)


def stats():
    """ Calculate and display average and median ratings.
    Print all movies with the highest and lowest ratings. """
    movies = movie_storage.load_data()
    ratings = [movie["rating"] for movie in movies]

    print(f"Average rating: {statistics.mean(ratings):.2f}")
    print(f"Median rating: {statistics.median(ratings):.2f}")

    max_rating = max(ratings)
    min_rating = min(ratings)

    def best_or_worst_movie(best_or_worst, rating):
        matching_movies = [movie for movie in movies if movie["rating"] == rating]
        if len(matching_movies) > 1:
            print(f"{best_or_worst} movies:")
        else:
            print(f"{best_or_worst} movie:", end="")
        for movie in matching_movies:
            print(f"{movie['title']}, {movie['rating']}")

    best_or_worst_movie("Best", max_rating)
    best_or_worst_movie("Worst", min_rating)


def random_movie():
    """ Print a randomly selected movie. """
    movies = movie_storage.load_data()
    i = random.randint(1, len(movies))
    print(
        f"Your movie for tonight: {movies[i]['title']}, it's rated {movies[i]['rating']}")


def search_movie():
    """ Search for movies by title and display matches. """
    movies = movie_storage.load_data()

    while True:
        search_term = input("\nEnter part of movie name: ").strip().lower()
        if search_term:
            break
        print("Title cannot be empty. Please enter part of a movie title.")

    matching_movies = [movie for movie in movies if search_term in movie['title'].lower()]
    if matching_movies:
        if len(matching_movies) > 1:
            extra_s = "s"
        else:
            extra_s = ""
        print(f"\nMovie{extra_s} with '{search_term}' in the title:\n")
        for movie in matching_movies:
            print(f"{movie['title']}, {movie['rating']}")
    else:
        print(f"\nCurrently, no movie in the database has '{search_term}' in the title")


def movies_sorted_by_rating():
    """ Sort movies by rating in descending order. """
    movies = movie_storage.load_data()
    rating_sorted_movies = sorted(movies, key=lambda m: m['rating'], reverse=True)
    print()
    for movie in rating_sorted_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


def movies_sorted_by_year():
    """ Sort movies by year. User can choose ascending or descending order. """
    movies = movie_storage.load_data()
    descending_sort_input = input("\nDo you want the latest movies first? (Y / N): ").strip().lower()
    descending_sort = descending_sort_input in positive_responses
    year_sorted_movies = sorted(movies, key=lambda m: m['year'], reverse=descending_sort)
    print()
    for movie in year_sorted_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


def filter_movies():
    """ Filter movies by minimum rating, start year, or end year.
    None values for minimum_rating, start_year, or end_year mean
    no filtering is applied for that criterion. """
    movies = movie_storage.load_data()

    try:
        minimum_rating = input("\nEnter minimum rating (leave blank for no minimum rating): ")
        minimum_rating = float(minimum_rating) if minimum_rating else None
    except ValueError:
        print("Invalid input for minimum rating. Using no filter for rating.")
        minimum_rating = None

    try:
        start_year = input("Enter start year (leave blank for no start year): ")
        start_year = int(start_year) if start_year else None
    except ValueError:
        print("Invalid input for start year. Using no filter for start year.")
        start_year = None

    try:
        end_year = input("Enter end year (leave blank for no end year): ")
        end_year = int(end_year) if end_year else None
    except ValueError:
        print("Invalid input for end year. Using no filter for end year.")
        end_year = None

    def movie_filter(movie):
        """Filter function to apply user criteria."""
        if minimum_rating is not None and movie.get("rating", 0) < minimum_rating:
            return False
        if start_year is not None and movie.get("year", 0) < start_year:
            return False
        if end_year is not None and movie.get("year", 0) > end_year:
            return False
        return True

    filtered_movies = list(filter(movie_filter, movies))
    print("\nFiltered Movies:")
    for movie in filtered_movies:
        print(f"{movie['title']} ({movie['year']}): {movie['rating']}")


dispatcher = {
    "0": exit_program,
    "1": list_movies,
    "2": add_movie,
    "3": delete_movie,
    "4": update_movie,
    "5": stats,
    "6": random_movie,
    "7": search_movie,
    "8": movies_sorted_by_rating,
    "9": movies_sorted_by_year,
    "10": filter_movies
}


def main():
    """ Run the main program loop: load data, display the menu, and handle user commands. """
    print("********** My Movies Database **********")

    while True:
        print_menu(dispatcher)
        menu_choice = get_user_function_choice(dispatcher)
        movies_function = dispatcher.get(f"{menu_choice}")
        movies_function()

        continue_check = input("\nPress enter to continue... ").strip().lower()
        if continue_check in {"quit", "exit"}:
            exit_program()
        else:
            continue


if __name__ == "__main__":
    main()
