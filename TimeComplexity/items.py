# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field



class ContainerItem(scrapy.Item):
    container_name=Field()
    find_time = Field()
    insert_time = Field()
    erase_time = Field()