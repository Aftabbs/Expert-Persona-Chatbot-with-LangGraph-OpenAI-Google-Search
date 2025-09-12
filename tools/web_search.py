# tools/web_search.py
from __future__ import annotations
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from .google_cse import GoogleCSEClient

@tool("web_search", return_direct=False)
def web_search(
    q: str,
    num: int = 6,
    date: Optional[str] = "m6",
    filetype: Optional[str] = None,
    sites: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Google Custom Search (CSE).
    Args:
      q: main query
      num: number of results
      date: dateRestrict (d7, m1, m3, m6, y1)
      filetype: optional 'pdf', etc.
      sites: optional list of domains to prioritize (runs multiple queries and merges)
    """
    client = GoogleCSEClient()
    results: Dict[str, Any] = {"query": q, "items": [], "total_results": 0}

    if sites:
        seen = set()
        for s in sites[:6]:
            r = client.search(q, num=max(2, num // min(len(sites), 6)), site=s, date=date, filetype=filetype, rerank=True)
            for it in r["items"]:
                if it["link"] not in seen:
                    results["items"].append(it); seen.add(it["link"])
            results["total_results"] += r.get("total_results", 0)
        return results

    return client.search(q, num=num, date=date, filetype=filetype, rerank=True)
