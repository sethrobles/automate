import requests
from bs4 import BeautifulSoup
import time

headers = {"User-Agent": "Mozilla/5.0"}


# Gets the yellow page URL based on a search term and location
def get_yellowpages_business_listing_urls(search_term, location, max_results=10):
    search_term = search_term.replace(' ', '+')
    location = location.replace(' ', '+')
    url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    business_urls = []

    for link in soup.find_all("a", class_="business-name", href=True):
        href = link["href"]
        full_url = f"https://www.yellowpages.com{href}"
        if full_url not in business_urls:
            business_urls.append(full_url)
        if len(business_urls) >= max_results:
            break

    return business_urls


# Gets an actual website from a yellowpage website listing
def get_actual_website_from_listing(listing_url):
    try:
        r = requests.get(listing_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        # Look for the actual business website
        website_tag = soup.find("a", class_="primary-btn website-link", href=True)
        if website_tag:
            return website_tag["href"]
    except Exception as e:
        print(f"Error processing {listing_url}: {e}")

    return None



# 🧪 Combine both stages
def get_business_websites(search_term, location, max_results=10):
    listings = get_yellowpages_business_listing_urls(search_term, location, max_results)
    websites = []

    for listing in listings:
        print(f"Checking listing: {listing}")
        website = get_actual_website_from_listing(listing)
        if website:
            print(f" → Found website: {website}")
            websites.append(website)
        else:
            print(" → No website found.")
        time.sleep(1)  # polite scraping

    return websites


# Example usage
business_sites = get_business_websites("dermatology", "Houston, TX", max_results=5)
print("\nFinal websites:")
for site in business_sites:
    print(site)
