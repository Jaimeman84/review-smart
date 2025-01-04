# src/services/scraper_service.py
from typing import List, Dict, Tuple
from google_play_scraper import reviews_all, app
import pandas as pd
from src.interfaces.scraper_interface import ScraperInterface
import time
from urllib.parse import urlparse, parse_qs

class GooglePlayScraper(ScraperInterface):
    def scrape_reviews(self, urls: List[str]) -> Tuple[pd.DataFrame, List[Dict]]:
        """
        Scrape reviews from multiple Google Play Store URLs
        """
        all_reviews = pd.DataFrame()
        all_insights = []
        
        for url in urls:
            try:
                print(f"Processing URL: {url}")
                app_id = self._extract_app_id(url)
                print(f"Extracted app_id: {app_id}")
                
                # Get app details
                try:
                    app_info = app(
                        app_id,
                        lang='en',
                        country='us'
                    )
                    print(f"App details fetched. Total reviews: {app_info.get('reviews', 0)}")
                except Exception as e:
                    print(f"Error fetching app details: {e}")
                    continue
                
                # Fetch reviews
                try:
                    print("Fetching reviews...")
                    reviews_data = reviews_all(
                        app_id,
                        sleep_milliseconds=0,  # Don't sleep between requests
                        lang='en',
                        country='us',
                    )
                    print(f"Successfully fetched {len(reviews_data)} reviews")
                    
                    # Convert to DataFrame
                    if reviews_data:
                        df = pd.DataFrame(reviews_data)
                        df['app_id'] = app_id
                        df['app_url'] = url
                        df['app_name'] = app_info.get('title', '')
                        
                        # Generate insights
                        insights = {
                            "app_name": app_info.get('title', ''),
                            "app_url": url,
                            "app_id": app_id,
                            "total_reviews": app_info.get('reviews', 0),
                            "reviews_analyzed": len(df),
                            "app_rating": app_info.get('score', 0.0),
                            "negative_reviews": len(df[df['score'] <= 3]),
                            "average_rating": round(df['score'].mean(), 2) if not df.empty else 0
                        }
                        
                        all_reviews = pd.concat([all_reviews, df], ignore_index=True)
                        all_insights.append(insights)
                        print(f"Successfully processed app: {app_info.get('title', '')}")
                    
                except Exception as e:
                    print(f"Error fetching reviews: {e}")
                    continue
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
        if all_reviews.empty:
            print("No reviews were collected for any URL")
        else:
            print(f"Total reviews collected: {len(all_reviews)}")
        
        return all_reviews, all_insights
    
    def _extract_app_id(self, url: str) -> str:
        """
        Extract app ID from Google Play Store URL handling various formats
        """
        try:
            # Parse the URL
            parsed = urlparse(url)
            
            # Try to get ID from query parameters
            query_params = parse_qs(parsed.query)
            if 'id' in query_params:
                return query_params['id'][0]
            
            # If no ID in query params, try to extract from path
            path_parts = parsed.path.split('/')
            if 'details' in path_parts:
                idx = path_parts.index('details')
                if idx + 1 < len(path_parts):
                    return path_parts[idx + 1]
            
            raise ValueError("Could not find app ID in URL")
            
        except Exception as e:
            raise ValueError(f"Invalid URL format: {url}. Error: {e}")

def process_url(url: str) -> str:
    """Clean and validate URL"""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url