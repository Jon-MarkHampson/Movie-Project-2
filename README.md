# Movie App

A Python-powered interactive movie database and website generator. This app allows users to store, manage, and display
their favorite movies in a sleek, dynamically generated website with a modern UI.

## **📖 Description**

This project is a **Movie Management Application** that allows users to:

- **Store movies** in either JSON or CSV format.
- **Manage movies** by adding, deleting, sorting, and searching.
- **Generate a website** from the movie database.
- **Use a dynamic storage system** based on command-line arguments (`argparse`).
- **Interact via the command line**, with support for creating **personalized** movie databases.
- **View country flags** for each movie's country of origin.
- **Hover over movie cards** to see personal notes added by users.
- **Click movie cards** to open their respective IMDb page.

## Features

- **Command-line Movie Management**: Add, delete, search, and filter movies.
- **OMDb API Integration**: Fetch movie details including posters, ratings, and release years.
- **Dynamic HTML Generation**: Converts stored movies into a professional-looking website.
- **Dark Mode Support**: Toggle between light and dark themes.
- **Responsive UI**: Optimized for desktop, tablet, and mobile views.
- **Sticky Header & Fading Effect**: Smooth gradient transition between the header and content.
- **Country Flags**: Displays flag icons for the movie's country.
- **Movie Notes**: Hover over a movie card to reveal personal notes.
- **Clickable Movie Cards**: Clicking a movie opens its IMDb page.

## Demo

![Movie App Commands](https://cdn.discordapp.com/attachments/1339902346192486403/1342368831099633674/Screenshot_2025-02-21_at_06.32.40.png?ex=67b961e5&is=67b81065&hm=e6b84ac201de6085a6bb2c5a76fbbfd6236520c6f101939112ac35ce13d88f52&)
![Movie App Screenshot List](https://cdn.discordapp.com/attachments/1339902346192486403/1342368804130263131/Screenshot_2025-02-21_at_06.33.11.png?ex=67b961de&is=67b8105e&hm=ec5e04ff04351230d2f47766fdc4e523ef4b9581ecf4bf13d94204648a3ccb40&)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/movie-app.git
   cd movie-app
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up your `.env` file with your OMDb API key:
   ```sh
   echo "API_KEY=your_omdb_api_key" > .env
   ```

## Usage

### Running the App

Run the Python script to manage your movies:
Run main.py to load the **default database**
OSX:

   ```sh
   python3 main.py
   ```

Windows:

   ```sh
   python main.py
   ```

**Add an argument create a new JSON or CSV database:**

   ```sh
   python3 main.py <your-name-movie-database>.json
   ```

### Available Commands

- `Exit Program` - Gracefully exits the program.
- `List Movies` – Displays all stored movies.
- `Add Movie` – Fetches details from OMDb and stores them.
- `Delete Movie` – Removes a movie by title.
- `Update Movie` - Add a note to a specified movie.
- `Movie Stats` - Displays average movies rating and best / worst movies.
- `Random Movie` - Randomly selects a movie from the stored movies.
- `Search Movie` – Finds movies based on user input.
- `Movies Sorted By Rating` - Lists movies by rating in descending order.
- `Movies Sorted By Year` - Displays movies sorted by release year, either from newest to oldest or in chronological
  order.
- `Filter Movies` – Filter by rating or release year.
- `Generate Website` – Generates an HTML file in the `dist/` folder.

### Viewing Your Website

Once generated, open:

   ```sh
   open dist/index.html
   ```

Or, for Windows:

   ```sh
   start dist/index.html
   ```

## File Structure

```
.
├── LICENSE
├── README.md
├── __init__.py
├── data
│   ├── movie_database.csv
│   ├── movie_database.json
│   └── positive_responses.json
├── dist # Git ignored
│   └── index.html # Dynamically Generated Website 
├── main.py
├── movie_app.py
├── requirements.txt
├── static
│   └── styles.css
├── storage
│   ├── __init__.py
│   ├── istorage.py
│   ├── storage_csv.py
│   └── storage_json.py
├── templates
│   └── index_template.html
└── utils
    ├── __init__.py
    ├── file_handler.py
    ├── text_colour_helper.py
    └── user_input_handler.py

```

## Customization

### Adjusting the UI

- Modify `templates/index_template.html` to change the website structure.
- Edit `styles.css` to tweak colors, gradients, and layouts.

### Dark Mode Support

Dark mode is automatically toggled with the **Dark Mode** button.

## Known Issues

- **Header Fade Effect**: Fine-tuned to ensure a seamless transition.
- **Tablet View Adjustments**: Handled to prevent unwanted scrollbars.

## Future Enhancements

- **Live Search Suggestions**
- **Movie Sorting Options**
- **User Authentication for Personalized Lists**

## License

This project is open-source and available under the [MIT License](LICENSE).

## Author

Developed by **Jon-Mark Hampson** with a passion for movies, Python, and sleek UI design.

---
🎬 *Enjoy organizing and displaying your favorite movies in style!*
