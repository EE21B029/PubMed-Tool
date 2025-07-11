# cli.py

import argparse
import csv
from pubmed_fetcher.fetcher import fetch_pubmed_ids, fetch_paper_details

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with company authors.")
    parser.add_argument("query", type=str, help="Search term for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Save results to CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logs")
    args = parser.parse_args()

    ids = fetch_pubmed_ids(args.query, debug=args.debug)
    results = fetch_paper_details(ids, debug=args.debug)

    if not results:
        print("No matching papers with company authors found.")
        return

    if args.file:
        with open(args.file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {args.file}")
    else:
        for row in results:
            for key, value in row.items():
                print(f"{key}: {value}")
            print("-" * 40)

if __name__ == "__main__":
    main()
