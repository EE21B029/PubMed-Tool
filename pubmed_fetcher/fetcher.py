from typing import List, Dict, Any
import requests
import xmltodict
import re

URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_pubmed_ids(query: str, debug= False) -> List[str]:
    url = f"{URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 20
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    ids = data["esearchresult"]["idlist"]
    if debug:
        print("PubMed IDs:", ids)
    return ids

def fetch_paper_details(pubmed_ids: List[str], debug = False) -> List[Dict[str, Any]]:
    if not pubmed_ids:
        return []

    url = URL+"efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    xml_data = xmltodict.parse(response.content)

    articles = xml_data['PubmedArticleSet']['PubmedArticle']
    if isinstance(articles, dict):
        articles = [articles]

    results = []

    for article in articles:
        try:
            article_info = article["MedlineCitation"]["Article"]
            authors = article_info.get("AuthorList", {}).get("Author", [])
            if isinstance(authors, dict):
                authors = [authors]

            company_authors = []
            affiliations = []
            email = None

            for author in authors:
                aff = author.get("AffiliationInfo", [])
                if isinstance(aff, dict):
                    aff = [aff]

                for affs in aff:
                    aff_text = affs.get("Affiliation", "")
                    text = aff_text.lower()

                    if ("university" not in text and "college" not in text and "school" not in text and "hospital" not in text and"institute" not in text) and (
                        "pharma" in text or "biotech" in text or"inc" in text or "ltd" in text or"corp" in text or "gmbh" in text or "llc" in text):
                            name = (author.get('ForeName', '')+" "+ author.get('LastName', '')).strip()
                            company_authors.append(name)
                            affiliations.append(aff_text)

                    if "@" in aff_text:
                        match = re.search(r'[\w\.-]+@[\w\.-]+', aff_text)
                        if match and not email:
                            email = match.group(0)

            if company_authors:
                result = {
                    "PubmedID": article["MedlineCitation"].get("PMID", "#"),
                    "Title": article_info.get("ArticleTitle", "#"),
                    "Publication Date": article_info.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}),
                    "Non-academic Author(s)": "; ".join(company_authors),
                    "Company Affiliation(s)": "; ".join(affiliations),
                    "Corresponding Author Email": email or "Not found"
                }
                results.append(result)

        except Exception as e:
            if debug:
                print("Error parsing article:", e)
            continue

    return results
