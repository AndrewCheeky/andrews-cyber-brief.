# 1. Configuration
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
ROOT = Path(__file__).resolve().parents[1]

# 2. Download and validate

def validate(data):
    items = data if isinstance(data, list) else [data]
    if not items:
        raise ValueError("Feed contains no items")
    now = datetime.now(timezone.utc)
    seen = set()
    for item in items:
        for key in ("uid", "updateDate", "titleText", "mainText", "redirectionUrl"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError("Missing required text field: " + key)
        if item["uid"] in seen:
            raise ValueError("Duplicate item identifier")
        seen.add(item["uid"])
        stamp = datetime.fromisoformat(item["updateDate"].replace("Z", "+00:00"))
        if stamp.tzinfo is None or not now - timedelta(days=7) < stamp <= now:
            raise ValueError("Publication date must be recent and not in the future")
        if not item["redirectionUrl"].startswith("https://"):
            raise ValueError("Read-more link must use HTTPS")
        if len(item["mainText"]) > 4500:
            raise ValueError("Spoken text exceeds 4500 characters")
        if item.get("streamUrl"):
            raise ValueError("Text feed must not include an audio stream")
    return sorted(items, key=lambda x: x["updateDate"], reverse=True)

# 3. Publish only a successful refresh

def main():
    url = (ROOT / "source-url.txt").read_text().strip()
    with urlopen(url, timeout=90) as response:
        data = json.load(response)
    items = validate(data)
    target = ROOT / "docs/briefing.json"
    temporary = target.with_suffix(".tmp")
    temporary.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)
    test = [{"uid": "andrew-diagnostic-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
             "updateDate": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "titleText": "Andrew's Cyber Brief Test",
             "mainText": "Hello Andrew. Your GitHub hosted cyber briefing test is working.",
             "redirectionUrl": "https://andrewcheeky.com"}]
    (ROOT / "docs/test.json").write_text(json.dumps(test, indent=2) + "\n")
    print("Validated and prepared", len(items), "briefing item(s)")

# 4. Entry point
if __name__ == "__main__":
    main()
