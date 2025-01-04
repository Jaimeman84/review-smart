from setuptools import setup, find_packages

setup(
    name="reviewsmart",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.22.0",
        "google-play-scraper>=1.2.3",
        "textblob>=0.17.1",
        "pandas>=1.5.3",
        "fpdf>=1.7.2",
    ],
    python_requires=">=3.8",
)