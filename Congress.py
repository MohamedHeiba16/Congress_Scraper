import os
from playwright.sync_api import sync_playwright
import requests as r
from bs4 import BeautifulSoup

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Cookie': 'AMCV_0D15148954E6C5100A4C98BC%40AdobeOrg=179643557%7CMCIDTS%7C19679%7CMCMID%7C04909859418672808692672071132721940625%7CMCAAMLH-1700936768%7C6%7CMCAAMB-1700936768%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1700339168s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-19686%7CvVersion%7C5.5.0; s_ecid=MCMID%7C04909859418672808692672071132721940625; __cf_bm=YgeRX4WetuPPiLsFc1_o4sWjpJF45GgTgeYzlkjFQcc-1700574817-0-AdtTeHexcSNntAOfims00sngznDPPITUXmxgo+g26N5kAhfysYpYJElsffgcMzIT4JzLniss+PsRAECVOd6PXG8=; __cfruid=5a6c1f14d091e0db5fb4e8b7359d0085674c0371-1700574817; __cf_bm=DagqMGDrMe5kWa8hZkDdibP79MT3qtOjnarWuKkAHY8-1700574870-0-ASAKO8wqxCghiZ+mNC3D9GvJSkaV2o2u55aAMBz7ESxHtrc03bcczkfmIlhwwOqEf1W7BC1HSsphO27HltVMbY8=',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-User': '?1',
  'If-Modified-Since': 'Wed, 07 Jul 2021 12:49:06 GMT',
  'If-None-Match': '"1538-5c687f6c1297a-gzip"',
  'TE': 'trailers'
}

def extract_full_body_html(url):
    
    with sync_playwright() as p :
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)

        page.wait_for_load_state("networkidle")
        page.wait_for_selector("ol li.expanded")

        # page.screenshot(path="steam.png",full_page=True)  

        return page.inner_html("body")
    

def budget(html):
    soup = BeautifulSoup(html, 'lxml')
    empty_list = []

    # Assuming the 'li.expanded div.quick-search-member div img' elements are the ones you want to target
    containers = soup.select("li.expanded div.quick-search-member div img")

    for container in containers:
        url = container['src']
        relative_url = "https://www.congress.gov" + url
        empty_list.append(relative_url)

    return empty_list


def save_imgs(imgurls, dest_dir="images"):
    
    for url in imgurls:
        resp = r.get(url,headers=headers)
    
        file_name = url.split("/")[-1]

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(f"{dest_dir}/{file_name}.jpg", "wb") as f:
            f.write(resp.content)
            

if __name__ == "__main__" :
    for page in range(1,26):
        url = f"https://www.congress.gov/members?page={page}"
        html = extract_full_body_html(url)
        img_urls = budget(html)
        print(img_urls)
        save_imgs(img_urls, dest_dir="output")

        