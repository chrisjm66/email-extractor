import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from email_operations.email_extractor import extract_emails

headers = {
    "User-Agent": "Mozilla/5.0"
}

non_html_extensions = {
    ".7z", ".avi", ".bmp", ".css", ".csv", ".doc", ".docx", ".eot", ".epub",
    ".gif", ".gz", ".ico", ".jpeg", ".jpg", ".js", ".json", ".m4a", ".mkv",
    ".mov", ".mp3", ".mp4", ".mpeg", ".mpg", ".odt", ".ogg", ".pdf", ".png",
    ".ppt", ".pptx", ".rar", ".svg", ".tar", ".tif", ".tiff", ".ttf", ".txt",
    ".wav", ".webm", ".webp", ".woff", ".woff2", ".xls", ".xlsx", ".xml",
    ".zip",
}


def is_probably_html_url(url):
    path = urlparse(url).path.lower()
    return not any(path.endswith(ext) for ext in non_html_extensions)


def is_html_response(response):
    content_type = response.headers.get("Content-Type", "").lower()
    return (
        not content_type
        or content_type.startswith("text/html")
        or content_type.startswith("application/xhtml+xml")
    )


def get_page(base_url, blocked_email_domains=None):
    visited = set()
    to_visit = {base_url}
    found_records = []
    seen_record_keys = set()

    pages_crawled = 0
    max_to_crawl = 15

    base_domain = urlparse(base_url).netloc

    while to_visit and pages_crawled < max_to_crawl:
        url = to_visit.pop()
        print("Current URL:", url)

        if url in visited:
            continue

        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            visited.add(url)

            if not is_html_response(res):
                print("Skipping non-HTML response:", url)
                continue

            pages_crawled += 1

            soup = BeautifulSoup(res.text, "html.parser")
            records = extract_emails(
                res.text,
                soup=soup,
                source_url=url,
                blocked_domains=blocked_email_domains,
            )
            for record in records:
                key = (record["email"], record["source_url"])
                if key in seen_record_keys:
                    continue
                seen_record_keys.add(key)
                found_records.append(record)

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                parsed_link = urlparse(link)

                if (
                    parsed_link.scheme in {"http", "https"}
                    and parsed_link.netloc == base_domain
                    and is_probably_html_url(link)
                ):
                    to_visit.add(link)

        except requests.RequestException as e:
            print(f"Request exception for {url}: {e}")

    return found_records
