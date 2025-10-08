import re

def extract_title(markdown):
    for line in markdown.splitlines():
        match = re.match(r"^# (.+)$", line.strip())
        if match:
            return match.group(1).strip()
    raise Exception("No h1 header found in markdown")
