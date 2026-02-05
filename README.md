# gMaps-Scrapper

> **Note:** Google Maps has Terms of Service that may restrict automated access. Use this project responsibly and comply with all applicable laws and policies.

## Overview
This repository provides a **Python + Playwright** CLI tool that:
- Prompts for search terms (e.g., `fethiye` + `berber`).
- Scrolls the left-hand results list to load all businesses.
- Visits each business card and captures available details.
- Optionally collects **all reviews** and **photo URLs**.
- Exports data to CSV files.

## Requirements
- Python 3.10+
- Playwright browsers installed

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install
```

## Usage
```bash
python gmaps_scraper.py
```
You will be prompted for:
- Location (e.g., `fethiye`)
- Query (e.g., `berber`)
- Output directory (defaults to `output`)

Outputs:
- `businesses.csv`
- `reviews.csv`
- `photos.csv`

## CSV Columns
### `businesses.csv`
- `business_id`, `name`, `address`, `phone`, `website`, `category`, `rating`, `review_count`, `hours`, `lat`, `lng`, `source_url`, `fetched_at`

### `reviews.csv`
- `business_id`, `review_id`, `reviewer`, `rating`, `date`, `text`

### `photos.csv`
- `business_id`, `photo_url`

## Tips to Reduce Blocks
- Run in **headed** mode (default).
- Keep your search volume modest.
- Avoid rapid, high-parallel scraping.

## Disclaimer
This tool is intended for legitimate data collection. Ensure you have the right to collect and use the data for your directory.
