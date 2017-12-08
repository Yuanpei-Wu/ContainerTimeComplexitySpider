# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

from urlparse import urljoin
from scrapy.http import Request
import json
from TimeComplexity.items import ContainerItem


class ReferenceSpider(scrapy.Spider):
    name = 'reference'
    allowed_domains = ['cplusplus.com']  #allowed_domain不能加http://前缀!
    start_urls = ['http://www.cplusplus.com/reference/stl/']

    def parse(self, response):

        next_urls = response.xpath('//div[@id="I_content"]//b[contains(text(),"Associative")]//following-sibling::dl[@class="links"]//a/@href').extract()
        for next_url in next_urls:
            container_name=next_url.split('/')[2]
            find_url= "http://www.cplusplus.com"+next_url+"find/"
            yield Request(find_url,callback=self.parse_middle,meta={'path_type':'find_time','container_name':container_name})
            insert_url="http://www.cplusplus.com"+next_url+"insert/"
            yield Request(insert_url,callback=self.parse_middle,meta={'path_type':'insert_time','container_name':container_name})
            erase_url = "http://www.cplusplus.com" + next_url + "erase/"
            yield Request(erase_url, callback=self.parse_middle,meta={'path_type':'erase_time','container_name':container_name})

    def parse_middle(self,response):
        result=response.xpath('//section[@id="complexity"]/text() | //section[@id="complexity"]/a/text()').extract()
        path_type=response.meta['path_type']
        container_name=response.meta['container_name']
        final_result=""
        for str in result:
            if str!='\n':
                final_result+=str
        item=ContainerItem()
        item['container_name']=container_name
        item[path_type]=final_result
        return item

