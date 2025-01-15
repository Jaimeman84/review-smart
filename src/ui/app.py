import streamlit as st
import pandas as pd
from pathlib import Path
from typing import List
import sys

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from src.services.scraper_service import GooglePlayScraper
from src.services.analyzer_service import SentimentAnalyzer

class ReviewSmartUI:
    def __init__(self):
        self.scraper = GooglePlayScraper()
        self.analyzer = SentimentAnalyzer()

    def run(self):
        st.set_page_config(
            page_title="ReviewSmart",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Custom CSS for better layout
        st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        .stMetric {
            background-color: #000;
            padding: 10px;
            border-radius: 5px;
        }
        .stDataFrame {
            width: 100%;
        }
        .row-widget.stButton {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Center the title
        st.markdown("<h1 style='text-align: center;'>ReviewSmart</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Google Play Review Analyzer</p>", unsafe_allow_html=True)

        # URL input
        app_urls = st.text_area(
            "Enter Google Play App URLs (one per line):",
            placeholder="https://play.google.com/store/apps/details?id=com.example.app",
            help="Enter one or more Google Play Store URLs to analyze reviews"
        )

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            analyze_button = st.button("📊 Analyze Reviews", use_container_width=True)

        if analyze_button:
            urls = [url.strip() for url in app_urls.splitlines() if url.strip()]
            
            if not urls:
                st.error("Please enter at least one valid URL")
                return

            try:
                with st.spinner("🔍 Scraping and analyzing reviews..."):
                    reviews_df, app_insights = self.scraper.scrape_reviews(urls)
                
                if not reviews_df.empty:
                    analysis = self.analyzer.analyze_sentiment(reviews_df)
                    self._display_results(analysis, app_insights)
                    self._offer_downloads(reviews_df, analysis)
                else:
                    st.error("No reviews found for the provided URLs")
            
            except Exception as e:
                st.error(f"Error analyzing reviews: {e}")

    def _display_results(self, analysis: dict, app_insights: List[dict]):
        # Display app insights in a clean table
        st.markdown("<h2 style='text-align: center;'>App Overview</h2>", unsafe_allow_html=True)
        insights_df = pd.DataFrame(app_insights)
        styled_insights = insights_df.style.format({
            'app_rating': '{:.2f}',
            'average_rating': '{:.2f}'
        })
        st.dataframe(styled_insights, use_container_width=True, hide_index=True)

        # Display metrics in a row
        st.markdown("<h2 style='text-align: center;'>Analysis Summary</h2>", unsafe_allow_html=True)
        cols = st.columns(4)
        metrics = [
            ("Total Reviews Analyzed", analysis['total_reviews']),
            ("Average Rating", f"{analysis['average_rating']:.2f}"),
            ("Negative Reviews", analysis['negative_reviews']),
            ("Sentiment Score", f"{analysis['average_sentiment']:.2f}")
        ]
        for col, (label, value) in zip(cols, metrics):
            with col:
                st.metric(label, value)

        # Display visualizations side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='text-align: center;'>Word Cloud</h3>", unsafe_allow_html=True)
            if analysis['wordcloud_base64']:
                st.image(
                    f"data:image/png;base64,{analysis['wordcloud_base64']}",
                    use_container_width=True
                )

        with col2:
            st.markdown("<h3 style='text-align: center;'>Sentiment Distribution</h3>", unsafe_allow_html=True)
            sentiment_df = pd.DataFrame(
                list(analysis['sentiment_distribution'].items()),
                columns=['Sentiment', 'Count']
            )
            st.bar_chart(sentiment_df.set_index('Sentiment'))

        # Display common themes and review details side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3 style='text-align: center;'>Common Themes</h3>", unsafe_allow_html=True)
            words_df = pd.DataFrame(
                list(analysis['common_words'].items()),
                columns=['Word', 'Count']
            ).head(10)  # Show top 10 for better visibility
            st.bar_chart(words_df.set_index('Word'))

        with col2:
            st.markdown("<h3 style='text-align: center;'>Latest Reviews</h3>", unsafe_allow_html=True)
            reviews_df = pd.DataFrame(analysis['reviews_data'])
            if not reviews_df.empty:
                reviews_df['at'] = pd.to_datetime(reviews_df['at'])
                st.dataframe(
                    reviews_df.sort_values('at', ascending=False).head(5),  # Show latest 5 reviews
                    use_container_width=True,
                    hide_index=True
                )

    def _offer_downloads(self, reviews_df: pd.DataFrame, analysis: dict):
        st.markdown("<h2 style='text-align: center;'>Download Reports</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Create download buttons
            csv = reviews_df.to_csv(index=False)
            st.download_button(
                "📥 Download Full Review Data (CSV)",
                csv,
                "reviews.csv",
                "text/csv",
                use_container_width=True
            )
            
            # Create insights DataFrame
            insights_df = pd.DataFrame([{
                'total_reviews': analysis['total_reviews'],
                'average_rating': analysis['average_rating'],
                'negative_reviews': analysis['negative_reviews'],
                'average_sentiment': analysis['average_sentiment']
            }])
            insights_csv = insights_df.to_csv(index=False)
            st.download_button(
                "📊 Download Analysis Summary (CSV)",
                insights_csv,
                "insights.csv",
                "text/csv",
                use_container_width=True
            )

            st.markdown("---")
            st.markdown("Made with ❤️ by Jaime Mantilla, MSIT + AI")

if __name__ == "__main__":
    app = ReviewSmartUI()
    app.run()