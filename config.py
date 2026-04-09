# ============================================================
#  config.py — Remote Finance, BA & Ops Alert Preferences
# ============================================================

ALERT_NAME = "Remote Finance & Business Ops Alert"
ALERT_EMAIL = "oladeleolamide14@gmail.com"
SENDER_EMAIL = "oladeleolamide14@gmail.com"
MIN_JOBS_TO_EMAIL = 1
MAX_AGE_DAYS = 2
SEEN_JOBS_FILE = "seen_jobs_remote.json"

# LinkedIn search locations:
# - Remote: catches fully remote roles worldwide
# - Ontario, Canada: lets us catch Ontario hybrid roles
LINKEDIN_SEARCH_LOCATIONS = [
    "Remote",
    "Ontario, Canada",
]

# Job Bank is Canada-specific, so keep it broad enough to catch
# remote or Ontario hybrid opportunities.
JOBBANK_LOCATION = "Ontario"
JOBBANK_DISTANCE_KM = "500"

# Primary search phrases sent to the scrapers.
SEARCH_KEYWORDS = [
    # Strategy & Operations
    "Strategy and Operations",
    "Business Operations",
    "Operations Strategy",
    "Strategy Analyst",
    "Senior Analyst Operations",
    "Business Operations Lead",
    "Go-to-Market Strategy",
    "Revenue Operations",
    "BizOps",
    "Biz Ops",

    # Business Analyst / BSA
    "Business Analyst",
    "Business Systems Analyst",
    "Senior Business Analyst",
    "BSA",
    "Requirements Analyst",

    # Project / Program / Delivery
    "Project Manager",
    "Senior Project Manager",
    "Program Manager",
    "Project Management",
    "Delivery Manager",

    # Process / Implementation
    "Process Improvement",
    "Process Excellence",
    "Continuous Improvement",
    "Lean Six Sigma",
    "Operational Excellence",
    "Process Optimization",
    "Implementation Manager",
    "Implementation Analyst",
    "Onboarding Manager",
    "Client Implementation",
    "Technical Implementation",

    # Broader analyst titles
    "Senior Analyst",
    "Senior Operations Analyst",
    "Senior Strategy Analyst",
    "Senior Business Operations",

    # New finance titles you asked to add
    "Finance Transformation Analyst",
    "Business Analyst Finance",
    "Project Analyst Finance",
    "Financial Operations Analyst",
    "PMO Analyst",
    "Strategy Analyst Financial Services",
    "Business Performance Analyst",
]

# Substrings used during filtering so titles do not need to match
# the search phrases exactly.
TITLE_FRAGMENTS = [
    "strategy",
    "operations",
    "business operations",
    "bizops",
    "biz ops",
    "business analyst",
    "business systems analyst",
    "requirements analyst",
    "project manager",
    "program manager",
    "delivery manager",
    "process improvement",
    "process excellence",
    "continuous improvement",
    "lean six sigma",
    "operational excellence",
    "process optimization",
    "implementation",
    "onboarding",
    "operations analyst",
    "strategy analyst",
    "finance transformation analyst",
    "financial operations analyst",
    "business performance analyst",
    "pmo analyst",
    "project analyst",
]

FINANCE_DOMAIN_TERMS = [
    "finance",
    "financial",
    "bank",
    "banking",
    "insurance",
    "treasury",
    "capital markets",
    "wealth",
    "commercial banking",
    "retail banking",
]

# Titles that we will allow when paired with a finance-oriented
# company or finance domain signal.
FINANCE_CONDITIONAL_TITLES = [
    "strategy analyst",
    "pmo analyst",
    "project analyst",
    "business analyst",
]

SENIORITY_EXCLUDE = [
    "vice president",
    "vp",
    "chief",
    "intern",
    "co-op",
    "coop",
    "junior",
    "entry level",
    "entry-level",
    "student",
]

PRIORITY_COMPANIES = [
    # Banks / Finserv
    "RBC", "Royal Bank", "TD", "TD Bank", "CIBC", "Scotiabank", "BMO",
    "Manulife", "Sun Life", "Canada Life", "Great-West Life", "Intact", "Aviva",
    "Wealthsimple", "Interac", "Mastercard", "Visa", "American Express",
    "EQ Bank", "Neo Financial", "Tangerine",

    # Consulting / transformation
    "Deloitte", "KPMG", "PwC", "EY", "Accenture", "IBM", "CGI", "Capgemini",

    # Broader employers still relevant to your mix
    "Shopify", "Dentalcorp", "Rogers", "Bell", "TELUS", "Metrolinx",
]

COMPANIES_TO_SKIP = []

REMOTE_PHRASES = [
    "remote",
    "work from home",
    "wfh",
    "virtual",
    "distributed",
    "anywhere",
    "home-based",
    "telecommute",
]

HYBRID_PHRASES = [
    "hybrid",
    "flexible",
]

ALLOW_ONTARIO_HYBRID = True

ONTARIO_LOCATION_MARKERS = [
    "ontario",
    "on, canada",
    "toronto",
    "north york",
    "mississauga",
    "markham",
    "vaughan",
    "oakville",
    "brampton",
    "scarborough",
    "richmond hill",
    "waterloo",
    "kitchener",
    "hamilton",
    "ottawa",
    "peterborough",
]
