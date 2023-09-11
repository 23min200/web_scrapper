from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver


def get_jobs_count(keyword):
    browser = webdriver.Chrome()
    browser.get(f"https://remoteok.com/remote-{keyword}-jobs")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    jobs = soup.find_all("tr", class_="job")
    results = []
    for job in jobs:
        anchor = job.find("a", class_="preventLink")
        link = anchor["href"]
        position = job.find("h2", itemprop="title").text.strip()
        company = job.find("h3", itemprop="name").text.strip()
        locations = [loc.text.strip()
                     for loc in job.find_all("div", class_="location")]

        job_data = {
            'link': f"https://remoteok.com/{link}",
            'company': company,
            'location': ', '.join(locations),
            'position': position
        }
        results.append(job_data)

    for result in results:
        print(result, "////////\n")
    return results


get_jobs_count("python")
