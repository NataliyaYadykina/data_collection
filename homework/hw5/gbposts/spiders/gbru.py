import scrapy
from scrapy.http import HtmlResponse
from ..items import GbpostsItem


class GbruSpider(scrapy.Spider):
    name = "gbru"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response: HtmlResponse):

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(self.start_urls, callback=self.parse)

        links = response.xpath(
            "//div[@class='image_container']/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.gb_parse)

    def gb_parse(self, response: HtmlResponse):
        title = response.xpath("//h1/text()").get()
        instock = response.xpath(
            "//p[@class='instock availability']/text()").get()
        url = response.url
        price = response.xpath("//p[@class='price_color']/text()").get()
        yield GbpostsItem(title=title, instock=instock, url=url, price=price)
