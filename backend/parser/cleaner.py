import re


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    cleaned_lines = []

    for line in text.split("\n"):
        line = line.strip()

        line = re.sub(r"\.{5,}", "", line)

        line = re.sub(r"(\|\s*){5,}", "", line)
        line = re.sub(r"(\ .\s*){2,}", "", line)

        line = re.sub(r"(\…\s*){5,}", "", line)

        line = re.sub(r"-{10,}", "", line)


        if not line:
            continue
        
        line = re.sub(r"[ \t]+", " ", line)

        if cleaned_lines and line == cleaned_lines[-1]:
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def clean_pages(pages):
    for page in pages:
        page["text"] = clean_text(page.get("text", ""))
    
    return pages