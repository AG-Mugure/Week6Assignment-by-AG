import os
import requests
from urllib.parse import urlparse
import uuid
from datetime import datetime

def fetch_image():
    # Prompt user for an image URL
    url = input("Enter the image URL: ").strip()

    # Create directory for fetched images
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)

    try:
        # Request the image
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        # If no filename in URL, generate one
        if not filename:
            filename = f"image_{uuid.uuid4().hex}.jpg"

        # Full path to save file
        file_path = os.path.join(save_dir, filename)

        # Save the image in binary mode
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image successfully fetched and saved as: {file_path}")

        # Log the download with timestamp
        log_path = os.path.join(save_dir, "download_log.txt")
        with open(log_path, "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {filename} <- {url}\n")

        print(f"Download logged in: {log_path}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    fetch_image()
