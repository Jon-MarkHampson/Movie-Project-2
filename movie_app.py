import os
import statistics
import random
import requests
from dotenv import load_dotenv
import country_converter as coco
from storage import StorageJson, StorageCsv
from utils import FileHandlerFactory, UserInputHandler, TextColors as TxtClr

# Load API key from .env file
load_dotenv()
OMDB_API_KEY = os.getenv("API_KEY")

if not OMDB_API_KEY:
    raise ValueError("❌ Error: OMDB API key is missing! Please check your .env file.")

# Constants for directories
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "dist"

# Creates output directory only if it doesn't already exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# OMDb base url
OMDB_URL = "https://www.omdbapi.com/"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage
        self._running = True
        self._user_input = UserInputHandler
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
            "10": self._command_filter_movies,
            "11": self._command_generate_website
        }

    @staticmethod
    def _print_section_header(title, color=TxtClr.LC):
        """Prints a formatted section header with a given title and color."""
        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")
        print(f"{TxtClr.BOLD}{color}{title.center(40, '=')}{TxtClr.RESET}")
        print(f"{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    @staticmethod
    def _convert_movies_dict_string_values_to_numbers(movies):
        """Convert year and rating to appropriate types where possible."""
        for movie in movies:
            movie["year"] = int(movie["year"].split("–")[0]) if movie["year"].isdigit() or "–" in movie["year"] else 0
            movie["rating"] = float(movie["rating"]) if movie["rating"].replace(".", "", 1).isdigit() else 0.0
            movie["media_type"] = movie.get("media_type", "movie")
        return movies

    @staticmethod
    def _print_movie_or_movie_list(movies):
        """Prints a formatted list of movies."""
        for movie in movies:
            type_symbol = {"movie": "🎬", "series": "📺"}.get(movie["media_type"], "🍿")
            print(
                f"{type_symbol} {TxtClr.LY}{movie['title']} {TxtClr.LB}({movie['year']}){TxtClr.RESET} "
                f"{TxtClr.LM}[{movie['media_type']}] {TxtClr.RESET}| "
                f"Rating: {TxtClr.LG}{movie['rating']}{TxtClr.RESET}")

    def _display_best_or_worst(self, title, rating, movies):
        """Prints movies with the highest or lowest rating."""
        matching_movies = [movie for movie in movies if movie["rating"] == rating]
        print(f"\n{title}:")
        self._print_movie_or_movie_list(matching_movies)

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
        self._running = False

    # Menu item 1.
    def _command_list_movies(self):
        """Displays the list of movies with formatting, handling string-based years and ratings."""
        self._print_section_header(" LIST MOVIES ", TxtClr.LB)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Convert year and rating to appropriate types where possible
        self._convert_movies_dict_string_values_to_numbers(movies)

        # Ask user if they want chronological sorting
        chronological_order = self._user_input.confirm_action(
            "Would you like to view the movies in chronological order?")

        if chronological_order:
            sorted_movies = sorted(movies, key=lambda m: (m["year"], -m["rating"]))
        else:
            sorted_movies = sorted(movies, key=lambda m: (-m["rating"], m["title"]))

        print(f"\nTotal movies currently in database: {TxtClr.LG}{len(movies)}{TxtClr.RESET}\n")

        # Print out the sorted list of movies to console
        self._print_movie_or_movie_list(sorted_movies)
        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 2.
    def _command_add_movie(self):
        """Handles user input for adding a new movie from OMDb and delegates storage."""
        self._print_section_header(" ADD MOVIE ", TxtClr.LG)

        # Get the list of existing movie titles
        existing_movies = self._storage.list_movies()
        existing_titles = {movie["title"].lower() for movie in existing_movies}

        while True:
            # Prompt user for a title using UserInputHandler
            user_title = self._user_input.get_non_empty_input("Enter movie or TV title (or press Enter to cancel):")
            if not user_title:
                return

            # Prevent duplicates
            if user_title.lower() in existing_titles:
                print(f"The title '{TxtClr.LY}{user_title.title()}{TxtClr.RESET}' is already in the database!")
                check_add_different_title = self._user_input.confirm_action(
                    "Would you like to add a different title?")
                if check_add_different_title:
                    continue  # Prompt user again
                else:
                    return  # Exit the function

            # Format title for use in URL
            formatted_user_title = user_title.replace(" ", "+")
            url = f"{OMDB_URL}?t={formatted_user_title}&apikey={OMDB_API_KEY}"

            try:
                # Fetch movie details from OMDb API
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                movie_data = response.json()

                # Check if movie was not found
                if "Error" in movie_data:
                    print(
                        f"{TxtClr.LR}ERROR!{TxtClr.RESET} Title: {TxtClr.LY}{user_title}{TxtClr.RESET} - {movie_data['Error']}")
                    check_add_different_title = self._user_input.confirm_action(
                        "Would you like to add a different title?")
                    if check_add_different_title:
                        continue
                    else:
                        return

                # Extract movie details
                title = movie_data.get("Title", "Unknown")
                year = movie_data.get("Year", "Unknown")
                rating = movie_data.get("imdbRating", "0.0")
                poster = movie_data.get("Poster", "")
                media_type = movie_data.get("Type", "movie")
                country = movie_data.get("Country", "Unknown")

                # Store the movie
                self._storage.add_movie(title, year, rating, poster, media_type, country, note="")

                # Print confirmation
                formatted_movie = [
                    {"title": title, "year": year, "rating": rating, "poster": poster, "media_type": media_type}]
                print(f"\n{TxtClr.LG}Successfully added movie!{TxtClr.RESET}")
                self._print_movie_or_movie_list(formatted_movie)

                check_add_different_title = self._user_input.confirm_action(
                    "Would you like to add a different title?")
                if check_add_different_title:
                    continue
                else:
                    return

            except requests.exceptions.ConnectionError:
                print(f"{TxtClr.LR}Error: Unable to connect to OMDb API. Check your internet connection.{TxtClr.RESET}")
            except requests.exceptions.Timeout:
                print(f"{TxtClr.LR}Error: The request timed out. Try again later.{TxtClr.RESET}")
            except requests.exceptions.HTTPError as http_err:
                print(f"{TxtClr.LR}HTTP Error: {http_err}{TxtClr.RESET}")
            except requests.exceptions.RequestException as req_err:
                print(f"{TxtClr.LR}Request Error: {req_err}{TxtClr.RESET}")

    # Menu item 3.
    def _command_delete_movie(self):
        """Handles user input for deleting a movie with best-match suggestions and exit handling."""
        self._print_section_header(" DELETE MOVIE ", TxtClr.LR)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No titles found in the database.{TxtClr.RESET}")
            return

        # Create a dictionary of movie titles (case-insensitive) for lookups
        movie_titles = {movie["title"].lower(): movie["title"] for movie in movies}
        all_titles = list(movie_titles.keys())

        while True:
            # Prompt user for a title using UserInputHandler
            user_title = self._user_input.get_non_empty_input("Enter movie or TV title (or press Enter to cancel):")
            if not user_title:
                return

            # Check for an exact match
            if user_title in movie_titles:
                matched_title = movie_titles[user_title]
                # break
            else:
                # Suggest best matches
                matched_title = self._user_input.get_best_match(user_title, all_titles)

            # If a match was found, confirm deletion, otherwise ask if the user wants to attempt to delete another title
            if matched_title:
                confirm = self._user_input.confirm_action(
                    f"Are you sure you want to delete '{TxtClr.LY}{matched_title.title()}{TxtClr.RESET}'?")
                if confirm:
                    self._storage.delete_movie(matched_title)
                    print(f"\nMovie '{TxtClr.LY}{matched_title.title()}{TxtClr.RESET}' has been successfully deleted!")

                    # Remove the title from available options
                    all_titles.remove(matched_title.lower())
                    del movie_titles[matched_title.lower()]
                else:
                    print(f"\n{TxtClr.LY}Deletion cancelled.{TxtClr.RESET}")

            # Check if user wants to delete a different title
            check_delete_different_title = self._user_input.confirm_action(
                "Would you like to delete a different title?")
            if check_delete_different_title:
                # Prompt user again for a movie title
                continue
            else:
                return

    # Menu item 4.
    def _command_update_movie(self):
        """Update the note of an existing movie with best-match suggestions and exit handling."""
        self._print_section_header(" UPDATE MOVIE ", TxtClr.LM)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Create a dictionary of movie titles (case-insensitive) for lookups
        movie_lookup = {movie["title"].lower(): movie for movie in movies}
        all_titles = list(movie_lookup.keys())

        while True:
            # Prompt user for a title using UserInputHandler
            user_title = self._user_input.get_non_empty_input(
                "Enter the title of the movie or TV show you want to add a note to (or press Enter to cancel):"
            )
            if not user_title:
                return

            # Check for an exact match
            if user_title in movie_lookup:
                matched_title = movie_lookup[user_title]["title"]
            else:
                # Suggest best matches
                matched_title = self._user_input.get_best_match(user_title, all_titles)
                if not matched_title:
                    print(f"{TxtClr.LR}No match found for '{user_title}'. Try again.{TxtClr.RESET}")
                    continue  # Restart loop if no match is found

            matched_movie = movie_lookup[matched_title.lower()]

            # Get the current movie note if one exists
            current_note = matched_movie.get("note", None)

            # Display current note or inform user that there's none
            if current_note:
                print(
                    f"Current note for '{TxtClr.LY}{matched_movie['title']}{TxtClr.RESET}': {TxtClr.LG}{current_note}{TxtClr.RESET}"
                )
            else:
                print(
                    f"{TxtClr.LG}No existing note for{TxtClr.RESET} '{TxtClr.LY}{matched_movie['title']}{TxtClr.RESET}'.")

            # Confirm if they want to proceed
            confirm = self._user_input.confirm_action(
                f"Are you sure you want to add a note to '{TxtClr.LY}{matched_movie['title']}{TxtClr.RESET}'?"
            )

            if confirm:
                # Get new note
                user_input_note = self._user_input.get_non_empty_input("Enter your note:")

                # Update the movie note in storage
                self._storage.update_movie(matched_movie["title"], user_input_note)

                print(
                    f"\n{TxtClr.LG}Added note: {TxtClr.LM}{user_input_note}{TxtClr.RESET} to movie '{TxtClr.LY}{matched_movie['title']}{TxtClr.RESET}' {TxtClr.LG}successfully!{TxtClr.RESET}"
                )

            # Check if user wants to update another movie
            check_update_different_title = self._user_input.confirm_action(
                "Would you like to update a different title?")
            if not check_update_different_title:
                return

    # Menu item 5.
    def _command_movie_stats(self):
        """
        Calculate and display average and median ratings.
        Print all movies with the highest and lowest ratings.
        """
        self._print_section_header(" STATISTICS ", TxtClr.LG)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Convert year and rating to appropriate types where possible
        self._convert_movies_dict_string_values_to_numbers(movies)

        # Extract all ratings
        ratings = [movie["rating"] for movie in movies]

        # Calculate statistics
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)
        max_rating = max(ratings)
        min_rating = min(ratings)

        print(f"\nAverage Rating: {TxtClr.LG}{avg_rating:.2f}{TxtClr.RESET}")
        print(f"Median Rating: {TxtClr.LG}{median_rating:.2f}{TxtClr.RESET}")

        # Display best and worst movies
        self._display_best_or_worst("Best Movie(s)", max_rating, movies)
        self._display_best_or_worst("Worst Movie(s)", min_rating, movies)

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
        random_movie = [random.choice(movies)]

        # Print random movie to console
        print("\nYour randomly selected title is...")
        self._print_movie_or_movie_list(random_movie)
        print("Enjoy the show!\n")

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
            # Prompt user for a title using UserInputHandler
            user_title = self._user_input.get_non_empty_input(
                "Enter movie or TV title to search (or press Enter to cancel):")
            if not user_title:
                return

            # Check for an exact match
            if user_title in movie_titles:
                matched_title = movie_titles[user_title]
                # break
            else:
                # Suggest best matches
                matched_title = self._user_input.get_best_match(user_title, all_titles)

            if matched_title:
                # Fetch the matched movie info from the list of movie dictionaries
                matched_movie = next((movie for movie in movies if movie["title"].lower() == matched_title.lower()),
                                     None)

                # Display search result details
                formatted_movie_for_printing = [matched_movie]
                self._print_movie_or_movie_list(formatted_movie_for_printing)
            else:
                print(f"{TxtClr.LR}No close matches found.{TxtClr.RESET}")

            # Check if user wants to delete a different title
            check_search_different_title = self._user_input.confirm_action(
                "Would you like to search for a different title?")
            if check_search_different_title:
                # Prompt user again for a movie title
                continue
            else:
                return

    # Menu item 8.
    def _command_movies_sorted_by_rating(self):
        """Displays movies sorted by rating from highest to lowest."""
        self._print_section_header(" MOVIES SORTED BY RATING ", TxtClr.LG)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Convert year and rating to appropriate types where possible
        self._convert_movies_dict_string_values_to_numbers(movies)

        # Sort movies by rating (highest to lowest)
        sorted_movies = sorted(movies, key=lambda m: -m["rating"])

        print(f"\n{TxtClr.LG}Total movies: {len(movies)}{TxtClr.RESET}\n")

        # Print out the sorted list of movies to console
        self._print_movie_or_movie_list(sorted_movies)
        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 9.
    def _command_movies_sorted_by_year(self):
        """Displays movies sorted by year in chronological or reverse order."""
        self._print_section_header(" MOVIES SORTED BY YEAR ", TxtClr.M)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Convert year and rating to appropriate types where possible
        self._convert_movies_dict_string_values_to_numbers(movies)

        # Ask user for sorting preference
        order_choice = self._user_input.confirm_action("Would you like to view movies in chronological order?")

        if order_choice:
            # Oldest to newest
            sorted_movies = sorted(movies, key=lambda m: m["year"])
        else:
            # Newest to oldest
            sorted_movies = sorted(movies, key=lambda m: -m["year"])

        print(f"\n{TxtClr.LG}Total movies: {len(movies)}{TxtClr.RESET}\n")

        # Print out the sorted list of movies to console
        self._print_movie_or_movie_list(sorted_movies)
        print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")

    # Menu item 10.
    def _command_filter_movies(self):
        """Filters movies based on user-defined year range or rating threshold."""
        self._print_section_header(" FILTER MOVIES ", TxtClr.LB)

        movies = self._storage.list_movies()

        if not movies:
            print(f"{TxtClr.LR}No movies found in the database.{TxtClr.RESET}")
            return

        # Convert year and rating to appropriate types where possible
        self._convert_movies_dict_string_values_to_numbers(movies)

        filtered_movies = []
        filter_message = ""
        while True:
            print("\nChoose a filter:")
            print(f"{TxtClr.LG}1.{TxtClr.RESET} Filter by year range")
            print(f"{TxtClr.LG}2.{TxtClr.RESET} Filter by rating threshold")

            # Get filter choice
            choice = self._user_input.get_non_empty_input(
                "Choose a filter (or press Enter to cancel):",
                cancel_message="Filtering cancelled."
            )

            if choice is None:
                # Exit if the user cancels
                return

            if choice not in {"1", "2"}:
                print(f"{TxtClr.LR}Invalid choice. Please enter 1 or 2.{TxtClr.RESET}")
                continue

            if choice == "1":
                # Get year range
                min_year = self._user_input.get_valid_numeric_input("Enter start year:", 1800, 2100)
                if min_year is None:
                    # Exit if canceled
                    return

                max_year = self._user_input.get_valid_numeric_input("Enter end year:", min_year, 2100)
                if max_year is None:
                    # Exit if canceled
                    return

                filtered_movies = [m for m in movies if min_year <= m["year"] <= max_year]
                filter_message = f"Movies released between {TxtClr.LB}{min_year}{TxtClr.RESET} and {TxtClr.LB}{max_year}{TxtClr.RESET}:"

            elif choice == "2":
                # Get rating threshold
                min_rating = self._user_input.get_valid_numeric_input("Enter minimum rating (0-10):", 0, 10, float)
                if min_rating is None:
                    # Exit if canceled
                    return

                filtered_movies = [m for m in movies if m["rating"] >= min_rating]
                filter_message = f"Movies with rating {TxtClr.LG}{min_rating}{TxtClr.RESET} or higher:"

            if not filtered_movies:
                print(f"{TxtClr.LR}No movies found matching your criteria.{TxtClr.RESET}")
                return

            print(f"\n{filter_message}{TxtClr.RESET}\n")
            sorted_movies = sorted(filtered_movies, key=lambda m: (-m["rating"], m["year"]))
            self._print_movie_or_movie_list(sorted_movies)
            print(f"\n{TxtClr.LC}{'=' * 40}{TxtClr.RESET}")
            # Exit after displaying results
            return

    # Menu item 11.
    def _command_generate_website(self):
        """Creates a modern, responsive website from the movie database."""

        html_template_file = f"{TEMPLATE_DIR}/index_template.html"
        html_template_handler = FileHandlerFactory.get_handler(html_template_file)

        html_output_file = f"{OUTPUT_DIR}/index.html"
        html_output_handler = FileHandlerFactory.get_handler(html_output_file)

        html_output_title = "Jon-Mark's Movies & TV Shows"
        placeholder_title = "__TEMPLATE_TITLE__"
        placeholder_grid = "__TEMPLATE_MOVIE_GRID__"

        # Load movies from storage
        movies = self._storage.list_movies()

        # Generate HTML for each movie
        movies_html_formatted_list = [self._dict_to_html_format(movie) for movie in movies]
        html_content = "\n".join(movies_html_formatted_list)

        # Load HTML template
        html_template = html_template_handler.load_data()

        # Replace placeholders
        modified_html = html_template.replace(placeholder_title, html_output_title)
        modified_html = modified_html.replace(placeholder_grid, html_content)

        # Save the updated HTML
        html_output_handler.save_data(modified_html)

        print(f"\nWebsite was generated {TxtClr.LG}successfully{TxtClr.RESET}.")

    @staticmethod
    def _dict_to_html_format(movie):
        """Creates a modern HTML card for a movie with country flags and hover notes."""

        type_symbol = {"movie": "🎬", "series": "📺"}.get(movie.get("media_type", ""), "🍿")
        movie_note = (movie.get("note") or "").strip()

        # Process country flags
        country_names = movie.get("country", "").split(", ") if movie.get("country") else []

        iso2_codes = []
        if country_names:
            for country in country_names:
                try:
                    iso2_code = coco.convert(names=country.strip(), to='ISO2')
                    iso2_codes.append(iso2_code.lower())
                except Exception as e:
                    print(f"Warning: Could not convert '{country}' to ISO2 - {e}")
                    # Avoid index errors
                    iso2_codes.append("")

        # Generate flag image elements (use fallback text if flag is missing)
        country_flags_html = " ".join(
            f'<img src="https://flagcdn.com/16x12/{code}.png" width="16" height="12" alt="{country.strip()}">' if code else country.strip()
            for code, country in zip(iso2_codes, country_names)
        )

        # Construct OMDb search URL (replace spaces with '+')
        imdb_url = f"https://www.imdb.com/find?q={movie['title'].replace(' ', '+')}"

        return f'''
        <a href="{imdb_url}" target="_blank" class="movie-link">
            <div class="movie-card">
                <img class="movie-poster" src="{movie["poster"]}" alt="{movie["title"]} poster">
                <div class="movie-info">
                    <h3>{movie["title"]} {type_symbol}</h3>
                    <p>{movie["year"]} • ⭐ {movie["rating"]} • {country_flags_html}</p>
                </div>
                {f'<div class="movie-note">{movie_note}</div>' if movie_note else ''}
            </div>
        </a>
        '''

    def run(self):
        """Main loop for the application."""

        while self._running:  # Uses the initialized flag
            self._print_menu(self._dispatcher_menu)
            choice = input("\nEnter your choice: ").strip()

            if choice in self._dispatcher_menu:
                self._dispatcher_menu[choice]()
            else:
                print("Invalid choice, please try again.")


def main():
    storage = StorageJson('data/movie_database.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
