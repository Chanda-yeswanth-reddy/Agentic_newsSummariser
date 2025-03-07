from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.newspaper4k import Newspaper4k

# Load environment variables
load_dotenv()
NEWS_API_KEY = ""

app = Flask(__name__)

# Initialize PhiData Agent
agent = Agent(
    tools=[Newspaper4k()],
    model=Groq(id="llama-3.3-70b-versatile"),
    debug_mode=False,
    show_tool_calls=False
)

# Function to fetch news
def fetch_news(category="technology", country="us", page_size=3):
    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return []  # Return empty if API fails

    return data.get("articles", [])

# Function to summarize news
def summarise_news(url):
    response = agent.run(f"Please summarize {url}")
    return response.content if response else "Summary not available"

# Flask route
@app.route("/", methods=["GET", "POST"])
def index():
    articles = []
    summaries = {}

    if request.method == "POST":
        category = request.form.get("category", "technology")
        articles = fetch_news(category=category)

        if not articles:
            return render_template("index.html", articles=[], summaries={})  # Prevent error

        for article in articles:
            summaries[article["title"]] = summarise_news(article["url"])

    return render_template("index.html", articles=articles, summaries=summaries)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
