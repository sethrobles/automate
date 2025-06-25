import streamlit as st
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph
import nest_asyncio
import os

nest_asyncio.apply()

# Load your API key (replace this with os.getenv if using .env)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

def scrape_scholarship(url):
    prompt = (
        "Extract all scholarship details including:\n"
        "- Scholarship name\n"
        "- Eligibility criteria\n"
        "- Award amount\n"
        "- Application process\n"
        "- Application start date (if listed)\n"
        "- Application deadline / end date (if listed)\n"
        "Provide the output in structured JSON."
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

# ---- Streamlit UI ----

st.title("Scholarship Scraper")

urls_input = st.text_area("Paste one or more scholarship URLs (one per line):")

if st.button("Scrape"):
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
    all_data = []

    with st.spinner("Scraping scholarships..."):
        for url in urls:
            st.text(f"Scraping: {url}")
            result = scrape_scholarship(url)
            all_data.extend(result)

    df = pd.DataFrame(all_data)
    st.success("Done!")

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="scholarships.csv",
        mime="text/csv",
    )
