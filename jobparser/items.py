import scrapy


class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    salary_from = scrapy.Field()
    salary_till = scrapy.Field()
    currency = scrapy.Field()
    link = scrapy.Field()
