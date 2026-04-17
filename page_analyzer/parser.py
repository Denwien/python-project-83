from bs4 import BeautifulSoup

MAX_META_LENGTH = 255


def truncate_with_ellipsis(
    value: str | None, max_length: int = MAX_META_LENGTH
) -> str | None:
    if value is None or len(value) <= max_length - 3:
        return value
    return f'{value[:max_length - 3]}...'


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": truncate_with_ellipsis(
            h1_tag.get_text(separator=' ', strip=True) if h1_tag else None
        ),
        "title": truncate_with_ellipsis(
            title_tag.get_text(separator=' ', strip=True) if title_tag else None
        ),
        "description": truncate_with_ellipsis(
            meta_desc_tag["content"].strip()
            if meta_desc_tag and meta_desc_tag.get("content")
            else None
        ),
    }
