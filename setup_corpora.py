import subprocess
import sys

def main():
    print("Downloading TextBlob corpora...")
    try:
        subprocess.check_call([sys.executable, '-m', 'textblob.download_corpora'])
        print("Successfully downloaded TextBlob corpora!")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading corpora: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()