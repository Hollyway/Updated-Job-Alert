# ============================================================
#  main.py — Remote finance alert orchestrator
# ============================================================

from scraper.linkedin import scrape_all_linkedin
from scraper.workday import scrape_all_workday
from scraper.jobbank import scrape_all_jobbank
from filter import apply_filters
from deduplicator import load_seen_jobs, save_seen_jobs, filter_new_jobs
from emailer import send_email
from config import MIN_JOBS_TO_EMAIL


def safe_scrape(label, fn):
    try:
        results = fn()
        return results if results else []
    except Exception as e:
        print(f"  ❌ {label} scraper failed: {e}")
        return []


def main():
    print("=" * 60)
    print("  🌍 Remote Finance & Business Ops Job Alert — Starting")
    print("  📡 Running across 3 sources")
    print("=" * 60)

    seen_ids = load_seen_jobs()

    print("\n📡 SCRAPING JOB BOARDS...")
    linkedin_jobs = safe_scrape("LinkedIn", scrape_all_linkedin)
    workday_jobs = safe_scrape("Workday", scrape_all_workday)
    jobbank_jobs = safe_scrape("Canada Job Bank", scrape_all_jobbank)

    all_raw_jobs = linkedin_jobs + workday_jobs + jobbank_jobs

    print("\n📦 SCRAPE SUMMARY:")
    print(f"  LinkedIn:         {len(linkedin_jobs)} jobs")
    print(f"  Workday:          {len(workday_jobs)} jobs")
    print(f"  Canada Job Bank:  {len(jobbank_jobs)} jobs")
    print("  ─────────────────────────────────")
    print(f"  Total raw:        {len(all_raw_jobs)} jobs")

    if not all_raw_jobs:
        save_seen_jobs(seen_ids)
        print("\n⚠️  No jobs scraped from any source.")
        return

    print("\n🔎 APPLYING FILTERS...")
    filtered_jobs = apply_filters(all_raw_jobs)
    print(f"✅ Jobs after filtering: {len(filtered_jobs)}")

    new_jobs, updated_seen = filter_new_jobs(filtered_jobs, seen_ids)
    print(f"🆕 New jobs (not previously emailed): {len(new_jobs)}")

    if len(new_jobs) >= MIN_JOBS_TO_EMAIL:
        print(f"\n📧 SENDING EMAIL with {len(new_jobs)} new jobs...")
        send_email(new_jobs)
    else:
        print(
            f"\n💤 Only {len(new_jobs)} new job(s) found. "
            f"Minimum threshold is {MIN_JOBS_TO_EMAIL}. No email sent."
        )

    save_seen_jobs(updated_seen)
    print("\n💾 seen_jobs_remote.json updated.")
    print("\n" + "=" * 60)
    print("  ✅ Remote job alert run complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
