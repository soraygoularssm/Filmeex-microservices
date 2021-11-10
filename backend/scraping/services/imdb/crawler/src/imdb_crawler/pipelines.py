# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

#from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

import os

# from scrapy.utils.request import request_fingerprint
# from scrapy.utils.defer import mustbe_deferred, defer_result
# from twisted.internet.defer import Deferred
# from scrapy.utils.defer import mustbe_deferred
# from scrapy.utils.log import failure_to_exc_info
# import logging

# logger = logging.getLogger(__name__)

class ImdbCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class CustomImageNamePipeline(ImagesPipeline):

    # def image_downloaded(self, response, request, info):
    #     checksum = None
    #     for path, image, buf in self.get_images(response, request, info):
    #         if checksum is None:
    #             buf.seek(0)
    #             checksum = buf
    #         width, height = image.size
    #         self.store.persist_file(
    #             path, buf, info,
    #             meta={'width': width, 'height': height},
    #             headers={
    #                 'Content-Type': 'image/jpeg',
    #                 'Connection': 'keep-alive',
    #                 'Upgrade-Insecure-Requests': '1',
    #                 'Proxy-Connection': 'keep-alive',
    #                 'Pragma': 'no-cache',
    #                 'Cache-Control': 'no-cache', })

    #     return checksum

    def get_media_requests(self, item, info):
        return [Request(x, dont_filter=True, meta={'image_name': item["id"]}) for x in item.get('image_urls', [])]

    def file_path(self, request, response=None, info=None):
        return 'full/%s.jpg' % request.meta['image_name']

    def thumb_path(self, request, thumb_id, response=None, info=None):
        return 'thumbs/%s/%s.jpg' % (thumb_id, request.meta['image_name'])

    def item_completed(self, results, item, info):
        try:
            return item['details']
        except:
            return item
