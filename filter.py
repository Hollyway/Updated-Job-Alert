# ============================================================
#  filter.py — Keep remote roles + Ontario hybrid only
# ============================================================

from config import (
    TITLE_FRAGMENTS,
    FINANCE_DOMAIN_TERMS,
    FINANCE_CONDITIONAL_TITLES,
    SENIORITY_EXCLUDE,
    PRIORITY_COMPANIES,
    COMPANIES_TO_SKIP,
    REMOTE_PHRASES,
    HYBRID_PHRASES,
    ONTARIO_LOCATION_MARKERS,
    ALLOW_ONTARIO_HYBRID,
)


def contains_any(text, terms):
    text = (text or "").lower()
    return any(term.lower() in text for term in terms)



def is_priority_company(company):
    company = (company or "").lower()
    return any(priority.lower() in company for priority in PRIORITY_COMPANIES)



def has_remote_or_allowed_hybrid(job):
    title = job.get("title", "")
    location = job.get("location", "")
    combined = f"{title} {location}".lower()

    if contains_any(combined, REMOTE_PHRASES):
        return True

    if (
        ALLOW_ONTARIO_HYBRID
        and contains_any(combined, HYBRID_PHRASES)
        and contains_any(combined, ONTARIO_LOCATION_MARKERS)
    ):
        return True

    return False



def title_is_relevant(job):
    title = (job.get("title", "") or "").lower()
    company = (job.get("company", "") or "").lower()
    location = (job.get("location", "") or "").lower()
    combined = f"{title} {company} {location}"

    # Direct title fragment match
    if contains_any(title, TITLE_FRAGMENTS):
        return True

    # Finance-conditional titles such as PMO Analyst / Strategy Analyst
    # should pass only when the company or context is finance-oriented.
    if contains_any(title, FINANCE_CONDITIONAL_TITLES) and (
        contains_any(combined, FINANCE_DOMAIN_TERMS) or is_priority_company(company)
    ):
        return True

    return False



def is_relevant(job):
    title = (job.get("title", "") or "").lower()
    company = (job.get("company", "") or "").lower()

    if not has_remote_or_allowed_hybrid(job):
        return False

    if any(skip.lower() in company for skip in COMPANIES_TO_SKIP):
        return False

    if any(exclude in title for exclude in SENIORITY_EXCLUDE):
        return False

    if title_is_relevant(job):
        return True

    # Priority companies still need a role signal, not just any job.
    if is_priority_company(company) and any(
        token in title for token in [
            "analyst", "manager", "lead", "specialist", "consultant",
            "project", "program", "operations", "strategy", "finance",
            "implementation", "transformation", "business"
        ]
    ):
        return True

    return False



def apply_filters(jobs):
    filtered = []

    for job in jobs:
        if is_relevant(job):
            job["priority"] = is_priority_company(job.get("company", ""))
            filtered.append(job)

    return filtered
