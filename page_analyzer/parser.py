from bs4 import BeautifulSoup


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    meta_desc_tag = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": h1_tag.get_text(strip=True) if h1_tag else None,
        "title": title_tag.get_text(strip=True) if title_tag else None,
        "description": (
            meta_desc_tag["content"].strip()
            if meta_desc_tag and meta_desc_tag.get("content")
            else None
        ),
    }
