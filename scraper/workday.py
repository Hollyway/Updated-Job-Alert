# ============================================================
#  scraper/workday.py — Workday search for remote finance roles
# ============================================================

import hashlib
import random
import time

import requests

from config import SEARCH_KEYWORDS

WORKDAY_COMPANIES = [
    ("RBC", "rbc", "RBC_Careers"),
    ("TD Bank", "td", "TD_Careers"),
    ("CIBC", "cibc", "CIBC_Careers"),
    ("Scotiabank", "scotiabank", "Scotiabank_Careers"),
    ("BMO", "bmo", "BMO_Careers"),
    ("Manulife", "manulife", "MFC_Careers"),
    ("Sun Life", "sunlife", "SunLifeFinancial"),
    ("Intact", "intact", "Intact_Careers"),
    ("Mastercard", "mastercard", "CorporateCareers"),
    ("Shopify", "shopify", "shopify"),
    ("Rogers", "rogers", "Rogers_Careers"),
    ("Bell Canada", "bell", "BellCanada"),
    ("Telus", "telus", "TELUS_Careers"),
    ("Deloitte", "deloitte", "DeloitteUSCareers"),
    ("Accenture", "accenture", "AccentureCareers"),
    ("KPMG", "kpmg", "KPMG_Careers"),
    ("Metrolinx", "metrolinx", "Metrolinx_Careers"),
]

WD_VARIANTS = ["wd3", "wd1", "wd5"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Workday-Client-Application-Name": "Career Hub",
    "Referer": "https://www.myworkdayjobs.com/",
    "Origin": "https://www.myworkdayjobs.com",
}


def make_job_id(title, company, url, ext_path):
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{url.strip()}|{ext_path.strip()}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


def get_working_url(subdomain, careers_path):
    for wd in WD_VARIANTS:
        url = (
            f"https://{subdomain}.{wd}.myworkdayjobs.com"
            f"/wday/cxs/{subdomain}/{careers_path}/jobs"
        )
        try:
            response = requests.options(url, headers=HEADERS, timeout=8)
            if response.status_code not in [404, 400]:
                return url, wd
        except requests.RequestException:
            continue
    return None, None


def search_workday_company(company_name, subdomain, careers_path, keyword):
    api_url, wd = get_working_url(subdomain, careers_path)
    if not api_url:
        api_url = (
            f"https://{subdomain}.wd3.myworkdayjobs.com"
            f"/wday/cxs/{subdomain}/{careers_path}/jobs"
        )
        wd = "wd3"

    payload = {
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": keyword,
    }

    try:
        response = requests.post(api_url, json=payload, headers=HEADERS, timeout=15)
        if response.status_code in [404, 422, 400]:
            return []
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"  ⚠️  {company_name}: {e}")
        return []

    jobs = []
    for posting in data.get("jobPostings", []):
        title = posting.get("title", "")
        location = posting.get("locationsText", "")
        posted = posting.get("postedOn", "")
        ext_path = posting.get("externalPath", "")
        job_url = (
            f"https://{subdomain}.{wd}.myworkdayjobs.com/en-US/{careers_path}{ext_path}"
            if ext_path else ""
        )

        if not title:
            continue

        jobs.append({
            "id": make_job_id(title, company_name, job_url, ext_path),
            "title": title,
            "company": company_name,
            "location": location,
            "posted": posted,
            "url": job_url,
            "source": "Workday",
            "keyword": keyword,
        })

    return jobs


def scrape_all_workday():
    all_jobs = []
    seen_ids = set()

    print(f"\n🏢 Starting Workday scrape across {len(WORKDAY_COMPANIES)} companies...")

    for company_name, subdomain, careers_path in WORKDAY_COMPANIES:
        company_jobs = []
        for keyword in SEARCH_KEYWORDS:
            jobs = search_workday_company(company_name, subdomain, careers_path, keyword)
            company_jobs.extend(jobs)
            time.sleep(random.uniform(0.8, 1.6))

        for job in company_jobs:
            if job["id"] not in seen_ids:
                seen_ids.add(job["id"])
                all_jobs.append(job)

        if company_jobs:
            print(f"  ✅ {company_name}: {len(company_jobs)} jobs found")
        else:
            print(f"  ○  {company_name}: no matches")

        time.sleep(random.uniform(1, 2.2))

    print(f"\n📋 Workday total: {len(all_jobs)} unique jobs found")
    return all_jobs
