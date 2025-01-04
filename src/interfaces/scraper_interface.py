from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import pandas as pd

class ScraperInterface(ABC):
    @abstractmethod
    def scrape_reviews(self, urls: List[str]) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Scrape reviews from provided Google Play Store URLs
        
        Args:
            urls: List of Google Play Store URLs
            
        Returns:
            Tuple containing:
            - DataFrame with all reviews
            - List of dictionaries with per-app insights
        """
        pass