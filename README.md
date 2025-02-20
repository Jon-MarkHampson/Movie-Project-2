# Movie App

A Python-powered interactive movie database and website generator. This app allows users to store, manage, and display their favorite movies in a sleek, dynamically generated website with a modern UI.

## Features

- **Command-line Movie Management**: Add, delete, search, and filter movies.
- **OMDb API Integration**: Fetch movie details including posters, ratings, and release years.
- **Dynamic HTML Generation**: Converts stored movies into a professional-looking website.
- **Dark Mode Support**: Toggle between light and dark themes.
- **Responsive UI**: Optimized for desktop, tablet, and mobile views.
- **Sticky Header & Fading Effect**: Smooth gradient transition between the header and content.

## Demo

![Movie App Screenshot](./screenshot.png)

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
   ```sh
   python movie_app.py
   ```

### Available Commands
- `List Movies` – Displays all stored movies.
- `Add Movie` – Fetches details from OMDb and stores them.
- `Delete Movie` – Removes a movie by title.
- `Search Movie` – Finds movies based on user input.
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
movie-app/
│-- dist/                # Generated HTML output (gitignored)
│-- templates/           # HTML templates
│   ├── index_template.html
│-- movie_app.py         # Main application logic
│-- storage_json.py      # JSON-based movie storage handler
│-- file_handler.py      # File handling utility
│-- text_colour_helper.py# CLI text formatting helper
│-- user_input_handler.py# User input handling
│-- .env                 # API key (gitignored)
│-- requirements.txt     # Dependencies
│-- README.md            # This file
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
Developed by **Jon-Mark** with a passion for movies, Python, and sleek UI design.

---
🎬 *Enjoy organizing and displaying your favorite movies in style!*
