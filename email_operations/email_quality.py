blacklist = [
    "info", "support", "sales", "marketing", "admin", "webmaster",
    "noreply", "no-reply", "contact", "office", "jobs", "careers",
    "billing", "help", "privacy", "dev", "test",
]

DEFAULT_BLOCKED_EMAIL_DOMAINS = {
    "wixsite.com",
    "wix.com",
    "wixstatic.com",
    "wixpress.com",
    "sentry.io",
}


def normalize_domain(domain):
    return domain.strip().lower().strip(".")


def parse_blocked_domains(blocked_domains):
    if not blocked_domains:
        return set(DEFAULT_BLOCKED_EMAIL_DOMAINS)
    return {
        normalize_domain(domain)
        for domain in blocked_domains
        if normalize_domain(domain)
    }


def is_blocked_domain(domain, blocked_domains):
    normalized_domain = normalize_domain(domain)
    for blocked in blocked_domains:
        if normalized_domain == blocked or normalized_domain.endswith(f".{blocked}"):
            return True
    return False


def is_valuable_email(email, blocked_domains=None):
    parts = email.lower().split("@", 1)
    if len(parts) != 2:
        return False

    prefix, domain = parts
    parsed_blocked_domains = parse_blocked_domains(blocked_domains)

    if is_blocked_domain(domain, parsed_blocked_domains):
        return False

    # if any(item in prefix for item in blacklist):
    #     return False

    return True
