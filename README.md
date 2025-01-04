# ReviewSmart

ReviewSmart is a powerful tool designed to help app developers and businesses analyze Google Play Store reviews efficiently. It provides sentiment analysis, identifies key improvement areas, and generates comprehensive reports from user feedback.

## Features

- **Bulk URL Support**: Analyze multiple apps simultaneously
- **Sentiment Analysis**: Automated analysis of reviews (3 stars and below)
- **Downloadable Reports**: Export insights in CSV and PDF formats
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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

Note: On first run, the application will automatically download required NLTK data if it's not already present.

## Usage

1. Start the Streamlit app:
```bash
streamlit run src/ui/streamlit_app.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter Google Play Store URLs (one per line) and click "Analyze Reviews"

4. View the analysis results and download reports in CSV or PDF format

## Development

### Project Structure

```
reviewsmart/
├── src/
│   ├── interfaces/       # Abstract interfaces
│   ├── services/        # Core functionality
│   └── ui/             # Streamlit UI
├── tests/              # Unit tests
└── ...
```

### Running Tests

```bash
pytest tests/
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

Run formatting:
```bash
black src/ tests/
isort src/ tests/
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with Streamlit
- Uses TextBlob for sentiment analysis
- Powered by google-play-scraper