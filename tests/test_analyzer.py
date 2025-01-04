import pytest
from src.services.analyzer_service import SentimentAnalyzer

@pytest.fixture
def sample_reviews():
    return [
        {
            'reviewId': '1',
            'content': 'This app is great!',
            'score': 5
        },
        {
            'reviewId': '2',
            'content': 'This app needs improvement',
            'score': 2
        }
    ]

def test_sentiment_analysis(sample_reviews):
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_sentiment(sample_reviews)
    
    assert 'sentiment_scores' in result
    assert 'common_issues' in result
    assert 'average_rating' in result
    assert 'total_reviews' in result
    assert result['total_reviews'] == 2
    assert isinstance(result['common_issues'], dict)
