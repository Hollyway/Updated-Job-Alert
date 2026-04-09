# ============================================================
#  deduplicator.py — track jobs already emailed
# ============================================================

import json
import os
from config import SEEN_JOBS_FILE



def load_seen_jobs():
    if not os.path.exists(SEEN_JOBS_FILE):
        return set()

    try:
        with open(SEEN_JOBS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return set()

    return set(data.get("job_ids", []))



def save_seen_jobs(seen_ids):
    payload = {"job_ids": sorted(seen_ids)}
    with open(SEEN_JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)



def filter_new_jobs(jobs, seen_ids):
    new_jobs = []
    updated_seen = set(seen_ids)

    for job in jobs:
        job_id = job.get("id")
        if not job_id:
            continue
        if job_id in updated_seen:
            continue
        new_jobs.append(job)
        updated_seen.add(job_id)

    return new_jobs, updated_seen
