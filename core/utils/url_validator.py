import re

def is_url(url):
    pattern = r'^https://[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}'
    if not re.match(pattern, url):
        print("URL is invalid: URL must start with 'https://' and contain valid domain")
        return False
    return True