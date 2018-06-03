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
            if i < 2:
                category_absolute_link = response.urljoin(category_link)
                yield scrapy.Request(url=category_absolute_link, callback=self.parse_category_page)

    def parse_category_page(self, response):
        topic_links = response.xpath('//*[contains(@class, "topic--title")]/../@href').extract()
        for topic_link in topic_links:
            topic_absolute_link = response.urljoin(topic_link)
            yield scrapy.Request(url=topic_absolute_link, callback=self.parse_topic_page)

    def parse_topic_page(self, response):
        topic_title = response.xpath('//*[contains(@class, "topic-title")]/a/text()').extract() 
        topic_message = response.xpath('//*[contains(@class, "post-message")]/p/text()').extract_first()
        topic_url = response.request.url
        yield{
            'title': topic_title,
            'body': topic_message,
            'url': topic_url
        }
        
