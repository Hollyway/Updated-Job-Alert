# ============================================================
#  emailer.py — send a clean HTML digest
# ============================================================

import html
import os
import smtplib
from collections import Counter
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import ALERT_EMAIL, ALERT_NAME, SENDER_EMAIL



def build_html_email(jobs):
    date_str = datetime.now().strftime("%B %d, %Y")
    count = len(jobs)

    source_counts = Counter(job.get("source", "Unknown") for job in jobs)
    source_pills = "".join(
        f'<span style="background:#1B3A5C; color:white; padding:3px 10px; '
        f'border-radius:12px; font-size:12px; margin-right:6px;">'
        f'{html.escape(source)}: {cnt}</span>'
        for source, cnt in sorted(source_counts.items())
    )

    html_body = f"""
    <html><body style="font-family: Arial, sans-serif; background: #f5f7fa; padding: 20px;">
    <div style="max-width: 700px; margin: 0 auto; background: white;
                border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
      <div style="background: #0D2B45; padding: 28px 32px;">
        <h1 style="color: white; margin: 0; font-size: 22px;">🌍 Remote Finance &amp; Business Ops Alert</h1>
        <p style="color: #A8D8E8; margin: 6px 0 12px 0; font-size: 14px;">
          {date_str} &nbsp;·&nbsp; {count} new role{'s' if count != 1 else ''} found
        </p>
        <p style="color: #D7F0FF; margin: 0 0 12px 0; font-size: 13px;">
          Remote worldwide, plus Ontario hybrid roles
        </p>
        <div>{source_pills}</div>
      </div>
    """

    for job in jobs:
        title = html.escape(job.get("title", "Unknown Title"))
        company = html.escape(job.get("company", "Unknown Company"))
        location = html.escape(job.get("location", ""))
        posted = html.escape(job.get("posted", ""))
        source = html.escape(job.get("source", ""))
        url = html.escape(job.get("url", "#"), quote=True)
        priority = job.get("priority", False)

        badge = """
          <span style="background: #F0A500; color: white; font-size: 11px;
                       padding: 2px 8px; border-radius: 12px; margin-left: 8px;">
            ⭐ Priority
          </span>
        """ if priority else ""

        meta_parts = []
        if location:
            meta_parts.append(f"📍 {location}")
        if posted:
            meta_parts.append(f"🕐 {posted}")
        if source:
            meta_parts.append(f"via {source}")
        meta_line = " &nbsp;·&nbsp; ".join(meta_parts)

        html_body += f"""
      <div style="padding: 20px 32px; border-bottom: 1px solid #EEF1F5;">
        <h2 style="margin: 0 0 4px 0; font-size: 17px; color: #0D2B45;">
          {title}{badge}
        </h2>
        <p style="margin: 0; color: #0E7C86; font-size: 15px; font-weight: bold;">
          {company}
        </p>
        <p style="margin: 6px 0 0 0; color: #888; font-size: 13px;">
          {meta_line}
        </p>
        <a href="{url}"
           style="display: inline-block; margin-top: 14px; padding: 8px 20px;
                  background: #0D2B45; color: white; text-decoration: none;
                  border-radius: 5px; font-size: 13px; font-weight: bold;">
          View Job →
        </a>
      </div>
        """

    html_body += """
      <div style="padding: 20px 32px; background: #f5f7fa;">
        <p style="color: #999; font-size: 12px; margin: 0;">
          Sent by your Job Alert Bot · Running on GitHub Actions · Jobs already seen will not be re-sent
        </p>
      </div>
    </div>
    </body></html>
    """
    return html_body



def send_email(jobs):
    gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_password:
        print("❌ GMAIL_APP_PASSWORD not found in environment.")
        print("   Add it in GitHub → Settings → Secrets and variables → Actions")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = (
        f"🌍 {len(jobs)} New Remote Finance / Ops Role{'s' if len(jobs) != 1 else ''}"
        f" — {datetime.now().strftime('%b %d')}"
    )
    msg["From"] = SENDER_EMAIL
    msg["To"] = ALERT_EMAIL
    msg.attach(MIMEText(build_html_email(jobs), "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, gmail_password)
            server.sendmail(SENDER_EMAIL, ALERT_EMAIL, msg.as_string())
        print(f"✅ {ALERT_NAME}: email sent to {ALERT_EMAIL} with {len(jobs)} jobs")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise
