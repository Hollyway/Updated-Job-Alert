# ============================================================
#  scraper/jobbank.py — Canada Job Bank for Ontario-focused roles
# ============================================================

import hashlib
import random
import re
import time
import xml.etree.ElementTree as ET

import requests

from config import JOBBANK_DISTANCE_KM, JOBBANK_LOCATION, SEARCH_KEYWORDS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}

BASE_URL = "https://www.jobbank.gc.ca/rss/jobsearch.rss"


def make_job_id(title, company, guid, url):
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{guid.strip()}|{url.strip()}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def extract_company(description):
    if not description:
        return ""
    match = re.search(r"(?:Employer|Company)[:\s]+([^\n<]+)", description, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"<b>([^<]+)</b>", description)
    return match.group(1).strip() if match else ""


def scrape_jobbank(keyword):
    params = {
        "searchstring": keyword,
        "locationstring": JOBBANK_LOCATION,
        "distance": JOBBANK_DISTANCE_KM,
        "sort": "M",
    }

    print(f"🔍 Job Bank: Searching for '{keyword}'...")

    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  ⚠️  Job Bank request failed for '{keyword}': {e}")
        return []

    try:
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        print(f"  ⚠️  Job Bank XML parse error for '{keyword}': {e}")
        return []

    channel = root.find("channel")
    if channel is None:
        return []

    jobs = []
    for item in channel.findall("item"):
        title = item.findtext("title", "").strip()
        job_url = item.findtext("link", "").strip()
        description = item.findtext("description", "")
        pub_date = item.findtext("pubDate", "").strip()
        guid = item.findtext("guid", "").strip()

        parts = title.split(" - ")
        job_title = parts[0].strip() if parts else title
        location = parts[1].strip() if len(parts) > 1 else JOBBANK_LOCATION
        company = extract_company(description) or "See posting"

        if not job_title:
            continue

        jobs.append({
            "id": make_job_id(job_title, company, guid, job_url),
            "title": job_title,
            "company": company,
            "location": location,
            "posted": pub_date[:16] if pub_date else "",
            "url": job_url,
            "source": "Canada Job Bank",
            "keyword": keyword,
        })

    print(f"  ✅ Found {len(jobs)} jobs for '{keyword}'")
    time.sleep(random.uniform(0.8, 1.6))
    return jobs


def scrape_all_jobbank():
    all_jobs = []
    seen_ids = set()

    keywords_to_search = SEARCH_KEYWORDS[:18]
    print(f"\n🇨🇦 Starting Canada Job Bank scrape for {len(keywords_to_search)} keywords...")

    for keyword in keywords_to_search:
        jobs = scrape_jobbank(keyword)
        for job in jobs:
            if job["id"] not in seen_ids:
                seen_ids.add(job["id"])
                all_jobs.append(job)
        time.sleep(random.uniform(0.8, 1.4))

    print(f"\n📋 Canada Job Bank total: {len(all_jobs)} unique jobs found")
    return all_jobs
