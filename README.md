# YouTube Channel Video Scraper

This script allows you to scrape video data from a YouTube channel and save it to an Excel file. The output includes the video title, published date, and view count. It is a simple and efficient way to analyze a channel's video performance.

As a Youtube professional, I find that it's useful to have this list handy in order to do analysis on a channel.

## Requirements

- Python 3.7+
- pandas
- google-api-python-client
- openpyxl

## Installation

1. Clone the repository:

git clone https://github.com/plotJ/Youtube-Scraper
cd Youtube-Scraper


2. Create a virtual environment:

python -m venv venv


3. Activate the virtual environment:

- On Windows:
  ```
  .\venv\Scripts\activate
  ```

- On macOS/Linux:
  ```
  source venv/bin/activate
  ```

4. Install the required packages:

pip install -r requirements.txt


## Usage

1. Replace the `api_key` in `main.py` with your own YouTube Data API key.

2. Run the script:

python main.py

3. Enter the URL of the YouTube channel you want to scrape when prompted.

4. The script will create an Excel file in the current directory with the scraped video data.

## Code Explanation

The script uses the following libraries:

- `pandas` for handling and exporting data to an Excel file.
- `google-api-python-client` for interacting with the YouTube Data API.
- `html` for decoding HTML entities in the video titles.
- `re` for regular expression pattern matching when extracting channel IDs.

The script first prompts the user for a YouTube channel URL, then checks if the URL is a custom URL (vanity URL) or a standard URL. If it's a custom URL, the script retrieves the channel ID using the YouTube Data API. It then fetches the video data for the channel, including the title, published date, and view count. This data is stored in a pandas DataFrame, which is then saved to an Excel file.

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
