from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.newspaper4k import Newspaper4k
import requests
import os
from dotenv import load_dotenv
NEWS_API_KEY=""
load_dotenv()

def fetch_news(category="technology", country="us", page_size=5):
    """Fetch top headlines from a specific category and country."""
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    if data["status"] != "ok":
        print("Error fetching news:", data.get("message", "Unknown error"))
        return []

    return data["articles"]

# Example Usage
articles = fetch_news(category="technology", country="us", page_size=3)
if articles:
    agent=Agent(tools=[Newspaper4k()],
    model = Groq(id="llama-3.3-70b-versatile"),
    debug_mode=True,
    show_tool_calls=True)
    for idx, article in enumerate(articles, start=1):
        print(f"{idx}. {article['title']}")
        print(f"   🔗 {article['url']}\n")
        agent.print_response(f"Please summarize {article['url']}")

    
else:
    print("No articles found.")