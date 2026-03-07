import re

from .email_quality import is_valuable_email

email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
name_regex = re.compile(r"^[A-Za-z][A-Za-z' .-]{1,80}$")


def clean_whitespace(value):
    return " ".join(value.split())


def build_context_snippet(page_text, email, raw_text="", radius=80):
    lower_page_text = page_text.lower()
    start = lower_page_text.find(email)
    if start != -1:
        left = max(0, start - radius)
        right = min(len(page_text), start + len(email) + radius)
        return clean_whitespace(page_text[left:right])

    lower_raw_text = raw_text.lower()
    raw_start = lower_raw_text.find(email)
    if raw_start == -1:
        return ""

    left = max(0, raw_start - radius)
    right = min(len(raw_text), raw_start + len(email) + radius)
    return clean_whitespace(raw_text[left:right])


def is_probable_name(value):
    normalized = clean_whitespace(value)
    if not normalized:
        return False
    if "@" in normalized or len(normalized.split()) > 4:
        return False
    return bool(name_regex.match(normalized))


def extract_name_from_mailto(soup, email):
    mailto_targets = soup.select("a[href^='mailto:']")
    target_email = email.lower()

    for anchor in mailto_targets:
        href = anchor.get("href", "").lower()
        href_email = href.replace("mailto:", "").split("?", 1)[0].strip()
        if href_email != target_email:
            continue

        anchor_text = clean_whitespace(anchor.get_text(" ", strip=True))
        if is_probable_name(anchor_text):
            return anchor_text

    return ""


def extract_emails(http_response_text, soup, source_url, blocked_domains=None):
    records = []
    page_text = clean_whitespace(soup.get_text(" ", strip=True))
    page_title = clean_whitespace(soup.title.get_text()) if soup.title else ""
    seen_emails = set()

    for match in re.finditer(email_regex, http_response_text):
        email = match.group(0).lower()
        if email in seen_emails:
            continue
        seen_emails.add(email)

        if not is_valuable_email(email, blocked_domains=blocked_domains):
            continue

        contact_name = extract_name_from_mailto(soup, email)
        context_snippet = build_context_snippet(page_text, email, raw_text=http_response_text)

        print("Found email: ", email, "| Name:", contact_name or "N/A")
        records.append(
            {
                "email": email,
                "contact_name": contact_name,
                "source_url": source_url,
                "page_title": page_title,
                "context_snippet": context_snippet,
            }
        )

    return records
