from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_yellowpages_websites_selenium(search_term, location, max_results=10):
    search_term = search_term.replace(" ", "+")
    location = location.replace(" ", "+")
    url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    time.sleep(2)  # Wait for JS to load

    website_links = []
    listings = driver.find_elements(By.CLASS_NAME, "result")

    for listing in listings:
        try:
            website_tag = listing.find_element(By.CLASS_NAME, "track-visit-website")
            href = website_tag.get_attribute("href")
            if href and href not in website_links:
                website_links.append(href)
        except:
            continue
        if len(website_links) >= max_results:
            break

    driver.quit()
    return website_links
