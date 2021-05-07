import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import re

# Future TODOS:
#   Make it so it can search for any job not just "Tableau Developer" and in any location
#   Attempt to code the pagination portion, which just requires adding "start = 10"
#   Provide a way for people to put their own file name (if name == __main__ function should do this)
#   Provide "memory" which checks how old the previous version of the copy is and re-runs script based on that
#   Long-term create API through FLASK or other systems
url = "https://ca.indeed.com/jobs?q=Tableau+Developer&rbl=Toronto,+ON&jlid=aaab304de0fc22ae"

page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")


def extract_job_loc_summa_dates(soup):
    jobs = []
    locations = []
    summaries = []
    dates = []
    for index, div in enumerate(soup.find_all(name = "div", attrs={"class": "jobsearch-SerpJobCard unifiedRow row result"})):
        for a in div.find_all(name = "a", attrs={"class": "jobtitle turnstileLink"}):
            jobs.append(a["title"])
        for location in div.find_all(name = "div", attrs={"class": "sjcl"}):
            for locale in location.find_all(name = "div", attrs={"class": "recJobLoc"}):
                locations.append(locale['data-rc-loc'])
        for summary in div.find_all(name = "div", attrs={"class": "summary"}):
            summaries.append(summary.text.strip())
        for date_info in div.find_all(name = "div", attrs={"class": "jobsearch-SerpJobCard-footer"}):
            date_ = str(re.match(pattern = r"[^S]*", string=date_info.text).group(0)).strip()
            if date_ == "Today" or date_ == "Just posted":
                dates.append("0 days ago")
            else:
                dates.append(date_)
    out_df = pd.DataFrame(data = [jobs, locations, summaries, dates])
    out_df = out_df.T
    out_df = out_df.rename(columns ={0:'jobs', 1:'locations', 2:'summaries', 3:'dates'})
    print(out_df)

    return out_df

def dataframe_to_csv(df, provided_name):
    df.to_csv(f"{provided_name}.csv", index=False)

test = 'daily_job_posting'
dataframe_to_csv(extract_job_loc_summa_dates(soup), test)