import pytest
import pandas as pd
from datetime import datetime
from src.services.analyzer_service import SentimentAnalyzer

def test_sentiment_analysis():
    # Create minimal test data
    reviews_df = pd.DataFrame({
        'content': ['This app is great!', 'This app needs improvement'],
        'score': [5, 2],
        'at': [datetime.now()] * 2
    })
    
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment(reviews_df)
    
    # Required fields
    required_fields = {
        'total_reviews',
        'average_rating',
        'negative_reviews',
        'average_sentiment',
        'sentiment_scores',
        'sentiment_distribution',
        'common_words',
        'reviews_data',
        'wordcloud_base64'
    }
    
    # Check all required fields are present
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
    
    # Check values
    assert result['total_reviews'] == 2
    assert isinstance(result['average_sentiment'], float)
    assert isinstance(result['sentiment_distribution'], dict)
    assert len(result['sentiment_scores']) == 2

def test_empty_analysis():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment(pd.DataFrame())
    
    # Check required fields
    required_fields = {
        'total_reviews',
        'average_rating',
        'negative_reviews',
        'average_sentiment',
        'sentiment_scores',
        'sentiment_distribution',
        'common_words',
        'reviews_data',
        'wordcloud_base64'
    }
    
    # Check all required fields are present
    for field in required_fields:
        assert field in result, f"Missing required field: {field}"
    
    # Check values for empty analysis
    assert result['total_reviews'] == 0
    assert result['average_rating'] == 0.0
    assert result['negative_reviews'] == 0
    assert result['average_sentiment'] == 0.0
    assert len(result['sentiment_scores']) == 0
    assert result['sentiment_distribution'] == {}