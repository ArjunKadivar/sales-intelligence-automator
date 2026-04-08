import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import asyncio
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

# Clean query
def clean_query(text):
    text = re.sub(r"[^\w\s]", " ", text)
    text = " ".join(text.split())
    return text


# DuckDuckGo search
def get_first_result_duckduckgo(query):
    url = f"https://duckduckgo.com/html/?q={query}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        for a in soup.select("a.result__a"):
            link = a.get("href")

            if not link:
                continue

            # Handle redirect links
            if "uddg=" in link:
                parsed = urlparse(link)
                real_url = parse_qs(parsed.query).get("uddg")

                if real_url:
                    return real_url[0]

            if link.startswith("http"):
                return link

    except Exception as e:
        print("DuckDuckGo error:", e)

    return None


# Normalize lead
def normalize_lead(lead: str):
    lead = lead.strip()

    if lead.startswith("http"):
        return lead

    clean_lead = clean_query(lead)
    print(f"🔍 Cleaned query: {clean_lead}")

    query = clean_lead.replace(" ", "+")

    website = get_first_result_duckduckgo(query)

    if website:
        return website

    # fallback: shorter query
    short_query = clean_lead.split("-")[0].strip()

    if short_query != clean_lead:
        print(f"🔁 Retrying with shorter query: {short_query}")
        query = short_query.replace(" ", "+")
        website = get_first_result_duckduckgo(query)

        if website:
            return website

    print("⚠️ Could not resolve website")
    return lead


# Fetch with retry
def fetch_with_retry(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)

            if response.status_code == 200:
                return response.text

            print(f"[Retry {attempt+1}] Status {response.status_code}")

        except Exception as e:
            print(f"[Retry {attempt+1}] Error: {e}")

    return None


# Clean HTML
def clean_text(soup):
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())


# Extract internal links
def extract_internal_links(soup, base_url, limit=3):
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)

        if base_url in full_url and len(links) < limit:
            if full_url not in links:
                links.append(full_url)

    return links


# Scrape single page
async def scrape_single(url):
    print(f" Scraping: {url}")

    html = fetch_with_retry(url)

    if not html:
        return ""

    try:
        soup = BeautifulSoup(html, "html.parser")
        return clean_text(soup)[:3000]

    except:
        return ""


# main scraper
async def scrape_website(lead):
    try:
        print(f"\n Processing Lead: {lead}")

        url = normalize_lead(lead)
        print(f" Using URL: {url}")

        if not url.startswith("http"):
            return None  # trigger fallback

        # Main page
        main_html = fetch_with_retry(url)
        if not main_html:
            return None

        soup = BeautifulSoup(main_html, "html.parser")
        main_text = clean_text(soup)[:3000]

        # Internal links
        links = extract_internal_links(soup, url)
        print("🔗 Links:", links)

        tasks = [scrape_single(link) for link in links]
        extra = await asyncio.gather(*tasks)

        full_content = main_text + " ".join(extra)
        final = full_content[:6000]

        if len(final.strip()) < 50:
            return None

        return final

    except Exception as e:
        print("Scraper error:", e)
        return None