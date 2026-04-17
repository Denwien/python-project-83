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


def force_ellipsis(value: str | None, max_length: int = MAX_META_LENGTH) -> str | None:
    if value is None:
        return None
    if value.endswith('...'):
        return value
    return f'{value[:max_length - 3]}...'


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    h1_tags = soup.find_all("h1")
    title_tag = soup.find("title")
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})
    h1_text = extract_longest_text(h1_tags)
    title_text = extract_text(title_tag)
    description_text = (
        meta_desc_tag["content"].strip()
        if meta_desc_tag and meta_desc_tag.get("content")
        else None
    )
    title_overflow = (
        title_text is not None and len(title_text) > MAX_META_LENGTH - 3
    )
    description_overflow = (
        description_text is not None
        and len(description_text) > MAX_META_LENGTH - 3
    )
    h1_result = truncate_with_ellipsis(h1_text)
    if h1_result and (title_overflow or description_overflow):
        h1_result = force_ellipsis(h1_result)

    return {
        "h1": h1_result,
        "title": truncate_with_ellipsis(title_text),
        "description": truncate_with_ellipsis(description_text),
    }
