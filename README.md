# Dark Web Monitoring Tool

The Dark Web Monitoring Tool is a comprehensive solution designed to scrape `.onion` websites, search for specific keywords within them, and log all operations for review. 
The project is divided into two primary modules: `scrapper.py` for scraping `.onion` URLs and `crawl.py` for searching and analyzing content on those URLs.
This tool also includes extensive logging for transparency and debugging.

**Start TOR proxy by "sudo service tor start" and let it be for 2-3 minutes before using Crawler.py and Scrapper.py**

## Features

- **Scraping**: Collects `.onion` URLs from various sources (e.g., marketplaces, blog articles).
- **Keyword Search**: Searches for specified keywords across the scraped URLs and logs the results.
- **Logging**: Captures detailed logs of the scraping and crawling processes for debugging and monitoring.
- **Backup**: Saves search results and logs in backup files for recovery.

## Files and Structure

### `scrapper.py`

- **Purpose**: Gathers `.onion` URLs from given sources, scrapes content, and stores the URLs for further crawling.
- **Key Features**:
  - Accepts `.onion` URLs and scrapes data.
  - Stores the scraped URLs in `urlDir/CustomScrapped.url` or other dataset files.
  - Logs the scraping activity in `logs/scrapper.log`.

### `crawl.py`

- **Purpose**: Searches the scraped URLs for specified keywords and logs the results.
- **Key Features**:
  - Searches for predefined or custom user-provided keywords within the `.onion` sites.
  - Outputs the results to `result/KeywordSearchResults.txt` and creates backup files.
  - Logs crawling activity in `logs/crawl.log`.

### `install.sh`

- **Purpose**: A shell script to install necessary dependencies for the tool.
- **Functionality**: Installs required Python packages and sets up the environment.

### `logs/`

Contains log files for both scraping and crawling:

- **`crawl.log`**: Logs activities and errors during the crawling process.
- **`scrapper.log`**: Logs scraping activities, including any errors encountered while fetching `.onion` URLs.

### `result/`

Stores the results of the keyword searches:

- **`KeywordSearchResults.txt`**: Contains the results of the keyword search across the scraped `.onion` URLs.
- **`KeywordSearchResults.txt.backup`**: A backup of the keyword search results.
- **`KeywordSearchResults.backup`**: A backup file for all the search results.

### `urlDir/`

Contains the URLs that are scraped and ready for crawling:

- **`CustomScrapped.url`**: A custom file for storing user-defined scraped URLs.
- **`OnionUrlDataset.url`**: A default dataset of scraped `.onion` URLs.
- **`UrlScraps.url`**: A file that contains all the URLs collected from the scraping process.

## Logs

The tool maintains detailed logs of all operations, making it easier to debug and track the progress of both scraping and crawling:

- **Scraper Logs**: All scraping activities, including successful URL collections and any errors, are recorded in `logs/scrapper.log`.
- **Crawler Logs**: The crawling process is logged in `logs/crawl.log`, which includes the keyword search status and any issues encountered.

## **Usage**

To use the **OnionKeywordSearchTool**, follow these steps:

1. **Run the Scraper** to collect `.onion` URLs:

   ```bash
   python Scrapper.py 

2. **Run the Crawler** to search key `.onion` URLs:

   ```bash
   python Crawler.py 
