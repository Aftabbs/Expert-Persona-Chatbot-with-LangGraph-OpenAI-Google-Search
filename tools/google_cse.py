import os, requests, random, time, re

API_URL = "https://www.googleapis.com/customsearch/v1"
RETRY_STATUS = {429, 500, 502, 503, 504}

def _jitter(attempt): return min(30, (2 ** attempt) + random.random())

class GoogleCSEClient:
    def __init__(self):
        self.key = os.getenv("GOOGLE_API_KEY")
        self.cse = os.getenv("GOOGLE_CSE_ID")
        if not self.key or not self.cse:
            raise ValueError("Missing GOOGLE_API_KEY / GOOGLE_CSE_ID")

    def search(self, q: str, num: int = 6, site=None, date=None):
        parts = [q] + ([f"site:{site}"] if site else [])
        params = {"q": " ".join(parts), "num": num, "key": self.key, "cx": self.cse}
        if date: params["dateRestrict"] = date
        for attempt in range(3):
            r = requests.get(API_URL, params=params, timeout=15)
            if r.status_code == 200: return r.json()
            if r.status_code in RETRY_STATUS: time.sleep(_jitter(attempt))
        r.raise_for_status()
