# PubMed-Tool

A Python CLI tool to search PubMed for articles, filter out academic-only papers, identify those with at least one **company-affiliated** author, extract author names and contact emails, and export the results to a CSV file.

Built using `requests`, regex, and CLI tooling — packaged and managed using **Poetry**.

---

##  Features

-  Search PubMed with any keyword or phrase
-  Filter results to include only articles with **company-affiliated** authors
-  Automatically skip purely academic papers
-  Extract:
  - Author names
  - Affiliations
  - Contact emails (via regex)
-  Export all data to a clean, structured **CSV file**

---

##  Tech Stack

- **Language**: Python 3.8+
- **Dependencies**: `requests`
- **Tooling**: Poetry for dependency & project management

---
##  Usage

You can run the CLI tool in two ways:

### With Poetry

If you're using Poetry (recommended):

```bash
 poetry run get-papers-list "your query"
```
### Without Poetry

```bash
python cli.py "your query" -f results.csv

