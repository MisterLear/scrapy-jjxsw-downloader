# -*- coding: utf-8 -*-
import scrapy
from xsdownloader.custom import PAGE_COUNT, GENRE


class JjxswSpider(scrapy.Spider):
    name = 'jjxsw'
    allowed_domains = ['www.jjxsw.la']
    start_urls = ['https://www.jjxsw.la']

    def parse(self, response):
        # txt/{}[/index_]*[\d+]*\.html
        for page in range(PAGE_COUNT + 1):
            url = self.start_urls[0] + "/txt/" + GENRE + "/index_{}.html".format(page)
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_page)


    def parse_page(self, response):
        book_list = response.xpath(""".//*[@id="catalog"]//div/span[contains(text(), "荐")]/../a""")
        for book in book_list:
            href = book.xpath("""@href""").extract()[0]
            title = book.xpath("""@title""").extract()[0]
            print(title)
            url = self.start_urls[0] + href
            yield scrapy.Request(url=url, callback=self.parse_item, meta={'book_title': title}, dont_filter=True)

    def parse_item(self, response):
        title = response.meta['book_title']
        download_href = response.xpath("""//*[@id="mainstory"]/ul[1]/li[1]/a/@href""").extract()[0]
        url = self.start_urls[0] + download_href
        yield scrapy.Request(url=url, meta={'book_title': title}, dont_filter=True)