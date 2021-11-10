# -*- coding: utf-8 -*-
import scrapy

import time
import random

import lxml.html

class SeriesSpider(scrapy.Spider):
    name = 'series'
    allowed_domains = ['my-filmm.pro']
    
    def parse(self, response):
        posts = response.xpath('//article[@class="post"]/div[1][contains(@class , "entry")]/header/h3/a/@href').getall()

        for post in posts:
            yield scrapy.Request(url=post,callback=self.parse_page)
      
        page_counter = response.meta['page_counter']
        page_counter = int(page_counter)

        try:
            current_page = int(response.request.url.split('/')[-1])
            last_page = current_page + page_counter
            if current_page < last_page:
                next_page_url = current_page + 1
                absolute_next_page_url = 'https://my-filmm.pro/series' + '/page/{}'.format(next_page_url)

                page_counter = page_counter - 1
                yield scrapy.Request(url=absolute_next_page_url ,  meta = {'page_counter':page_counter})
            else:
                pass
        except:
            absolute_next_page_url = 'https://my-filmm.pro/series' + '/page/2'
            
            page_counter = page_counter - 1
            yield scrapy.Request(url=absolute_next_page_url , meta = {'page_counter':page_counter})


    def parse_page(self,response):
        try:
            post_content = response.xpath('//div[@class="post-content"]')
            
            farsi_name = post_content.xpath('.//p[starts-with(text() , "نام") and not(contains(text() , "خلاصه"))]/text()[normalize-space()]').get()
            #summary = response.xpath('.//p[contains(text() , "خلاصه")]').get()
            try:
                summary = response.xpath("//*[contains(text(),'خلاصه')]").get()
                if len(summary) < 50:
                    summary = response.xpath("//*[contains(text(),'خلاصه')]/..").get()

                summary_root = lxml.html.fromstring(summary)
                summary_element = lxml.html.tostring(summary_root,method='text',encoding='unicode')
                summary = summary_element
            except:
                summary = 'خلاصه فیلم'

            imdb_id = response.xpath('.//p/a[contains(@href , "imdb")]/@href').get()
            imdb_id = imdb_id[27:].replace('/','')

            try:    
                farsi_name = farsi_name.replace('نام فارسی','').replace(':','').strip()
            except:
                pass
            
            summary = summary.replace('خلاصه فیلم','').replace(':','').strip()
            
            urls = response.xpath('//article[@class="post"]//a[contains(@href , "dlserver") and not(contains(@href , ".mka"))]/@href').getall()
            urls = [url for url in urls if 'x265' not in url]
            urls = [url for url in urls if 'HEVC' not in url]

            # qualities = ['240p' , '360p' , '480p' , '720p' , '1080p']
        
            # urls_list = []
            # for q in qualities:
            #     for url in urls:
            #         if q in url:
            #             urls_list.append({'quality': q , 'url': url})

            res = {
                'imdb_id': imdb_id,
                'summary' : summary,
                'sub_urls': urls
                # 'sources' : {
                #     'urls': urls_list
                # }
            }
            if farsi_name:
                res['farsi_name'] =  farsi_name

            yield res
        except Exception as e:
            pass
            # error = {'error': str(e) ,  'response': response}
            # yield error