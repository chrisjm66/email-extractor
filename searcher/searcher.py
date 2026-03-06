import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from email_operations.email_extractor import extract_emails

headers = {
    "User-Agent": 'Mozilla/5.0'
}


def get_page(url):
    visited = set()
    to_visit = {url}
    found_emails = set()

    pages_crawled = 0
    max_to_crawl = 15

    while to_visit and pages_crawled < max_to_crawl:
        url = to_visit.pop()

        if url in visited:
            continue

        try:
            res = requests.get(url, headers=headers, timeout=5)
            visited.add(url)
            pages_crawled = pages_crawled + 1

            emails = extract_emails(res.text)
            found_emails.add(emails)

            # Parse HTML for anchor tag parsing
            soup = BeautifulSoup(res.text, 'html.parser')
            for a in soup.findall('a', href=True):
                link = urljoin(url, a['href'])

                # check that its still the same domain
                if urlparse(link).netloc == urlparse(url).netloc:
                    to_visit.add(link)

        except Exception as e:
            print(f"exception: {e}")

    return found_emails
