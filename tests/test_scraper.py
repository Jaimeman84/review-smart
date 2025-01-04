import pytest
from src.services.scraper_service import GooglePlayScraper

def test_extract_app_id():
    scraper = GooglePlayScraper()
    url = "https://play.google.com/store/apps/details?id=com.example.app&hl=en"
    assert scraper._extract_app_id(url) == "com.example.app"

def test_scrape_reviews():
    scraper = GooglePlayScraper()
    urls = ["https://play.google.com/store/apps/details?id=com.example.app"]
    reviews = scraper.scrape_reviews(urls)
    assert isinstance(reviews, list)
    if reviews:  # If we got actual reviews
        assert all(isinstance(review, dict) for review in reviews)
