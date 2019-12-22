import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def process_price(price):
    try:
        price = int(price)
        return price
    except:
        print(f'Цена получена в неверном формате: {price}')
    return 'NaN'


def process_geo(geo):
    return ' '.join(geo.split())


class AvitoparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    price = scrapy.Field(input_processor=MapCompose(process_price), output_processor=TakeFirst())
    geo = scrapy.Field(input_processor=MapCompose(process_geo), output_processor=TakeFirst())
    description = scrapy.Field(output_processor=Join(' '))