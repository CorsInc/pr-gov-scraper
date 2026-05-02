"""Parsing logic for pr.gov pages."""

from bs4 import BeautifulSoup


def parse_main_page(html: str) -> dict:
    """Extract navigation links, featured services, and announcements."""
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "title": "",
        "navigation_links": [],
        "featured_services": [],
        "announcements": [],
    }

    # Title
    title_tag = soup.find("title")
    if title_tag:
        result["title"] = title_tag.get_text(strip=True)

    # Navigation links
    nav = soup.find("nav")
    if nav:
        for a in nav.find_all("a", href=True):
            text = a.get_text(strip=True)
            if text:
                result["navigation_links"].append({
                    "text": text,
                    "href": a["href"],
                })

    # Look for featured sections / cards
    for section in soup.find_all(["section", "div"], class_=lambda c: c and any(
            kw in (c or "").lower() for kw in ["featured", "service", "card", "destacado"]
    )):
        for a in section.find_all("a", href=True):
            text = a.get_text(strip=True)
            if text:
                result["featured_services"].append({
                    "text": text,
                    "href": a["href"],
                })

    # Announcements / news items
    for item in soup.find_all(["article", "div"], class_=lambda c: c and any(
            kw in (c or "").lower() for kw in ["news", "announce", "notice", "noticia"]
    )):
        title_el = item.find(["h2", "h3", "h4", "a"])
        date_el = item.find("time")
        link = item.find("a", href=True)
        result["announcements"].append({
            "title": title_el.get_text(strip=True) if title_el else "",
            "date": date_el.get("datetime", "") if date_el else "",
            "link": link["href"] if link else "",
        })

    return result


def parse_generic_page(html: str) -> dict:
    """Extract basic info from any pr.gov sub-page."""
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "title": "",
        "headings": [],
        "links": [],
        "text_length": 0,
    }

    title_tag = soup.find("title")
    if title_tag:
        result["title"] = title_tag.get_text(strip=True)

    for h in soup.find_all(["h1", "h2", "h3"]):
        text = h.get_text(strip=True)
        if text:
            result["headings"].append(text)

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if text:
            result["links"].append({"text": text, "href": a["href"]})

    result["text_length"] = len(soup.get_text())

    return result
