from langchain_community.tools import DuckDuckGoSearchRun

from langchain.tools import Tool

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

def save_to_txt(data: str, filename: str = "leads_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Leads Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

def scrape_website(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r'\s+', ' ', text)  

        return text[:5000]
    except Exception as e:
        return f"Error scraping website: {e}"

def generate_search_queries(company_name: str) -> list[str]:
    keywords = ["IT Services", "managed IT", "technology solutions"]
    return [f"{company_name} {keyword}" for keyword in keywords]

def search_and_scrape(company_name: str) -> str:
    queries = generate_search_queries(company_name)
    results = []

    for query in queries:
        search_results = search.run(query)

        urls = re.findall(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            search_results
        )

        if urls:
            results.append(scrape_website(urls[0]))

    return " ".join(results)

search = DuckDuckGoSearchRun()


search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

scrape_tool = Tool(
    name="scrape_website",
    func=search_and_scrape,
    description="Scrape the content of a website and search for related information.",
)

save_tool = Tool(
    name="save",
    func=save_to_txt,
    description="Saves structured data to a text file.",
)