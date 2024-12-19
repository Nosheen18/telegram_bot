from bs4 import BeautifulSoup
import requests

def generate_keywords(industry, objective, website=None, social_media=None, ppc_data=None, target_audience=None, location=None):

    predefined_keywords = {
        "Construction": ["building materials", "construction tools", "civil engineering"],
        "Retail": ["e-commerce", "shopping deals", "retail trends"]
    }

    if website:
        response = requests.get(website)
        soup = BeautifulSoup(response.text, 'html.parser')

    keywords = predefined_keywords.get(industry, ["default keywords"])
    return {"keywords": keywords, "suggestions": ["Optimize PPC for better reach", "Focus on local SEO"]}

