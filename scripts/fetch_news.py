#!/usr/bin/env python3
"""Holt den Google-News-RSS-Feed und speichert die neuesten Beitraege als news.json."""
import json, re, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

FEED = ("https://news.google.com/rss/search?q=Asbest+OR+Schadstoffgutachten+OR+"
        "Gefahrstoffverordnung+OR+Asbestsanierung&hl=de&gl=DE&ceid=DE:de")

req = urllib.request.Request(FEED, headers={"User-Agent": "Mozilla/5.0 (news-fetch)"})
xml = urllib.request.urlopen(req, timeout=30).read()
root = ET.fromstring(xml)

items = []
for it in root.iter("item"):
    title = (it.findtext("title") or "").strip()
    src = (it.findtext("source") or "Google News").strip()
    title = re.sub(r"\s+-\s+[^-]+$", "", title)
    pub = it.findtext("pubDate") or ""
    try:
        date = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
    except Exception:
        date = ""
    items.append({"title": title, "link": (it.findtext("link") or "").strip(),
                  "source": src, "date": date})
    if len(items) == 6:
        break

if not items:
    raise SystemExit("Keine Beitraege im Feed – news.json bleibt unveraendert.")

with open("news.json", "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": items},
              f, ensure_ascii=False, indent=1)
print(f"{len(items)} Beitraege gespeichert.")
