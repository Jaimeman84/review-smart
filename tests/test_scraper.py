import pytest
import pandas as pd
from src.services.scraper_service import GooglePlayScraper

def test_extract_app_id():
    scraper = GooglePlayScraper()
    
    # Test different URL formats
    urls = [
        "https://play.google.com/store/apps/details?id=com.example.app&hl=en",
        "https://play.google.com/store/apps/details?id=com.example.app",
        "play.google.com/store/apps/details?id=com.example.app"
    ]
    
    for url in urls:
        app_id = scraper._extract_app_id(url)
        assert app_id == "com.example.app"

def test_invalid_url():
    scraper = GooglePlayScraper()
    with pytest.raises(ValueError):
        scraper._extract_app_id("invalid_url")

@pytest.mark.integration
def test_scrape_reviews():
    """
    Integration test for review scraping.
    Note: This test requires internet connection and might be rate-limited
    """
    scraper = GooglePlayScraper()
    url = "https://play.google.com/store/apps/details?id=com.aurahealth"
    
    reviews_df, insights = scraper.scrape_reviews([url])
    
    # Basic validation
    assert isinstance(reviews_df, pd.DataFrame)
    assert isinstance(insights, list)
    
    if not reviews_df.empty:
        # Check DataFrame structure
        expected_columns = {'content', 'score', 'app_id', 'app_url'}
        assert all(col in reviews_df.columns for col in expected_columns)
        
        # Check insights structure
        assert len(insights) > 0
        insight = insights[0]
        expected_keys = {
            'app_name', 'app_url', 'app_id', 'total_reviews',
            'reviews_analyzed', 'app_rating', 'negative_reviews', 'average_rating'
        }
        assert all(key in insight for key in expected_keys)

def test_empty_url_list():
    scraper = GooglePlayScraper()
    reviews_df, insights = scraper.scrape_reviews([])
    
    assert isinstance(reviews_df, pd.DataFrame)
    assert reviews_df.empty
    assert insights == []