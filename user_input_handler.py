import difflib
from file_handler import FileHandlerFactory
from text_colour_helper import TextColors as TxtClr

# Load positive responses
POSITIVE_FILE = "positive_responses.json"
POSITIVE_HANDLER = FileHandlerFactory.get_handler(POSITIVE_FILE)
POSITIVE_RESPONSES = set(
    response.strip().lower() for response in POSITIVE_HANDLER.load_data().get("positive_responses", []))


class UserInputHandler:
    """Handles user input validation for MovieApp."""

    @staticmethod
    def get_non_empty_input(prompt, cancel_message="Operation cancelled."):
        """Ensures the user inputs a non-empty string, allowing cancellation."""
        while True:
            user_input = input(f"\n{prompt} ").strip()
            if not user_input:
                print(f"{TxtClr.LY}{cancel_message}{TxtClr.RESET}")
                return None
            return user_input

    @staticmethod
    def confirm_action(prompt):
        """Asks the user to confirm an action with (Y/N)."""
        while True:
            response = input(f"\n{prompt} (Y / N): ").strip().lower()
            if not response:
                print(f"{TxtClr.LY}Operation cancelled.{TxtClr.RESET}")
                return False
            if response in POSITIVE_RESPONSES:
                return True
            elif response in {"no", "n"}:
                return False
            else:
                print(f"{TxtClr.LR}Invalid input. Please enter Y or N.{TxtClr.RESET}")

    @staticmethod
    def get_best_match(user_input, options):
        """Finds the best match for user input from a given list.

        - If multiple titles contain the search term, return all of them.
        - Otherwise, suggest best matches.
        """
        lower_options = {option.lower(): option for option in options}
        user_input_lower = user_input.lower()

        # Exact match
        if user_input_lower in lower_options:
            return lower_options[user_input_lower]

        # Find all titles containing the search term
        matches = [title for title in options if user_input_lower in title.lower()]

        if matches:
            print(f"{TxtClr.LB}Titles containing '{user_input}':{TxtClr.RESET}")
            for index, match in enumerate(matches, 1):
                print(f"{index}. {TxtClr.LY}{match.title()}{TxtClr.RESET}")

            # Ask user if they want to select a title from the list
            selected_index = UserInputHandler.get_valid_numeric_input(
                "Enter the number of the movie to select (or press Enter to cancel):",
                min_value=1, max_value=len(matches)
            )

            if selected_index is not None:
                # Adjust for 0-based index
                return matches[selected_index - 1]

            print(f"{TxtClr.LY}Search cancelled.{TxtClr.RESET}")
            return None

        # If no matches, suggest close matches instead
        close_matches = difflib.get_close_matches(user_input_lower, lower_options.keys(), n=5, cutoff=0.4)

        if close_matches:
            print(f"{TxtClr.LB}Did you mean:{TxtClr.RESET}")
            for index, match in enumerate(close_matches, 1):
                print(f"{index}. {TxtClr.LY}{lower_options[match].title()}{TxtClr.RESET}")

            selected_index = UserInputHandler.get_valid_numeric_input(
                "\nEnter the number of the correct movie (or press Enter to cancel):",
                min_value=1, max_value=len(close_matches)
            )

            if selected_index is not None:
                return lower_options[close_matches[selected_index - 1]]

        print(f"{TxtClr.LR}No matches found.{TxtClr.RESET}")
        return None

    @staticmethod
    def get_valid_numeric_input(prompt, min_value, max_value, value_type=int):
        """Ensures user enters a valid numeric value within a given range."""
        while True:
            try:
                user_input = input(f"\n{prompt} ").strip()
                if not user_input:
                    print(f"{TxtClr.LY}Operation cancelled.{TxtClr.RESET}")
                    return None
                value = value_type(user_input)
                if min_value <= value <= max_value:
                    return value
                print(f"{TxtClr.LR}Error: Value must be between {min_value} and {max_value}.{TxtClr.RESET}")
            except ValueError:
                print(f"{TxtClr.LR}Invalid input! Please enter a valid number.{TxtClr.RESET}")
