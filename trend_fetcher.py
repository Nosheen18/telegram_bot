import requests
from bs4 import BeautifulSoup

def fetch_trends(industry):
    url = "https://databox.com/ppc-industry-benchmarks"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract industry-specific CPC data (example logic)
    industry_trend = {
        "Construction": {"CPC": 2.5, "CTR": 3.2},
        "Retail": {"CPC": 1.8, "CTR": 4.1}
    }

    return industry_trend.get(industry, {"CPC": "N/A", "CTR": "N/A"})
