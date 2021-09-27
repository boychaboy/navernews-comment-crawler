from pathlib import Path
from time import time
from typing import List

import scrapy
from lxml import html
from navernews_comment.data import Corpus
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class NavernewsScraper:
    def __init__(self):
        # chromedriver setting
        PKG_DIR = Path(__file__).parents[2]
        CHROMEDRIVER_PATH = f"{PKG_DIR}/chromedriver"
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        self.driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options
        )
        self.driver.implicitly_wait(1)

    def _get_article_urls_per_page(self):
        root = html.fromstring(self.driver.page_source)
        _article_urls = root.xpath('//*[@id="news_result_list"]/li/div[1]/a/@href')
        # filter out news outside naver news
        article_urls = []
        for url in _article_urls:
            if url.startswith("https://n.news.naver.com/") or url.startswith(
                "https://m.news.naver.com/"
            ):
                article_urls.append(url)
        return article_urls

    def get_article_urls(self) -> List[str]:
        """Crawl all available article urls"""
        article_urls = []
        start_time = time()
        keyword = input("Keyword: ")
        # 210825 first keywords
        #  domains = {
        #       "gender": ["백래시", "페미니즘", "여성혐오", "여성단체"],
        #       "xenophobia": ["이민자", "난민", "중국동포", "외국인 근로자"],
        #       "sexual_orientation": ["차별금지법", "동성혼", "퀴어", "퀴어 활동가", "성소수자"],
        #  }
        #  for key in domains.keys():
        #      print(f"Domain : {key}")
        #      queries = domains[key]
        #      for query in queries:
        # 210927 beep-title-keyword
        keywords = ["성추행", "해명", "반응", "공식입장", "노출", "컴백", "부인", "시청률", "단톡방"]
        max_articles_per_keyword = 100
        for keyword in keywords:
            num_articles = 0
            print(f"Scraping with keyword {keyword}...")
            # use mobile link
            NEWS_URL = f"https://m.search.naver.com/search.naver?where=m_news&sm=mtb_nmr&query={keyword}&sort=0&nso=so:r,p:1y"
            self.driver.get(NEWS_URL)
            self.driver.implicitly_wait(1)
            page = 1
            while True:
                article_urls_per_page = self._get_article_urls_per_page()
                article_urls.extend(article_urls_per_page)
                num_articles += len(article_urls_per_page)

                try:
                    last_page = self.driver.find_element_by_class_name(
                        "btn_next"
                    ).get_attribute("aria-disabled")
                    if last_page != "true":
                        # go to next page
                        self.driver.find_element_by_xpath(
                            '//*[@id="ct"]/div[3]/div/div/button[2]/i'
                        ).click()
                        self.driver.implicitly_wait(3)
                        page += 1
                    else:
                        # break when last page
                        print("Done!")
                        break
                except:
                    # break when no next page
                    print("Done!")
                    break
                if num_articles > max_articles_per_keyword:
                    break
            print(f"Total : {num_articles} \t time elapsed: {time() - start_time}")
            print(f"Total Articles : {len(article_urls)}")
        return article_urls


class NavernewsSpider(scrapy.Spider):
    def __init__(self):
        # chromedriver setting
        PKG_DIR = Path(__file__).parents[2]
        CHROMEDRIVER_PATH = f"{PKG_DIR}/chromedriver"
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")

        self.driver = webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options
        )
        self.driver.implicitly_wait(1)

    name = "navernews"
    url_scraper = NavernewsScraper()
    start_urls = url_scraper.get_article_urls()

    def parse(self, response):
        title = response.xpath('//*[@id="ct"]/div[1]/div[2]/h2/text()').get()
        date = response.xpath(
            '//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/text()'
        ).get()
        if date and (date[0].isalpha() or len(date.split("."))) < 2:
            date = response.xpath(
                '//*[@id="ct"]/div[1]/div[3]/div[1]/div/span[2]/text()'
            ).get()
        self.driver.get(response.url)
        self.driver.implicitly_wait(1)
        # check if there are comments

        flag = 0
        try:
            self.driver.find_element_by_xpath('//*[@id="comment_count"]').click()
            flag = 1
        except:
            print("No comments")

        if flag == 1:
            comments = []
            while True:
                try:
                    btn_more = self.driver.find_element_by_css_selector(
                        "a.u_cbox_btn_more"
                    )
                    btn_more.click()
                    self.driver.implicitly_wait(1)
                except:
                    break
            dabgul_btns = self.driver.find_elements_by_xpath(
                '//*[@id="cbox_module_wai_u_cbox_content_wrap_tabpanel"]/ul/li/div[1]/div/div[4]/a/strong'
            )
            for dabgul_btn in dabgul_btns:
                dabgul_btn.click()

            comments_per_page = self.driver.find_elements_by_class_name(
                "u_cbox_contents"
            )
            for comment in comments_per_page:
                comments.append(comment.text)
            num_comments = len(comments)
            print(f"Number of comments : {len(comments)}")
            comments = "[SEP]".join(comments)
        else:
            comments = ""
            num_comments = 0

        corpus = Corpus(
            title=title,
            date=date,
            corpus_source="네이버뉴스",
            num_comments=num_comments,
            comments=comments,
        )
        yield corpus.asdict()
