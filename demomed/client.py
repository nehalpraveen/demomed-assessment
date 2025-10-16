from __future__ import annotations
import os, time
import requests
from typing import Dict, Any, List

BASE_URL = os.getenv("DEMOMED_BASE_URL", "https://assessment.ksensetech.com/api")
API_KEY  = os.getenv("DEMOMED_API_KEY", "")

HEADERS = {"x-api-key": API_KEY}

class DemoMedClient:
    def __init__(self, base_url: str = BASE_URL, headers: Dict[str, str] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or HEADERS
        if not self.headers.get("x-api-key"):
            raise RuntimeError("DEMOMED_API_KEY missing. Put it in .env or env vars.")

    def _get(self, path: str, params: Dict[str, Any] = None, retries: int = 4) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        backoff = 1.0
        for attempt in range(retries):
            try:
                r = requests.get(url, headers=self.headers, params=params, timeout=12)
                if r.status_code == 200: return r.json()
                if r.status_code in (429, 500, 503):
                    time.sleep(backoff); backoff *= 2; continue
                r.raise_for_status()
            except requests.RequestException as e:
                if attempt == retries - 1: raise
                time.sleep(backoff); backoff *= 2
        return {}

    def list_patients(self, limit: int = 10) -> List[Dict[str, Any]]:
        page, all_rows = 1, []
        while True:
            data = self._get("/patients", {"page": page, "limit": limit})
            rows = (data or {}).get("data") or []
            if not rows: break
            all_rows.extend(rows)
            page += 1
        return all_rows

    def submit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/submit-assessment"
        r = requests.post(url, headers={**self.headers, "Content-Type":"application/json"}, json=payload, timeout=15)
        r.raise_for_status()
        return r.json()
