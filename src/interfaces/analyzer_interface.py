from abc import ABC, abstractmethod
from typing import Dict
import pandas as pd

class AnalyzerInterface(ABC):
    @abstractmethod
    def analyze_sentiment(self, reviews_df: pd.DataFrame) -> Dict:
        """
        Analyze sentiments from the reviews DataFrame
        
        Args:
            reviews_df: DataFrame containing reviews
            
        Returns:
            Dictionary containing analysis results with at least:
            - total_reviews: int
            - sentiment_scores: list
            - common_words: dict
            - reviews_data: list
        """
        pass