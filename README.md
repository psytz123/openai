# Government Opportunity Monitoring Agent

This repository includes a simple script for monitoring U.S. government contract solicitations and grants relevant to Beverly Knits or similar textile businesses.

## Features
- Searches SAM.gov for open contract opportunities with keywords related to apparel and knit textiles.
- Searches Grants.gov for posted grants and filters out any opportunities estimated below $25,000.
- Limits results to opportunities in the United States.

## Requirements
- Python 3 with the `requests` library installed (`pip install requests`).
- A valid SAM.gov API key stored in the environment variable `SAM_API_KEY`. You can request a key for free from [SAM.gov](https://sam.gov/content/api).

## Usage
Run the script from the command line. You can optionally provide search keywords,
a minimum grant amount, and a date range:

```bash
python monitor.py berry textile "technical apparel" --min-grant 25000 --days 15
```

If no keywords are supplied, the script searches for `apparel`, `knit textiles`, and `Berry Amendment` by default. The `--days` flag controls how many days back the SAM.gov search goes (30 days by default).

Use the optional `--min-grant` argument to filter out grants estimated below the given dollar amount (defaults to $25,000).

The script prints a list of current opportunities for each keyword.

You can schedule this script with cron or another job scheduler to monitor for new opportunities regularly.
