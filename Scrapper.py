import requests
from bs4 import BeautifulSoup
import os
import logging

LOG_FILE = "logs/scrapper.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

session = requests.Session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def collect_onion_links(start_url, depth=1, visited=None, to_visit=None, onion_links=None):
    if visited is None:
        visited = set()
    if to_visit is None:
        to_visit = [start_url]
    if onion_links is None:
        onion_links = set()

    for _ in range(depth):
        next_round = []
        for url in to_visit:
            if url in visited:
                continue
            visited.add(url)

            try:
                print(f"Scraping: {url}")
                logging.info(f"Scraping URL: {url}")
                response = session.get(url, headers=headers, timeout=30)
                soup = BeautifulSoup(response.text, 'html.parser')

                for a in soup.find_all('a', href=True):
                    link = a['href']
                    if '.onion' in link:
                        full_link = link if link.startswith('http') else f"http://{link}"
                        if full_link not in visited:
                            onion_links.add(full_link)
                            next_round.append(full_link)

            except Exception as e:
                error_msg = f"Error scraping URL {url}: {e}"
                print(f"Error scraping {url}: {e}")
                logging.error(error_msg)

        to_visit = next_round

    return onion_links

if __name__ == "__main__":
    dataset_path = input("Enter the path for the dataset to be scraped, or press Enter to use the default dataset: ")
    dataset_path = dataset_path if dataset_path else "urlDir/OnionUrlDataset.url"

    if not os.path.exists(dataset_path):
        print(f"File {dataset_path} not found. Exiting...")
        logging.error(f"Dataset file not found: {dataset_path}")
        exit()

    with open(dataset_path, 'r') as f:
        urls = f.readlines()

    depth = int(input("Enter crawl depth (1-3): "))

    all_links = set()
    for url in urls:
        url = url.strip()
        print(f"Starting to scrape from: {url}")
        logging.info(f"Starting to scrape from: {url}")
        links = collect_onion_links(url, depth)
        all_links.update(links)

    if dataset_path == "urlDir/OnionUrlDataset.url":
        output_file = "urlDir/UrlScraps.url"
    else:
        output_file = "urlDir/CustomScrapped.url"

    with open(output_file, 'w') as f:
        f.write("\n".join(all_links))

    print(f"Scraped {len(all_links)} URLs. Saved to '{output_file}'.")
    logging.info(f"Scraped {len(all_links)} URLs. Saved to '{output_file}'.")
