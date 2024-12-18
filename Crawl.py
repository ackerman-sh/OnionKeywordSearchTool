import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import subprocess

session = requests.Session()
session.proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

LOG_FILE = "logs/crawl.log"
RESULT_FILE = "result/KeywordSearchResults.txt"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, 'a') as log:
        log.write(f"{timestamp} {message}\n")

def backup_results():
    if os.path.exists(RESULT_FILE):
        backup_file = RESULT_FILE.replace(".txt", ".backup")
        os.rename(RESULT_FILE, backup_file)
        log_message(f"[INFO] Backup created: {backup_file}")

def search_keywords_in_url(url, keywords):
    try:
        print(f"Searching in: {url}")
        log_message(f"[INFO] Searching in URL: {url}")

        response = session.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = {}
        for keyword in keywords:
            if keyword.lower() in soup.get_text().lower():
                results[keyword] = "Found"
            else:
                results[keyword] = "Not Found"
        return results
    except Exception as e:
        error_message = f"[ERROR] Error fetching or processing URL {url}: {e}"
        #print(error_message)
        log_message(error_message)
        return None

if __name__ == "__main__":
    file_path = input("Enter path to scraped URL file (or press enter to use default: urlDir/UrlScraps.url): ")
    file_path = file_path if file_path else "urlDir/UrlScraps.url"

    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Exiting...")
        log_message(f"[ERROR] File {file_path} not found. Exiting...")
        exit()

    with open(file_path, 'r') as f:
        urls = f.readlines()

    keywords = input("Enter comma-separated keywords to search for: ").split(',')

    backup_results()

    with open(RESULT_FILE, 'w') as result_file:
        for url in urls:
            url = url.strip()
            if not url:
                continue

            results = search_keywords_in_url(url, keywords)
            if results:
                result_file.write(f"Results for {url}:\n")
                print(f"Results for {url}:")
                for keyword, status in results.items():
                    result_line = f"  {keyword}: {status}\n"
                    result_file.write(result_line)
                    print(result_line.strip())
                result_file.write("\n")
            else:
                #print(f"Skipping {url} due to an error.")
                log_message(f"[INFO] Skipping {url} due to an error.")

    print(f"Keyword search completed. Results saved to {RESULT_FILE}.")
    log_message(f"[INFO] Keyword search completed. Results saved to {RESULT_FILE}.")

try:
    print("[INFO] Crawling complete. Sending email...")
    subprocess.run(["python3", "smtpSender.py"], check=True)
    print("[SUCCESS] Email script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"[ERROR] Failed to execute email script: {e}")
