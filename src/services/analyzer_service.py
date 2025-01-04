from typing import Dict
import pandas as pd
from textblob import TextBlob
from collections import Counter
from wordcloud import WordCloud
import base64
import io
import re
from src.interfaces.analyzer_interface import AnalyzerInterface

class SentimentAnalyzer(AnalyzerInterface):
    def __init__(self):
        self.stop_words = {
            'app', 'use', 'using', 'used', 'would', 'could', 'please',
            'think', 'way', 'make', 'need', 'like', 'good', 'great'
        }

    def analyze_sentiment(self, reviews_df: pd.DataFrame) -> Dict:
        """
        Analyze sentiments from the reviews DataFrame
        
        Args:
            reviews_df: DataFrame containing reviews
            
        Returns:
            Dictionary containing analysis results
        """
        if reviews_df.empty:
            return self._empty_analysis()

        # Process reviews
        reviews_df['clean_content'] = reviews_df['content'].apply(self._clean_text)
        reviews_df['sentiment'] = reviews_df['content'].apply(
            lambda x: TextBlob(str(x)).sentiment.polarity
        )
        reviews_df['subjectivity'] = reviews_df['content'].apply(
            lambda x: TextBlob(str(x)).sentiment.subjectivity
        )

        # Generate word cloud
        all_text = ' '.join(reviews_df['clean_content'])
        wordcloud_base64 = self._generate_wordcloud(all_text)

        # Analyze common words
        words = all_text.split()
        word_freq = Counter(words).most_common(20)

        return {
            'total_reviews': len(reviews_df),
            'average_rating': round(reviews_df['score'].mean(), 2),
            'negative_reviews': len(reviews_df[reviews_df['score'] <= 3]),
            'average_sentiment': round(reviews_df['sentiment'].mean(), 2),
            'sentiment_distribution': self._get_sentiment_distribution(reviews_df),
            'common_words': dict(word_freq),
            'wordcloud_base64': wordcloud_base64,
            'reviews_data': reviews_df[[
                'content', 'score', 'sentiment', 'subjectivity', 'at'
            ]].to_dict('records')
        }

    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = [word for word in text.split() if word not in self.stop_words]
        return ' '.join(words)

    def _generate_wordcloud(self, text: str) -> str:
        """Generate word cloud and return as base64 string"""
        try:
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                min_font_size=10,
                max_font_size=150
            ).generate(text)

            img = io.BytesIO()
            wordcloud.to_image().save(img, format='PNG')
            img.seek(0)
            return base64.b64encode(img.getvalue()).decode()
        except Exception as e:
            print(f"Error generating word cloud: {e}")
            return ""

    def _get_sentiment_distribution(self, df: pd.DataFrame) -> Dict:
        """Calculate sentiment distribution"""
        sentiment_ranges = {
            'Very Negative': (-1.0, -0.6),
            'Negative': (-0.6, -0.2),
            'Neutral': (-0.2, 0.2),
            'Positive': (0.2, 0.6),
            'Very Positive': (0.6, 1.0)
        }

        distribution = {}
        for label, (low, high) in sentiment_ranges.items():
            count = len(df[(df['sentiment'] >= low) & (df['sentiment'] < high)])
            distribution[label] = count

        return distribution

    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'total_reviews': 0,
            'average_rating': 0,
            'negative_reviews': 0,
            'average_sentiment': 0,
            'sentiment_distribution': {},
            'common_words': {},
            'wordcloud_base64': '',
            'reviews_data': []
        }