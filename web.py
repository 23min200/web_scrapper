from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver


def get_page_count(keyword):
    browser = webdriver.Chrome()
    browser.get(f"https://kr.indeed.com/jobs?q={keyword}")
    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagintaion = soup.find("nav", class_="ecydgvn0")
    if pagintaion == None:
        return 1
    pages = pagintaion.find_all("div", reccursive=False)
    count = len(pages)

    if count >= 5:
        return 5
    else:
        return count


def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        browser = webdriver.Chrome()
        final_url = (f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}")
        print("Requesting", final_url)
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="eu4oa1w0")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")

                job_data = {
                    'link': f"https://kr.indeed.com/{link}",
                    'compnay': company.string,
                    'location': location.string,
                    'position': title
                }
                results.append(job_data)
        for result in results:
            print(result, "////////\n")
        while (True):
            pass
    return results


jobs = extract_indeed_jobs("python")

print(jobs)
