import os
import argparse
import requests

SAM_API_URL = "https://api.sam.gov/prod/opportunities/v2/search"
GRANTS_API_URL = "https://apply07.grants.gov/grantsws/rest/opportunities/search"

def search_sam(keyword, limit=10):
    api_key = os.getenv("SAM_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the SAM_API_KEY environment variable")
    params = {
        "api_key": api_key,
        "q": keyword,
        "limit": limit,
        "offset": 0,
        "postedFrom": "TODAY-30DAYS",
        "placeOfPerformanceCountryCode": "USA"
    }
    resp = requests.get(SAM_API_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    return data.get("opportunitiesData", [])

def search_grants(keyword, rows=10):
    payload = {
        "keyword": keyword,
        "opportunityStatus": "posted",
        "startRecordNum": 0,
        "maxRecords": rows,
        "fundingOppNum": "",
        "cfda": "",
    }
    resp = requests.post(GRANTS_API_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("oppHits", [])

def format_grant(grant):
    opp_num = grant.get("number")
    title = grant.get("title")
    close_date = grant.get("closeDate")
    return f"- {opp_num}: {title} (closes {close_date})"


def format_notice(notice):
    notice_id = notice.get("noticeId")
    title = notice.get("title")
    close_date = notice.get("responseDate")
    return f"- {notice_id}: {title} (closes {close_date})"


def main():
    parser = argparse.ArgumentParser(description="Monitor SAM.gov and Grants.gov for opportunities")
    parser.add_argument(
        "keywords",
        nargs="*",
        default=["apparel", "knit textiles", "Berry Amendment"],
        help="keywords to search for",
    )
    args = parser.parse_args()

    for kw in args.keywords:
        print(f"\nSAM.gov results for '{kw}':")
        try:
            for opp in search_sam(kw):
                print(format_notice(opp))
        except Exception as exc:
            print(f"Failed to fetch SAM.gov results: {exc}")

        print(f"\nGrants.gov results for '{kw}':")
        try:
            for grant in search_grants(kw):
                est = grant.get("estimatedFunding")
                if est:
                    try:
                        amount = float(est.replace("$", "").replace(",", ""))
                    except ValueError:
                        amount = 0
                    if amount < 25000:
                        continue
                print(format_grant(grant))
        except Exception as exc:
            print(f"Failed to fetch Grants.gov results: {exc}")

if __name__ == "__main__":
    main()
