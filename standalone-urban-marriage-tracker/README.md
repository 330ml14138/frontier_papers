# Standalone Urban Governance / Real Estate / Marriage Tracker

Tracks latest-issue TOC papers from selected domestic and international journals across economics, political science, public administration, sociology, urban studies, and housing studies.

Topics:

- 城市治理
- 房地产
- 婚姻

## Structure

- `scripts/update_urban_marriage_tracker.py`: updater script
- `data/urban_marriage_tracker.json`: generated data

## Usage

```powershell
python scripts\update_urban_marriage_tracker.py
```

Optional env vars:

- `KIMI_API_KEY`
- `KIMI_MODEL` (default: `moonshot-v1-8k`)
- `MAX_URBAN_MARRIAGE_PAPERS_PER_JOURNAL` (default: `12`)
- `MAX_ABSTRACT_TRANSLATE_CHARS` (default: `2500`)

Crossref is the default metadata source. Chinese journals are included in the tracked list; journals without reliable Crossref metadata will remain visible with an error note until a dedicated domestic data source is added.
