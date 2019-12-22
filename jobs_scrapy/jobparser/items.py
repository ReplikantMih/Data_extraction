import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join



class JobparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    salary_from = scrapy.Field(output_processor=TakeFirst())
    salary_till = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
