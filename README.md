# Remote Finance & Business Ops Alert Bot

Standalone GitHub Actions bot for:
- fully remote roles worldwide
- Ontario hybrid roles
- finance, business analyst, PMO, strategy, operations, and transformation roles

## Files
- `main.py` — orchestrates the run
- `scraper/` — LinkedIn, Workday, and Canada Job Bank scrapers
- `filter.py` — keeps only remote roles or Ontario hybrid roles
- `deduplicator.py` — stores previously emailed jobs in `seen_jobs_remote.json`
- `.github/workflows/daily_remote_alert.yml` — scheduled workflow

## GitHub setup
1. Create a new repo.
2. Upload these files, keeping the same folder structure.
3. Add GitHub Actions secret `GMAIL_APP_PASSWORD`.
4. Run the workflow manually once.
