# -*- coding: utf-8 -*-
import scrapy

class SubtitleSpider(scrapy.Spider):
    name = 'subtitle'
    allowed_domains = ['moviesubtitles.xyz']
    
    base_url = 'http://moviesubtitles.xyz'

    def find_list_of_sub(self, response):
        sub_list = response.meta['sub_list']

        for sub in sub_list:
            sub_url = f"http://moviesubtitles.xyz/subtitles/searchbytitle?query={sub['name']}"

            meta = {'year':sub['year']}
            
            yield scrapy.Request(url=sub_url,callback= self.find_sub , meta=meta)

    def find_sub(self, response):
        try:
            year = response.meta['year']

            movie_links = response.xpath('//div[@class="title"]/a/@href').getall()
            movie_titles = response.xpath(
                '//div[@class="title"]/a/text()').getall()

            movie_url = str()
            movies = dict()
            for movie_title in movie_titles:
                if str(year) in movie_title:
                    movie_index = movie_titles.index(movie_title)
                    movie_link = movie_links[movie_index]
                    movie_url = self.base_url + movie_link
            
            
            yield scrapy.Request(movie_url, self.get_dlpath)
        except:
            pass

    def get_dlpath(self, response):
        try:
            download_paths = response.xpath(
                '//a[contains(@class , "download")]/@href').getall()[:5]

            dl_paths = [self.base_url + dl_path for dl_path in download_paths]
            yield scrapy.Request(dl_paths[0], self.get_dl_links ,  meta = {'paths':dl_paths})
        except:
            pass

    def get_dl_links(self, response):
        try:
            try:
                subtitles_list = response.meta['subtitles_list']
            except:
                subtitles_list = list()

            dl_link = response.xpath('//a[@id = "downloadButton"]/@href').get()
            dl_link = self.base_url + dl_link

            subtitles_list.append(dl_link)
            
            try:
                paths = response.meta['paths']
                paths = paths[1:]

                meta = {'paths': paths , 'subtitles_list': subtitles_list}
                
                path = paths[0]

                yield scrapy.Request(url=path , callback = self.get_dl_links , meta=meta)
            except:
                imdb_link = response.xpath('//a[@class = "imdb"]/@href').get()
                imdb = imdb_link.split('/')[-1]
                yield {'sub_urls': subtitles_list , 'imdb_id': imdb}
        except:
            pass