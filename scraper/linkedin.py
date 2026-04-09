# ============================================================
#  scraper/linkedin.py — LinkedIn remote + Ontario hybrid search
# ============================================================

import hashlib
import random
import time

import requests
from bs4 import BeautifulSoup

from config import LINKEDIN_SEARCH_LOCATIONS, MAX_AGE_DAYS, SEARCH_KEYWORDS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-CA,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def make_job_id(title, company, url, location):
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{url.strip()}|{location.lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def is_recent(posted_text):
    if not posted_text:
        return True

    posted_text = posted_text.lower().strip()

    if "just now" in posted_text or "hour" in posted_text or "today" in posted_text:
        return True

    if "day" in posted_text:
        try:
            days = int(posted_text.split()[0])
            return days <= MAX_AGE_DAYS
        except Exception:
            return True

    if "week" in posted_text or "month" in posted_text:
        return False

    return True


def scrape_linkedin(keyword, search_location):
    encoded_keyword = keyword.replace(" ", "%20")
    encoded_location = search_location.replace(" ", "%20").replace(",", "%2C")
    seconds = MAX_AGE_DAYS * 86400

    url = (
        f"https://www.linkedin.com/jobs/search/"
        f"?keywords={encoded_keyword}"
        f"&location={encoded_location}"
        f"&f_TPR=r{seconds}"
        f"&sortBy=DD"
    )

    print(f"🔍 LinkedIn: Searching for '{keyword}' in '{search_location}'...")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ⚠️  Request failed for '{keyword}' / '{search_location}': {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="base-card")

    if not job_cards:
        print(f"  ℹ️  No results found for '{keyword}' / '{search_location}'")
        return []

    jobs = []

    for card in job_cards:
        try:
            title_el = card.find("h3", class_="base-search-card__title")
            company_el = card.find("h4", class_="base-search-card__subtitle")
            location_el = card.find("span", class_="job-search-card__location")
            time_el = card.find("time")
            link_el = card.find("a", class_="base-card__full-link")

            title = title_el.get_text(strip=True) if title_el else ""
            company = company_el.get_text(strip=True) if company_el else ""
            location = location_el.get_text(strip=True) if location_el else ""
            posted = time_el.get_text(strip=True) if time_el else ""
            job_url = link_el["href"].split("?")[0] if link_el and link_el.get("href") else ""

            if not title or not company:
                continue
            if not is_recent(posted):
                continue

            jobs.append({
                "id": make_job_id(title, company, job_url, location),
                "title": title,
                "company": company,
                "location": location,
                "posted": posted,
                "url": job_url,
                "source": "LinkedIn",
                "keyword": keyword,
                "search_location": search_location,
            })
        except Exception as e:
            print(f"  ⚠️  Error parsing LinkedIn job card: {e}")
            continue

    print(f"  ✅ Found {len(jobs)} jobs for '{keyword}' in '{search_location}'")
    time.sleep(random.uniform(2, 4))
    return jobs


def scrape_all_linkedin():
    all_jobs = []
    seen_ids = set()

    for search_location in LINKEDIN_SEARCH_LOCATIONS:
        for keyword in SEARCH_KEYWORDS:
            jobs = scrape_linkedin(keyword, search_location)
            for job in jobs:
                if job["id"] not in seen_ids:
                    seen_ids.add(job["id"])
                    all_jobs.append(job)
            time.sleep(random.uniform(2, 5))

    print(f"\n📋 LinkedIn total: {len(all_jobs)} unique jobs found")
    return all_jobs
