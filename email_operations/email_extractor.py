import re

from email.email_quality import is_valuable_email

email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'


def extract_emails(http_response_text):
    emails = set()

    raw_emails = re.findall(email_regex, http_response_text)
    for email in raw_emails:
        if is_valuable_email(email):
            emails.add(email)

    return emails
