import os
import argparse
import requests
import datetime
import time

SAM_API_URL = "https://api.sam.gov/prod/opportunities/v2/search"
GRANTS_API_URL = "https://apply07.grants.gov/grantsws/rest/opportunities/search"


def _request_with_retry(method, url, *, retries=3, **kwargs):
    for attempt in range(retries):
        resp = requests.request(method, url, **kwargs)
        if resp.status_code == 429 and attempt < retries - 1:
            time.sleep(1)
            continue
        resp.raise_for_status()
        return resp
    return resp

def search_sam(keyword, limit=10, days=30):
    api_key = os.getenv("SAM_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the SAM_API_KEY environment variable")
    today = datetime.date.today()
    posted_from = (today - datetime.timedelta(days=days)).strftime("%m/%d/%Y")
    posted_to = today.strftime("%m/%d/%Y")
    params = {
        "api_key": api_key,
        "q": keyword,
        "limit": limit,
        "offset": 0,
        "postedFrom": posted_from,
        "postedTo": posted_to,
        "placeOfPerformanceCountryCode": "USA"
    }
    resp = _request_with_retry("get", SAM_API_URL, params=params)
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
    resp = _request_with_retry("post", GRANTS_API_URL, json=payload)
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
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="how many days back to search SAM.gov",
    )
    parser.add_argument(
        "--min-grant",
        type=float,
        default=25000,
        help="minimum estimated funding for grants.gov results",
    )
    args = parser.parse_args()

    for kw in args.keywords:
        print(f"\nSAM.gov results for '{kw}':")
        try:
            for opp in search_sam(kw, days=args.days):
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
                    if amount < args.min_grant:
                        continue
                print(format_grant(grant))
        except Exception as exc:
            print(f"Failed to fetch Grants.gov results: {exc}")

if __name__ == "__main__":
    main()
