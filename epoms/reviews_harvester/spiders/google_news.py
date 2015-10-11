import scrapy
from reviews_harvester.items import ResultItem
import re
import base64
import os.path


class GoogleReviewsSpider(scrapy.Spider):
    name = "google_reviews"
    start_urls = []
    base_url = "https://www.google.nl/search?hl=en&gl=us&ie=UTF-8&num=100&q={0}&oq={1}"
    with open("reviews_harvester/product_categories.txt") as f:
        for line in f:
            line = line.strip() + " reviews"
            if line == "":
                continue
            query = line.replace(" ", "%20")
            url = base_url.format(query, query)
            start_urls.append(url)

    def __init__(self):
        self.p = re.compile('/url\?q=(.*)&sa=U&ved')
        self.added = {}

    def extract_link(self, sel):
        google_url = str(sel.xpath('@href').extract()[0])
        m = self.p.match(google_url)
        return m.group(1)

    def generate_filename(self, link):
        return "reviews_harvester/output/" + base64.urlsafe_b64encode(link) + ".html"

    def parse(self, response):
        for href in response.xpath('//a[@class="fl"]/@href'):  # pages 2...n-1
            url = response.urljoin(href.extract())
            # yield scrapy.Request(url, callback=self.parse_results_page)
        yield scrapy.Request(response.url, callback=self.parse_results_page)

    def parse_results_page(self, response):
        for sel in response.xpath('//li[@class="g"]//a[1]'):
            item = ResultItem()
            item['title'] = "".join(sel.xpath('text()').extract())
            item['link'] = self.extract_link(sel)
            item['filename'] = self.generate_filename(item['link'])
            if item['filename'] not in self.added:
                self.added[item['filename']] = True
                yield scrapy.Request(item['link'], callback=self.parse_article)
                yield item

    def parse_article(self, response):
        filename = self.generate_filename(response.url)
        if not os.path.isfile(filename):
            with open(filename, 'wb') as f:
                f.write(response.body)
