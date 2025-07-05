# selenium_temuscraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

def scrape_top5_temuproducts(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)  # let JS and lazy-loading finish

    products = driver.find_elements(By.CSS_SELECTOR, "a._2Tl9qLr1")[:5]
    results = []

    for prod in products:
        title = prod.get_attribute("aria-label") or prod.text.strip()
        href = prod.get_attribute("href")
        price_el = prod.find_element(By.XPATH, ".//following::span[contains(@class, '_2de9ERAH')][1]")
        price = price_el.text.strip() if price_el else None
        img_el = prod.find_element(By.XPATH, ".//img")
        img_url = img_el.get_attribute("src") if img_el else None

        results.append({
            "title": title,
            "price": price,
            "product_url": href,
            "image_url": img_url
        })

    driver.quit()
    return results

if __name__ == "__main__":
    url = "https://www.temu.com/search_result.html?search_key=shampoo%20for%20dry%20scalp..."
    top5 = scrape_top5_temuproducts(url)
    print(json.dumps(top5, indent=2))
