from typing import Dict
import pandas as pd
from textblob import TextBlob
from collections import Counter
from datetime import datetime
import re
from wordcloud import WordCloud
import base64
import io

class SentimentAnalyzer:
    def __init__(self):
        self.stop_words = {
            'app', 'use', 'using', 'used', 'would', 'could', 'please',
            'think', 'way', 'make', 'need', 'like', 'good', 'great',
            'want', 'get', 'got', 'one', 'also', 'much', 'many',
            'even', 'now', 'will', 'just', 'time'
        }

    def analyze_sentiment(self, reviews_df: pd.DataFrame) -> Dict:
        """
        Analyze sentiments from the reviews DataFrame
        """
        # Handle empty DataFrame
        if reviews_df.empty:
            return self._empty_analysis()

        # Ensure required columns exist
        required_columns = {'content', 'score', 'at'}
        for col in required_columns:
            if col not in reviews_df.columns:
                reviews_df[col] = None
        
        # Calculate sentiments
        sentiment_scores = []
        common_words = Counter()
        all_sentiments = []
        cleaned_texts = []
        
        for _, row in reviews_df.iterrows():
            content = str(row['content'])
            blob = TextBlob(content)
            sentiment = blob.sentiment.polarity
            
            sentiment_scores.append({
                'text': content,
                'score': sentiment
            })
            all_sentiments.append(sentiment)
            
            # Clean and process text for word cloud and common words
            cleaned_text = self._clean_text(content)
            cleaned_texts.append(cleaned_text)
            
            # Add words to counter
            words = cleaned_text.split()
            common_words.update(words)

        # Calculate sentiment distribution
        sentiment_distribution = self._get_sentiment_distribution(all_sentiments)

        # Generate word cloud
        wordcloud_base64 = self._generate_wordcloud(' '.join(cleaned_texts))

        return {
            'total_reviews': len(reviews_df),
            'average_rating': float(reviews_df['score'].mean()) if 'score' in reviews_df.columns else 0.0,
            'negative_reviews': len(reviews_df[reviews_df['score'] <= 3]) if 'score' in reviews_df.columns else 0,
            'average_sentiment': sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0.0,
            'sentiment_scores': sentiment_scores,
            'sentiment_distribution': sentiment_distribution,
            'common_words': dict(common_words.most_common(10)),
            'reviews_data': reviews_df.to_dict('records'),
            'wordcloud_base64': wordcloud_base64
        }

    def _clean_text(self, text: str) -> str:
        """Clean and preprocess text for word cloud and analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Split into words and remove stop words
        words = [word for word in text.split() if word not in self.stop_words]
        
        return ' '.join(words)

    def _generate_wordcloud(self, text: str) -> str:
        """Generate word cloud and return as base64 string"""
        if not text.strip():
            return ''
            
        try:
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                min_font_size=10,
                max_font_size=150,
                colormap='viridis',
                max_words=100
            ).generate(text)

            img = io.BytesIO()
            wordcloud.to_image().save(img, format='PNG')
            img.seek(0)
            return base64.b64encode(img.getvalue()).decode()
        except Exception as e:
            print(f"Error generating word cloud: {e}")
            return ''

    def _get_sentiment_distribution(self, sentiments: list) -> Dict:
        """Calculate sentiment distribution"""
        ranges = {
            'Very Negative': (-1.0, -0.6),
            'Negative': (-0.6, -0.2),
            'Neutral': (-0.2, 0.2),
            'Positive': (0.2, 0.6),
            'Very Positive': (0.6, 1.0)
        }

        distribution = {}
        for label, (low, high) in ranges.items():
            count = sum(1 for s in sentiments if low <= s < high)
            distribution[label] = count

        return distribution

    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            'total_reviews': 0,
            'average_rating': 0.0,
            'negative_reviews': 0,
            'average_sentiment': 0.0,
            'sentiment_scores': [],
            'sentiment_distribution': {},
            'common_words': {},
            'reviews_data': [],
            'wordcloud_base64': ''
        }