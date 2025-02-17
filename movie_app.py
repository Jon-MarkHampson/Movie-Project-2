import statistics
import datetime
import difflib
import random
from file_handler import FileHandlerFactory
from text_colour_helper import TextColors as TxtClr

POSITIVE_FILE = "positive_responses.json"
POSITIVE_HANDLER = FileHandlerFactory.get_handler(POSITIVE_FILE)

# Load positive responses
POSITIVE_RESPONSES = POSITIVE_HANDLER.load_data()


class MovieApp:
    def __init__(self, storage):
        self._storage = storage
        self.running = True
        self._dispatcher_menu = {
            "0": self._command_exit_program,
            "1": self._command_list_movies,
            "2": self._command_add_movie,
            "3": self._command_delete_movie,
            "4": self._command_update_movie,
            "5": self._command_movie_stats,
            "6": self._command_random_movie,
            "7": self._command_search_movie,
            "8": self._command_movies_sorted_by_rating,
            "9": self._command_movies_sorted_by_year,
            "10": self._command_filter_movies
        }

    @staticmethod
    def _print_section_header(title, color=TxtClr.LC):
        """Prints a formatted section header with a given title and color."""
        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")
        print(f"{TxtClr.BOLD}{color}{title.center(40, '=')}{TxtClr.RESET}")
        print(f"{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    def _print_menu(self, dispatcher_menu):
        """Prints a formatted menu using the generic header method."""
        self._print_section_header(" MOVIE MENU ", TxtClr.LY)

        for number, command in dispatcher_menu.items():
            formatted_name = command.__name__.replace("_command_", "").replace("_", " ").title()
            print(f"{TxtClr.LG}{number}. {TxtClr.RESET}{formatted_name}")

    # Menu item 0.
    def _command_exit_program(self):
        """Exit the program with a nicely formatted message."""
        self._print_section_header(" EXITING MOVIE APP ", TxtClr.LR)

        print(f"\n{TxtClr.LG}Thank you for using the Movie App! Have a great day!{TxtClr.RESET}")
        print(f"{TxtClr.LC}Shutting down...{TxtClr.RESET}\n")
        self.running = False

    # Menu item 1.
    def _command_list_movies(self):
        """Displays the list of movies with formatting."""
        self._print_section_header(" LIST MOVIES ", TxtClr.LB)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Ask user if they want chronological sorting
        chronological_order = input(
            "\nWould you like to view the movies in chronological order? (Y / N) "
        ).strip().lower()

        if chronological_order in POSITIVE_RESPONSES:
            sorted_movies = sorted(movies, key=lambda m: (m["year"], -m["rating"]))
        else:
            sorted_movies = sorted(movies, key=lambda m: (-m["rating"], m["title"]))

        print(f"\n{TxtClr.LG}Total movies: {len(movies)}{TxtClr.RESET}\n")

        for movie in sorted_movies:
            print(
                f"{TxtClr.LY}{movie['title']} {TxtClr.LB}({movie['year']}){TxtClr.RESET}: {TxtClr.LG}{movie['rating']}{TxtClr.RESET}")

        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 2.
    def _command_add_movie(self):
        """Handles user input for adding a new movie and delegates storage."""
        self._print_section_header(" ADD MOVIE ", TxtClr.LG)

        # Get the list of existing movie titles
        existing_movies = self._storage.list_movies()
        existing_titles = {movie["title"].lower() for movie in existing_movies}

        # Prompt user for a movie title
        while True:
            title = input("\nEnter movie title: ").strip()
            if not title:
                print(f"{TxtClr.LR}Title cannot be empty! Please try again.{TxtClr.RESET}")
            elif title.lower() in existing_titles:
                print(f"{TxtClr.LY}The movie '{title}' already exists!{TxtClr.RESET}")
            else:
                break

        # Get the movie release year
        current_year = datetime.datetime.now().year
        while True:
            try:
                year = int(input("Enter movie release year: ").strip())
                if 1800 <= year <= current_year:
                    break
                print(f"{TxtClr.LR}Year must be between 1800 and {current_year}.{TxtClr.RESET}")
            except ValueError:
                print(f"{TxtClr.LR}Invalid input! Enter a valid year.{TxtClr.RESET}")

        # Get the movie rating
        while True:
            try:
                rating = float(input("Enter movie rating (0-10): ").strip())
                if 0 <= rating <= 10:
                    rating = round(rating, 1)
                    break
                print(f"{TxtClr.LR}Rating must be between 0 and 10.{TxtClr.RESET}")
            except ValueError:
                print(f"{TxtClr.LR}Invalid input! Enter a valid rating.{TxtClr.RESET}")

        # (Optional) Get movie poster URL - if not required, remove this
        poster = input("Enter movie poster URL (optional, press enter to skip): ").strip()
        # Default to None if not provided
        if not poster:
            poster = None

        # Store the movie using the storage class
        self._storage.add_movie(title, year, rating, poster)

        print(f"\n{TxtClr.LG}Movie '{title}' ({year}) added successfully!{TxtClr.RESET}")

    # Menu item 3.
    def _command_delete_movie(self):
        """Handles user input for deleting a movie with best-match suggestions and exit handling."""
        self._print_section_header(" DELETE MOVIE ", TxtClr.LR)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Create a dictionary of movie titles (case-insensitive) for lookups
        movie_titles = {movie["title"].lower(): movie["title"] for movie in movies}
        all_titles = list(movie_titles.keys())

        while True:
            title_input = input("\nEnter the movie title to delete (or press Enter to cancel): ").strip().lower()

            if not title_input:
                # Exit the function if user presses Enter
                print(f"{TxtClr.LY}Deletion cancelled.{TxtClr.RESET}")
                return

            # Check for an exact match
            if title_input in movie_titles:
                matched_title = movie_titles[title_input]
                break

            # Suggest best matches
            close_matches = difflib.get_close_matches(title_input, all_titles, n=3, cutoff=0.5)
            if close_matches:
                print(f"{TxtClr.LY}Did you mean:{TxtClr.RESET}")
                for match in close_matches:
                    print(f"- {TxtClr.LG}{movie_titles[match]}{TxtClr.RESET}")

                retry = input("\nEnter the correct movie title (or press Enter to cancel): ").strip().lower()
                if not retry:
                    # Exit function if user presses Enter
                    print(f"{TxtClr.LY}Deletion cancelled.{TxtClr.RESET}")
                    return
                elif retry in movie_titles:
                    matched_title = movie_titles[retry]
                    break
            else:
                print(f"{TxtClr.LR}No close matches found.{TxtClr.RESET}")
                retry = input("\nWould you like to try again? (Y / N): ").strip().lower()
                if retry not in POSITIVE_RESPONSES:
                    # Exit function if user doesn't want to retry
                    print(f"{TxtClr.LY}Deletion cancelled.{TxtClr.RESET}")
                    return

        # Confirm deletion
        confirm = input(f"\nAre you sure you want to delete '{matched_title}'? (Y / N): ").strip().lower()
        if confirm in POSITIVE_RESPONSES:
            self._storage.delete_movie(matched_title)
            print(f"\n{TxtClr.LG}Movie '{matched_title}' has been successfully deleted!{TxtClr.RESET}")
        else:
            print(f"\n{TxtClr.LY}Deletion cancelled.{TxtClr.RESET}")

    # Menu item 4.
    def _command_update_movie(self):
        """Update the rating of an existing movie with best-match suggestions and exit handling."""
        self._print_section_header(" UPDATE MOVIE ", TxtClr.LM)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Create a dictionary of movie titles (case-insensitive) for lookups
        movie_titles = {movie["title"].lower(): movie["title"] for movie in movies}
        all_titles = list(movie_titles.keys())

        while True:
            title_input = input("\nEnter the movie title to update (or press Enter to cancel): ").strip().lower()

            if not title_input:
                # Exit the function if user presses Enter
                print(f"{TxtClr.LY}Update cancelled.{TxtClr.RESET}")
                return

            # Check for an exact match
            if title_input in movie_titles:
                matched_title = movie_titles[title_input]
                break

            # Suggest best matches
            close_matches = difflib.get_close_matches(title_input, all_titles, n=3, cutoff=0.5)
            if close_matches:
                print(f"{TxtClr.LY}Did you mean:{TxtClr.RESET}")
                for match in close_matches:
                    print(f"- {TxtClr.LG}{movie_titles[match]}{TxtClr.RESET}")

                retry = input("\nEnter the correct movie title (or press Enter to cancel): ").strip().lower()
                if not retry:
                    # Exit function if user presses Enter
                    print(f"{TxtClr.LY}Update cancelled.{TxtClr.RESET}")
                    return
                elif retry in movie_titles:
                    matched_title = movie_titles[retry]
                    break
            else:
                print(f"{TxtClr.LR}No close matches found.{TxtClr.RESET}")
                retry = input("\nWould you like to try again? (Y / N): ").strip().lower()
                if retry not in POSITIVE_RESPONSES:
                    # Exit function if user doesn't want to retry
                    print(f"{TxtClr.LY}Update cancelled.{TxtClr.RESET}")
                    return

        # Get new rating input
        while True:
            try:
                rating = float(input(f"\nEnter new rating for '{matched_title}' (0-10): ").strip())
                if 0 <= rating <= 10:
                    rating = round(rating, 1)
                    break
                print(f"{TxtClr.LR}Rating must be between 0 and 10.{TxtClr.RESET}")
            except ValueError:
                print(f"{TxtClr.LR}Invalid input! Enter a valid rating.{TxtClr.RESET}")

        # Update the movie rating in storage
        self._storage.update_movie(matched_title, rating)
        print(f"\n{TxtClr.LG}Movie '{matched_title}' rating updated to {rating} successfully!{TxtClr.RESET}")

    # Menu item 5.
    def _command_movie_stats(self):
        """
        Calculate and display average and median ratings.
        Print all movies with the highest and lowest ratings.
        """
        self._print_section_header(" MOVIE STATISTICS ", TxtClr.LG)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Extract all ratings
        ratings = [movie["rating"] for movie in movies]

        # Calculate statistics
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        max_rating = max(ratings)
        min_rating = min(ratings)

        print(f"\n{TxtClr.LG}Average Rating: {TxtClr.RESET}{avg_rating:.2f}/10")
        print(f"{TxtClr.LG}Median Rating: {TxtClr.RESET}{median_rating:.2f}/10")

        def display_best_or_worst(title, rating):
            """Prints movies with the highest or lowest rating."""
            matching_movies = [movie for movie in movies if movie["rating"] == rating]

            print(f"\n{title}:")
            for movie in matching_movies:
                print(f"- {TxtClr.LY}{movie['title']}{TxtClr.RESET} {TxtClr.LB}({movie['year']}){TxtClr.RESET}: "
                      f"{TxtClr.LG}{movie['rating']}/10{TxtClr.RESET}")

        # Display best and worst movies
        display_best_or_worst("Best Movie(s)", max_rating)
        display_best_or_worst("Worst Movie(s)", min_rating)

        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 6.
    def _command_random_movie(self):
        """Selects and displays a random movie from the database."""
        self._print_section_header(" RANDOM MOVIE ", TxtClr.LG)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Pick a random movie
        random_movie = random.choice(movies)

        print(f"\n🎬 {TxtClr.LY}{random_movie['title']}{TxtClr.RESET} "
              f"{TxtClr.LB}({random_movie['year']}){TxtClr.RESET}: "
              f"{TxtClr.LG}{random_movie['rating']}/10{TxtClr.RESET}")

    # Menu item 7.
    def _command_search_movie(self):
        """Search for a movie with best-match suggestions."""
        self._print_section_header(" SEARCH MOVIE ", TxtClr.LM)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Create a dictionary of movie titles (case-insensitive) for lookups
        movie_titles = {movie["title"].lower(): movie for movie in movies}
        all_titles = list(movie_titles.keys())

        while True:
            title_input = input("\nEnter the movie title to search (or press Enter to cancel): ").strip().lower()

            if not title_input:
                # Exit the function if user presses Enter
                print(f"{TxtClr.LY}Search cancelled.{TxtClr.RESET}")
                return

            # Check for an exact match
            if title_input in movie_titles:
                matched_movie = movie_titles[title_input]
                break

            # Suggest best matches
            close_matches = difflib.get_close_matches(title_input, all_titles, n=3, cutoff=0.5)
            if close_matches:
                print(f"{TxtClr.LY}Did you mean:{TxtClr.RESET}")
                for match in close_matches:
                    print(f"- {TxtClr.LG}{movie_titles[match]['title']}{TxtClr.RESET}")

                retry = input("\nEnter the correct movie title (or press Enter to cancel): ").strip().lower()
                if not retry:
                    # Exit function if user presses Enter
                    print(f"{TxtClr.LY}Search cancelled.{TxtClr.RESET}")
                    return
                elif retry in movie_titles:
                    matched_movie = movie_titles[retry]
                    break
            else:
                print(f"{TxtClr.LR}No close matches found.{TxtClr.RESET}")
                retry = input("\nWould you like to try again? (Y / N): ").strip().lower()
                if retry not in POSITIVE_RESPONSES:
                    # Exit function if user doesn't want to retry
                    print(f"{TxtClr.LY}Search cancelled.{TxtClr.RESET}")
                    return

        # Display movie details
        print(f"\n🎬 {TxtClr.LY}{matched_movie['title']}{TxtClr.RESET} "
              f"{TxtClr.LB}({matched_movie['year']}){TxtClr.RESET}: "
              f"{TxtClr.LG}{matched_movie['rating']}/10{TxtClr.RESET}")

    # Menu item 8.
    def _command_movies_sorted_by_rating(self):
        """Displays movies sorted by rating from highest to lowest."""
        self._print_section_header(" MOVIES SORTED BY RATING ", TxtClr.LG)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Sort movies by rating (highest to lowest)
        sorted_movies = sorted(movies, key=lambda m: -m["rating"])

        print(f"\n{TxtClr.LG}Total movies: {len(movies)}{TxtClr.RESET}\n")

        for movie in sorted_movies:
            print(f"{TxtClr.LY}{movie['title']} {TxtClr.LB}({movie['year']}){TxtClr.RESET}: "
                  f"{TxtClr.LG}{movie['rating']}/10{TxtClr.RESET}")

        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 9.
    def _command_movies_sorted_by_year(self):
        """Displays movies sorted by year in chronological or reverse order."""
        self._print_section_header(" MOVIES SORTED BY YEAR ", TxtClr.M)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Ask user for sorting preference
        order_choice = input("\nWould you like to view movies in chronological order? (Y / N): ").strip().lower()

        if order_choice in POSITIVE_RESPONSES:
            # Oldest to newest
            sorted_movies = sorted(movies, key=lambda m: m["year"])
        else:
            # Newest to oldest
            sorted_movies = sorted(movies, key=lambda m: -m["year"])

        print(f"\n{TxtClr.LG}Total movies: {len(movies)}{TxtClr.RESET}\n")

        for movie in sorted_movies:
            print(f"{TxtClr.LY}{movie['title']} {TxtClr.LB}({movie['year']}){TxtClr.RESET}: "
                  f"{TxtClr.LG}{movie['rating']}/10{TxtClr.RESET}")

        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 10.
    def _command_filter_movies(self):
        """Filters movies based on user-defined year range or rating threshold."""
        self._print_section_header(" FILTER MOVIES ", TxtClr.LB)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        while True:
            print("\nChoose a filter:")
            print(f"{TxtClr.LG}1.{TxtClr.RESET} Filter by year range")
            print(f"{TxtClr.LG}2.{TxtClr.RESET} Filter by rating threshold")
            print(f"{TxtClr.LG}3.{TxtClr.RESET} Cancel")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                # Get year range
                try:
                    min_year = int(input("\nEnter start year: ").strip())
                    max_year = int(input("Enter end year: ").strip())
                except ValueError:
                    print(f"{TxtClr.LR}Invalid input! Please enter valid years.{TxtClr.RESET}")
                    continue

                filtered_movies = [m for m in movies if min_year <= m["year"] <= max_year]

                if not filtered_movies:
                    print(f"{TxtClr.LR}No movies found in this year range.{TxtClr.RESET}")
                    return

                print(f"\n{TxtClr.LG}Movies released between {min_year} and {max_year}:{TxtClr.RESET}\n")

            elif choice == "2":
                # Get rating threshold
                try:
                    min_rating = float(input("\nEnter minimum rating (0-10): ").strip())
                    if not (0 <= min_rating <= 10):
                        raise ValueError
                except ValueError:
                    print(f"{TxtClr.LR}Invalid input! Rating must be between 0 and 10.{TxtClr.RESET}")
                    continue

                filtered_movies = [m for m in movies if m["rating"] >= min_rating]

                if not filtered_movies:
                    print(f"{TxtClr.LR}No movies found with rating {min_rating} or higher.{TxtClr.RESET}")
                    return

                print(f"\n{TxtClr.LG}Movies with rating {min_rating} or higher:{TxtClr.RESET}\n")

            elif choice == "3":
                print(f"{TxtClr.LY}Filtering cancelled.{TxtClr.RESET}")
                return

            else:
                print(f"{TxtClr.LR}Invalid choice. Please enter 1, 2, or 3.{TxtClr.RESET}")
                continue

            # Display filtered movies
            for movie in sorted(filtered_movies, key=lambda m: (-m["rating"], m["year"])):
                print(f"{TxtClr.LY}{movie['title']} {TxtClr.LB}({movie['year']}){TxtClr.RESET}: "
                      f"{TxtClr.LG}{movie['rating']}/10{TxtClr.RESET}")

            print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")
            return

    def _generate_website(self):
        pass

    def run(self):
        """Main loop for the application."""

        while self.running:  # Uses the initialized flag
            self._print_menu(self._dispatcher_menu)
            choice = input("\nEnter your choice: ").strip()

            if choice in self._dispatcher_menu:
                self._dispatcher_menu[choice]()
            else:
                print("Invalid choice, please try again.")


def main():
    from storage_json import StorageJson

    storage = StorageJson('movie_database.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
