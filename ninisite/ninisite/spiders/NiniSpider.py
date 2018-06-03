import scrapy
from pymongo import MongoClient
from scrapy.conf import settings


class NiniSpider(scrapy.Spider):
    name = "NiniSpider"

    def __init__(self):
        connection = MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

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
            if i < 3:
                category_absolute_link = response.urljoin(category_link)
                yield scrapy.Request(url=category_absolute_link, callback=self.parse_category_page)

    def parse_category_page(self, response):
        topic_links = response.xpath('//*[contains(@class, "topic--title")]/../@href').extract()
        first_topic_absolute_link = response.urljoin(topic_links[0])
        is_old = self.collection.find({'url':first_topic_absolute_link}).count()
        if is_old != 0:
            for topic_link in topic_links:
                topic_absolute_link = response.urljoin(topic_link)
                yield scrapy.Request(url=topic_absolute_link, callback=self.parse_topic_page)
                #TODO go to next page!

    def parse_topic_page(self, response):
        topic_title = response.xpath('//*[contains(@class, "topic-title")]/a/text()').extract_first() 
        main_post_message = response.xpath('//*[contains(@class, "post-message")]')[0]
        main_post_message_text = ' '.join(main_post_message.xpath('./p/text()').extract())
        topic_url = response.request.url
        yield{
            'title': topic_title,
            'body': main_post_message_text,
            'url': topic_url
        }
        
