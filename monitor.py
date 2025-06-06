import os
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

def main():
    keywords = ["apparel", "knit textiles", "Berry Amendment"]
    for kw in keywords:
        print(f"\nSAM.gov results for '{kw}':")
        for opp in search_sam(kw):
            notice_id = opp.get("noticeId")
            title = opp.get("title")
            close_date = opp.get("responseDate")
            print(f"- {notice_id}: {title} (closes {close_date})")
        print(f"\nGrants.gov results for '{kw}':")
        for grant in search_grants(kw):
            opp_num = grant.get("number")
            title = grant.get("title")
            close_date = grant.get("closeDate")
            estimated_funding = grant.get("estimatedFunding")
            if estimated_funding:
                try:
                    amount = float(estimated_funding.replace("$", "").replace(",", ""))
                except ValueError:
                    amount = 0
                if amount < 25000:
                    continue
            print(f"- {opp_num}: {title} (closes {close_date})")

if __name__ == "__main__":
    main()
