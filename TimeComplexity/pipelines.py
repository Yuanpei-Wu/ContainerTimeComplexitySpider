# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis



class TimecomplexityPipeline(object):
    def __init__(self):
        self.client=redis.Redis(host='127.0.0.1',port=6379,password='password')

    def process_item(self, item, spider):
        if spider.name=='reference':
            if dict(item).has_key('find_time') :
                self.client.hset('container_time_complexity::'+item['container_name'],'find_time',item['find_time'])
            if dict(item).has_key('insert_time'):
                self.client.hset('container_time_complexity::' + item['container_name'], 'insert_time', item['insert_time'])
            if dict(item).has_key('erase_time'):
                self.client.hset('container_time_complexity::' + item['container_name'], 'erase_time', item['erase_time'])
        return item

    def close_spider(self,spider):
        containers=self.client.keys('container_time_complexity*')
        for container in containers :
            print "result for "+container+":"
            print self.client.hgetall(container)
        print "end"