from bs4 import BeautifulSoup

MAX_META_LENGTH = 255


def extract_text(tag) -> str | None:
    if not tag:
        return None

    text = ' '.join(tag.stripped_strings)
    return text if text else None


def extract_longest_text(tags) -> str | None:
    texts = [text for tag in tags if (text := extract_text(tag))]
    if not texts:
        return None
    return max(texts, key=len)


def truncate_with_ellipsis(
    value: str | None, max_length: int = MAX_META_LENGTH
) -> str | None:
    if value is None or len(value) <= max_length - 3:
        return value
    return f'{value[:max_length - 3]}...'


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    h1_tags = soup.find_all("h1")
    title_tag = soup.find("title")
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": truncate_with_ellipsis(extract_longest_text(h1_tags)),
        "title": truncate_with_ellipsis(extract_text(title_tag)),
        "description": truncate_with_ellipsis(
            meta_desc_tag["content"].strip()
            if meta_desc_tag and meta_desc_tag.get("content")
            else None
        ),
    }
