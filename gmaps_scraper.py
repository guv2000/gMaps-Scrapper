import csv
import os
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


@dataclass
class Business:
    business_id: str
    name: str
    address: str
    phone: str
    website: str
    category: str
    rating: str
    review_count: str
    hours: str
    lat: str
    lng: str
    source_url: str
    fetched_at: str


@dataclass
class Review:
    business_id: str
    review_id: str
    reviewer: str
    rating: str
    date: str
    text: str


@dataclass
class Photo:
    business_id: str
    photo_url: str


def prompt(text: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{text}{suffix}: ").strip()
    return value or (default or "")


def slugify(text: str) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in text.lower())
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe.strip("-")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def click_if_exists(locator, timeout: int = 2000) -> bool:
    try:
        locator.first.wait_for(timeout=timeout)
        locator.first.click()
        return True
    except PlaywrightTimeoutError:
        return False


def safe_text(locator, timeout: int = 1000) -> str:
    try:
        locator.first.wait_for(timeout=timeout)
        return locator.first.inner_text().strip()
    except PlaywrightTimeoutError:
        return ""


def safe_attr(locator, name: str, timeout: int = 1000) -> str:
    try:
        locator.first.wait_for(timeout=timeout)
        return locator.first.get_attribute(name) or ""
    except PlaywrightTimeoutError:
        return ""


def get_detail_text(page, data_item_id: str) -> str:
    return safe_text(page.locator(f"button[data-item-id='{data_item_id}']"))


def get_place_id_from_url(url: str) -> str:
    if "/place/" in url:
        return slugify(url.split("/place/")[-1].split("/")[0])
    return uuid.uuid4().hex


def scroll_results_list(page) -> None:
    feed = page.locator("div[role='feed']")
    feed.wait_for(timeout=10000)
    last_count = 0
    idle_rounds = 0

    while idle_rounds < 5:
        cards = feed.locator("div[role='article']")
        count = cards.count()
        if count == last_count:
            idle_rounds += 1
        else:
            idle_rounds = 0
            last_count = count
        page.evaluate(
            "el => { el.scrollBy(0, el.scrollHeight); }",
            feed,
        )
        time.sleep(1.2)


def collect_business_cards(page) -> Iterable:
    feed = page.locator("div[role='feed']")
    feed.wait_for(timeout=10000)
    return feed.locator("div[role='article']")


def open_reviews_panel(page) -> bool:
    return click_if_exists(page.locator("button[aria-label*='reviews']"), timeout=3000)


def open_photos_panel(page) -> bool:
    return click_if_exists(page.locator("button[aria-label*='photos']"), timeout=3000)


def scroll_panel(page, panel_selector: str, pause: float = 1.0, limit_rounds: int = 8) -> None:
    panel = page.locator(panel_selector)
    panel.wait_for(timeout=10000)
    last_height = 0
    idle_rounds = 0

    while idle_rounds < limit_rounds:
        height = panel.evaluate("el => el.scrollHeight")
        if height == last_height:
            idle_rounds += 1
        else:
            idle_rounds = 0
            last_height = height
        panel.evaluate("el => { el.scrollBy(0, el.scrollHeight); }")
        time.sleep(pause)


def extract_reviews(page, business_id: str) -> list[Review]:
    reviews: list[Review] = []
    if not open_reviews_panel(page):
        return reviews

    scroll_panel(page, "div[role='main']", pause=1.2, limit_rounds=10)
    review_cards = page.locator("div[data-review-id]")
    for idx in range(review_cards.count()):
        card = review_cards.nth(idx)
        review_id = card.get_attribute("data-review-id") or uuid.uuid4().hex
        reviewer = safe_text(card.locator(".d4r55"))
        rating = safe_attr(card.locator("span[role='img']"), "aria-label")
        date = safe_text(card.locator(".rsqaWe"))
        text = safe_text(card.locator(".MyEned"))
        reviews.append(
            Review(
                business_id=business_id,
                review_id=review_id,
                reviewer=reviewer,
                rating=rating,
                date=date,
                text=text,
            )
        )
    return reviews


def extract_photos(page, business_id: str) -> list[Photo]:
    photos: list[Photo] = []
    if not open_photos_panel(page):
        return photos

    scroll_panel(page, "div[role='main']", pause=1.2, limit_rounds=10)
    image_nodes = page.locator("img[src^='https://']")
    for idx in range(image_nodes.count()):
        src = image_nodes.nth(idx).get_attribute("src")
        if src and "googleusercontent" in src:
            photos.append(Photo(business_id=business_id, photo_url=src))
    return photos


def parse_lat_lng(url: str) -> tuple[str, str]:
    if "@" not in url:
        return "", ""
    try:
        coord_segment = url.split("@", 1)[1]
        lat, lng = coord_segment.split(",", 2)[:2]
        return lat, lng
    except ValueError:
        return "", ""


def extract_business(page) -> Business:
    name = safe_text(page.locator("h1"))
    address = get_detail_text(page, "address")
    phone = get_detail_text(page, "phone")
    website = safe_text(page.locator("a[data-item-id='authority']"))
    category = safe_text(page.locator("button[jsaction='pane.rating.category']"))
    rating = safe_text(page.locator("div[role='img'][aria-label*='stars']"))
    review_count = safe_text(page.locator("button[jsaction='pane.rating.moreReviews']"))
    hours = safe_text(page.locator("div[aria-label*='Hours']"))
    url = page.url
    business_id = get_place_id_from_url(url)
    lat, lng = parse_lat_lng(url)

    return Business(
        business_id=business_id,
        name=name,
        address=address,
        phone=phone,
        website=website,
        category=category,
        rating=rating,
        review_count=review_count,
        hours=hours,
        lat=lat,
        lng=lng,
        source_url=url,
        fetched_at=now_iso(),
    )


def write_csv(path: str, rows: list, headers: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def run() -> None:
    location = prompt("Location (e.g., fethiye)")
    query = prompt("Query (e.g., berber)")
    output_dir = prompt("Output directory", default="output")

    ensure_dir(output_dir)
    search_text = f"{query} {location}".strip()

    businesses: list[Business] = []
    reviews: list[Review] = []
    photos: list[Photo] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        page.wait_for_timeout(2000)

        search_box = page.locator("input[aria-label='Search Google Maps']")
        search_box.fill(search_text)
        search_box.press("Enter")
        page.wait_for_timeout(3000)

        scroll_results_list(page)
        cards = collect_business_cards(page)
        count = cards.count()

        for idx in range(count):
            card = cards.nth(idx)
            card.scroll_into_view_if_needed()
            card.click()
            page.wait_for_timeout(2000)

            business = extract_business(page)
            if business.name and business.address:
                businesses.append(business)
            else:
                continue

            reviews.extend(extract_reviews(page, business.business_id))
            photos.extend(extract_photos(page, business.business_id))

            page.keyboard.press("Escape")
            page.wait_for_timeout(500)

        browser.close()

    write_csv(
        os.path.join(output_dir, "businesses.csv"),
        businesses,
        list(Business.__annotations__.keys()),
    )
    write_csv(
        os.path.join(output_dir, "reviews.csv"),
        reviews,
        list(Review.__annotations__.keys()),
    )
    write_csv(
        os.path.join(output_dir, "photos.csv"),
        photos,
        list(Photo.__annotations__.keys()),
    )

    print(f"Saved {len(businesses)} businesses to {output_dir}.")
    print(f"Saved {len(reviews)} reviews to {output_dir}.")
    print(f"Saved {len(photos)} photos to {output_dir}.")


if __name__ == "__main__":
    run()
