import scrapy


class NiniSpider(scrapy.Spider):
    name = "NiniSpider"

    def start_requests(self):
        urls = [
            'https://www.ninisite.com/discussion/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_homepage)

    def parse_homepage(self, response):
        categories_link = response.xpath('//*[@class="category--title"]/@href').extract()
        i = 0 
        for category_link in categories_link:
            i = i + 1
            if i < 11:
                category_absolute_link = response.urljoin(category_link)
                yield scrapy.Request(url=category_absolute_link, callback=self.parse_category_page)

    def parse_category_page(self, response):
        topic_titles = response.xpath('//*[contains(@class, "topic--title")]/span/text()').extract()
        topic_links = response.xpath('//*[contains(@class, "topic--title")]/../@href').extract()
        for topic_title in topic_titles:
            print("\n")
            print(topic_title)
            print("\n")