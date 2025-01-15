# ReviewSmart

ReviewSmart is a powerful tool designed to help app developers and businesses analyze Google Play Store reviews efficiently. It provides sentiment analysis, identifies key improvement areas, and generates comprehensive reports from user feedback.

## Features

- **Bulk URL Support**: Analyze multiple apps simultaneously
- **Sentiment Analysis**: Automated sentiment analysis of reviews
- **Data Visualization**: 
  - Word cloud of common themes
  - Sentiment distribution charts
  - Rating distribution
- **Downloadable Reports**: Export insights in CSV format
- **User-Friendly Interface**: Built with Streamlit for easy interaction

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reviewsmart.git
cd reviewsmart
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/ui/streamlit_app.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter Google Play Store URLs (one per line) in the format:
```
https://play.google.com/store/apps/details?id=com.example.app
```

4. Click "Analyze Reviews" to start the analysis

## Project Structure

```
reviewsmart/
├── src/
│   ├── interfaces/      # Abstract interfaces
│   │   ├── analyzer_interface.py
│   │   └── scraper_interface.py
│   ├── services/       # Core functionality
│   │   ├── analyzer_service.py
│   │   └── scraper_service.py
│   └── ui/            # Streamlit UI
│       └── streamlit_app.py
├── tests/             # Unit tests
│   ├── test_analyzer.py
│   └── test_scraper.py
├── requirements.txt   # Project dependencies
└── README.md
```

## Development

### Running Tests

Run all tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_analyzer.py -v
```

### Code Style

The project follows Python best practices and SOLID principles:
- Single Responsibility Principle: Each class has one primary responsibility
- Open/Closed Principle: Open for extension, closed for modification
- Liskov Substitution Principle: Interfaces are properly abstracted
- Interface Segregation: Interfaces are focused and minimal
- Dependency Inversion: High-level modules depend on abstractions

## Limitations

- The Google Play Scraper API has some limitations on the number of reviews it can fetch
- The app typically can analyze around 2000-3000 reviews reliably
- Review scraping might be affected by rate limiting

## Contributing

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a Pull Request

## Dependencies

- streamlit: Web interface
- google-play-scraper: Review scraping
- textblob: Sentiment analysis
- pandas: Data manipulation
- wordcloud: Word cloud generation
- pillow: Image processing
- pytest: Testing

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [google-play-scraper](https://github.com/JoMingyu/google-play-scraper) for data collection
- Sentiment analysis powered by [TextBlob](https://textblob.readthedocs.io/)