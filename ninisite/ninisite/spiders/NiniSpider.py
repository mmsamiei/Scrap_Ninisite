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
        topic_subjects = response.xpath('//*[@class="topic_subject"]/text()').extract()
        for topic_subject in topic_subjects:
            print("\n")
            print(topic_subject)
            print("\n")