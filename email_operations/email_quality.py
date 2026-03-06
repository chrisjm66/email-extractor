blacklist = [
    'info', 'support', 'sales', 'marketing', 'admin', 'webmaster',
    'noreply', 'no-reply', 'contact', 'office', 'jobs', 'careers',
    'billing', 'help', 'privacy', 'dev', 'test'
]


def is_valuable_email(email):
    prefix = email.split('@')[0].lower()

    if any(item in prefix for item in blacklist):
        return False

    return True
