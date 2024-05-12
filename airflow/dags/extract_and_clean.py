import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_and_clean(url, limit=10):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    articles = soup.find_all('article')[:limit]
    data = []
    for article in articles:
        title = article.find('h3').get_text().strip()
        description = article.find('p').get_text().strip()
        data.append({'title': title, 'description': description})
    return data

def clean_data(data):
    # Perform data cleaning here (e.g., remove special characters, HTML tags, etc.)
    # This is just a placeholder, you can customize as needed
    cleaned_data = []
    for item in data:
        cleaned_title = item['title'].replace('<', '').replace('>', '')
        cleaned_description = item['description'].replace('<', '').replace('>', '')
        cleaned_data.append({'title': cleaned_title, 'description': cleaned_description})
    return cleaned_data

def store_to_csv(data, filepath):
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

if __name__ == "__main__":
    # Example usage
    url = 'https://www.dawn.com/'  # Change URL as needed
    cleaned_data = clean_data(extract_and_clean(url))
    filepath = 'extracted_data.csv'  # Change filepath as needed
    store_to_csv(cleaned_data, filepath)
