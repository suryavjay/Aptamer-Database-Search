# Load environment variables from .env file

from dotenv import load_dotenv
import os
import requests
import xml.etree.ElementTree as ET
import pandas as pd

load_dotenv()
api_key = os.getenv("NCBI_API_KEY")
email = os.getenv("NCBI_EMAIL")

# write the esearch

params = {
    "db": "pubmed",
    "term": '(aptamer[Title/Abstract] OR aptamers[Title/Abstract]) AND thrombin[Title/Abstract] AND ("1990"[Date - Publication] : "2026"[Date - Publication])',
    "retmax": 10,
    "api_key": api_key,
    "email": email,
    "retmode": "json"
}

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

response = requests.get(base_url, params=params)

# parse the json data into a python dictionary

data = response.json()

print(data)

# build the pmid list

pmids = data["esearchresult"]["idlist"]

print(pmids)

# write the efetch

params_efetch = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "retmode": "xml",
    "api_key": api_key,
    "email": email,
    "rettype": "abstract"
}

ef_response = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi", params=params_efetch)

# parse the xml data into a python dictionary

ef_data = ef_response.text

print(ef_data)

ef_root = ET.fromstring(ef_data)

articles = ef_root.findall(".//PubmedArticle")


# extract the relevant information from each article and store it in a list of dictionaries

records = []

for article in articles:
    pmid = article.find(".//PMID").text
    title = article.find(".//ArticleTitle").text
    parts = [p.text for p in article.findall(".//Abstract/AbstractText") if p.text is not None]
    abstract = " ".join(parts) if parts else "No abstract available"
    year = article.find(".//PubDate/Year").text if article.find(".//PubDate/Year") is not None else "No year available"
    record = {
    "PMID": pmid,
    "Title": title,
    "Abstract": abstract,
    "Year": year
    }
    records.append(record)

# create a pandas dataframe from the list of dictionaries

df = pd.DataFrame(records)
df.to_excel("pubmed_aptamer_thrombin.xlsx", index=False)