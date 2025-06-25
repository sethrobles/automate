import streamlit as st
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph
import nest_asyncio
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time

nest_asyncio.apply()

# Load your API key (replace with os.getenv or Streamlit secrets in prod)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# ---- Web Scraper Using Selenium ----
def get_yellowpages_websites_selenium(search_term, location, max_results=10):
    search_term = search_term.replace(" ", "+")
    location = location.replace(" ", "+")
    url = f"https://www.yellowpages.com/search?search_terms={search_term}&geo_location_terms={location}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(2)

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

# ---- Analyzer ----
def analyze_company_site(url):
    prompt = (
        "Extract details about this business including:\n"
        "- Business name\n"
        "- Industry or field\n"
        "- Services offered\n"
        "- Contact information (email, phone)\n"
        "- Whether they already use a chatbot or have a contact form\n\n"
        "Then, suggest one or more ways a chatbot could improve their site based on what you find."
        "Output should be structured JSON."
    )

    graph_config = {
        "llm": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o",
            "temperature": 0,
        },
        "verbose": False,
    }

    graph = SmartScraperGraph(source=url, config=graph_config, prompt=prompt)

    try:
        data = graph.run()
        if isinstance(data, dict):
            data = [data]
        for entry in data:
            entry['source_url'] = url
        return data
    except Exception as e:
        return [{"error": str(e), "source_url": url}]

# ---- Streamlit App ----
st.title("🤖 AI Automation Opportunity Finder")

USE_API = st.checkbox("Use OpenAI API for Analysis", value=True)

# ----- Option A: Search YellowPages -----
st.header("🔍 Find Businesses from YellowPages")

with st.form("search_form"):
    search_term = st.text_input("Business type (e.g., dermatologist, plumber)")
    location = st.text_input("Location (e.g., Houston, TX)")
    max_results = st.slider("How many businesses?", 1, 25, 5)
    submitted = st.form_submit_button("Search and Analyze")

if submitted:
    st.info(f"Searching for {search_term} businesses in {location}...")
    try:
        urls = get_yellowpages_websites_selenium(search_term, location, max_results)
    except Exception as e:
        st.error(f"Failed to search: {e}")
        urls = []

    if not urls:
        st.warning("No business websites found.")
    else:
        st.success(f"Found {len(urls)} websites. Analyzing now...")
        all_data = []

        with st.spinner("Analyzing business sites..."):
            for url in urls:
                st.text(f"Analyzing: {url}")
                if USE_API:
                    result = analyze_company_site(url)
                    all_data.extend(result)
                else:
                    st.warning(f"Skipped API call for {url} (API usage disabled)")

        if all_data:
            df = pd.DataFrame(all_data)
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv,
                file_name="chatbot_opportunities.csv",
                mime="text/csv",
            )
        else:
            st.info("No analysis results to display.")

# ----- Option B: Manual URLs -----
st.header("📎 Or Paste Business URLs Manually")

urls_input = st.text_area("Paste one or more business URLs (one per line):")

if st.button("Analyze Pasted Sites"):
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    all_data = []

    with st.spinner("Analyzing business sites..."):
        for url in urls:
            st.text(f"Analyzing: {url}")
            if USE_API:
                result = analyze_company_site(url)
                all_data.extend(result)
            else:
                st.warning(f"Skipped API call for {url} (API usage disabled)")

    if all_data:
        df = pd.DataFrame(all_data)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="chatbot_opportunities.csv",
            mime="text/csv",
        )
    else:
        st.info("No analysis results to display.")
