import nltk
import subprocess
import sys

def setup_nltk():
    """Download required NLTK data packages"""
    print("Downloading required NLTK packages...")
    required_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'wordnet',
        'stopwords',
        'omw-1.4'
    ]
    
    for package in required_packages:
        try:
            print(f"Downloading {package}...")
            nltk.download(package)
        except Exception as e:
            print(f"Error downloading {package}: {e}")

def setup_textblob():
    """Download TextBlob corpora"""
    print("\nDownloading TextBlob corpora...")
    try:
        subprocess.check_call([sys.executable, '-m', 'textblob.download_corpora'])
        print("Successfully downloaded TextBlob corpora!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading TextBlob corpora: {e}")
        sys.exit(1)

def main():
    print("Setting up NLTK and TextBlob resources...")
    setup_nltk()
    setup_textblob()
    print("\nSetup completed successfully!")

if __name__ == "__main__":
    main()