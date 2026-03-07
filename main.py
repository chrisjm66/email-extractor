import os

from email_operations.email_quality import DEFAULT_BLOCKED_EMAIL_DOMAINS
from searcher.searcher import get_page
from csv_operations.export_csv import write_to_csv


def build_blocked_email_domains():
    blocked = set(DEFAULT_BLOCKED_EMAIL_DOMAINS)
    raw_env_domains = os.getenv("BLOCKED_EMAIL_DOMAINS", "")

    env_domains = [
        value.strip().lower().strip(".")
        for value in raw_env_domains.split(",")
        if value.strip()
    ]
    blocked.update(env_domains)
    return blocked


def get_links():
    # opening the file
    file_obj = open("links.txt", "r")

    # reading the data from the file
    file_data = file_obj.read()

    # splitting the file data into lines
    lines = file_data.splitlines()
    print(lines)
    file_obj.close()
    return lines


def main():
    blocked_email_domains = build_blocked_email_domains()
    urls = get_links()
    all_records = []
    for url in urls:
        page = get_page(url, blocked_email_domains=blocked_email_domains)

        if page:
            all_records.extend(page)

    write_to_csv(all_records)


if __name__ == "__main__":
    main()
