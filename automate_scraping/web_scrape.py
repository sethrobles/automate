import nest_asyncio
import pandas as pd
from scrapegraphai.graphs import SmartScraperGraph

from dotenv import load_dotenv
import os

# Define OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

nest_asyncio.apply()


# Load the input CSV with scholarship URLs
input_csv = "input_scholarships.csv"
df_input = pd.read_csv(input_csv)

# Define prompt
prompt = (
    "Extract all scholarship details including:\n"
    "- Scholarship name\n"
    "- Eligibility criteria\n"
    "- Award amount\n"
    "- Application process\n"
    "- Application start date (if listed)\n"
    "- Application deadline / end date (if listed)\n"
    "Provide the output in structured JSON with keys: "
    "'name', 'eligibility', 'amount', 'process', 'start_date', 'end_date'."
)

# List to collect all results
results = []

# Scrape each URL
for index, row in df_input.iterrows():
    url = row['url']
    print(f"🔍 Scraping: {url}")

    graph_config = {
        "llm": {
            "api_key": OPENAI_API_KEY,
            "model": "gpt-4o",
            "temperature": 0,
        },
        "verbose": False,
    }

    try:
        scraper = SmartScraperGraph(source=url, config=graph_config, prompt=prompt)
        data = scraper.run()

        # Normalize to a list of dicts
        if isinstance(data, dict):
            data = [data]

        for item in data:
            item["source_url"] = url  # Add the URL to each entry
            results.append(item)

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        results.append({
            "name": None,
            "eligibility": None,
            "amount": None,
            "process": None,
            "start_date": None,
            "end_date": None,
            "source_url": url,
            "error": str(e)
        })

# Save to CSV
df_output = pd.DataFrame(results)
df_output.to_csv("scholarship_output.csv", index=False)

print("✅ Done! Results saved to 'scholarship_output.csv'")




# import nest_asyncio
# from scrapegraphai.graphs import SmartScraperGraph
# import pandas as pd

# nest_asyncio.apply()

# # Define your OpenAI API key
# OPENAI_API_KEY = "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"

# # Define the URL of the scholarship page
# url = "https://www.thegatesscholarship.org/scholarship"

# # Configure the scraping task
# graph_config = {
#     "llm": {
#         "api_key": OPENAI_API_KEY,
#         "model": "gpt-4o",
#         "temperature": 0,
#     },
#     "verbose": True,
# }

# # Define the prompt
# prompt = (
#     "Extract all scholarship details including:\n"
#     "- Scholarship name\n"
#     "- Eligibility criteria\n"
#     "- Award amount\n"
#     "- Application process\n"
#     "- Application start date (if listed)\n"
#     "- Application deadline / end date (if listed)\n"
#     "Provide the output in a structured JSON format with keys: "
#     "'name', 'eligibility', 'amount', 'process', 'start_date', 'end_date'."
# )

# # Initialize the scraper
# smart_scraper = SmartScraperGraph(source=url, config=graph_config, prompt=prompt)

# # Run the scraper
# data = smart_scraper.run()

# # Ensure the data is in list-of-dicts format
# if isinstance(data, dict):
#     data = [data]

# # Convert to DataFrame and save to CSV
# df = pd.DataFrame(data)
# df.to_csv("scholarship_details.csv", index=False)

# print("✅ CSV saved as 'scholarship_details.csv'")
# print(df)
