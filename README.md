# Government Opportunity Monitoring Agent

This repository includes a simple script for monitoring U.S. government contract solicitations and grants relevant to Beverly Knits or similar textile businesses.

## Features
- Searches SAM.gov for open contract opportunities with keywords related to apparel and knit textiles.
- Searches Grants.gov for posted grants and filters out any opportunities estimated below $25,000.
- Limits results to opportunities in the United States.

## Requirements
- Python 3 with the `requests` library installed (`pip install requests`).
- A valid SAM.gov API key stored in the environment variable `SAM_API_KEY`.

## Usage
Run the script from the command line:

```bash
python monitor.py
```

The script prints a list of current opportunities for each keyword.

You can schedule this script with cron or another job scheduler to monitor for new opportunities regularly.
