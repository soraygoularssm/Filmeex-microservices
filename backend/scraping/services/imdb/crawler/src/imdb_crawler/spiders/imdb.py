import scrapy
from ..items import MediaItem
# from scrapy_splash import SplashRequest
import random
import lxml
import unicodedata
import time

class ImdbSpider(scrapy.Spider):
    name = "imdb"

    def __init__(self):
        self.img_list = dict()
        self.seasons_list = dict()

    def get_top_250(self ,  response):
        bests_list = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="posterColumn"]/a/@href').getall()
        bests_list = [media.split('/') for media in bests_list]
        bests_list = [[m for m in media if m] for media in bests_list]

        bests_list = [media[1] for media in bests_list]

        yield {'tops':bests_list}
        
    def get_id(self, response):
        year = response.meta['year']
        tv = response.meta['tv']

        result_table = response.xpath(
            '//table[@class = "findList"]/tr/td[contains(@class, "result_text")]')

        all_elements = list()
        for rt in result_table:
            html_str = rt.get()
            root = lxml.html.fromstring(html_str)
            element = lxml.html.tostring(
                root, method='text', encoding='unicode')

            not_included = ('(TV Series)', '(TV Episode)', '(TV Special)', '(Video)', '(Short)',
                            '(in development)', '(TV Movie)', '(Video Game)', '(TV Mini-Series)')

            if tv:
                not_included = not_included[1:]
                
            proof_count = 0
            for ni in not_included:
                if ni not in element:
                    proof_count += 1

            if len(not_included) == proof_count:
                element_dict = dict()
                element_dict['html'] = rt
                element_dict['text'] = element
                all_elements.append(element_dict)

        result_movies = list()
        for ae in all_elements:
            if '({})'.format(str(year)) in ae['text']:
                result_movies.append(ae['html'])

        movie_href = result_movies[0].xpath('.//a/@href').get()
        movie_imdb_url = response.urljoin(movie_href)
        imdb_id = movie_imdb_url[27:-1]

        yield {
            'id': imdb_id,
        }

    def get_list_of_details(self, response):
        self.seasons_list.clear()
        # self.img_list.clear()
        # self.img_list['urls'] = []

        media_list = response.meta['media_list']
        tv = response.meta['tv']
        base_url = 'https://www.imdb.com/title/'
        if not tv:  
            for media in media_list:
                yield scrapy.Request(url = base_url + media , callback = self.get_details)
        else:
            for media in media_list:
                yield scrapy.Request(url = base_url + media , callback = self.get_series_details)

    def get_details(self, response):
        title_wrapper = response.xpath('//div[@class="title_wrapper"]')[0]
        movie_name = title_wrapper.xpath('.//h1/text()').get()
        movie_name = unicodedata.normalize("NFKD", movie_name)
        movie_name = movie_name.strip()

        release_year = title_wrapper.xpath(
            './/span[@id="titleYear"]/a/text()').get()

        rating_bar = response.xpath('//div[@class = "imdbRating"]')

        rating_val = rating_bar.xpath(
            './/div[@class = "ratingValue"]/strong/@title').get()

        rating_val = rating_val.replace(
            'based on', '').replace('user ratings', '').strip()
        rating_val = rating_val.split()

        rating_val = {
            'rate': float(rating_val[0]),
            'rates_amount': rating_val[1]
        }

        writers = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Writers")]/../a/text()').getall()
        if not writers:
            writers = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Writer")]/../a/text()').getall()

        # directors_name = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Directors")]/../a/text()').getall()

        directors_id = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Directors")]/../a/@href').getall()
        if not directors_id:
            directors_id = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Director")]/../a/@href').getall()

        directors_id = [director.split('/') for director in directors_id]
        directors_id = [[d for d in director if d] for director in directors_id]
        directors_id = [director[1] for director in directors_id if len(director) > 1]

        directors = directors_id

        try:
            actors_list = response.xpath(
                '//table[@class = "cast_list"]/tr')[1:6]
        except:
            actors_list = response.xpath(
                '//table[@class = "cast_list"]/tr')[1:]

        actors_name = actors_list.xpath('.//td[not(@id) and not(@class)]/a/text()').getall()
        actors_name = [actor.strip() for actor in actors_name]

        actors_id = actors_list.xpath(
            './/td[not(@id) and not(@class)]/a/@href').getall()
        actors_id = [actor.split('/') for actor in actors_id]
        actors_id = [[a for a in actor if a] for actor in actors_id]
        actors_id = [actors[1] for actors in actors_id]

        actors = list()

        for actor_id in actors_id:
            actor_index = actors_id.index(actor_id)
            actor = dict()
            actor['name'] = actors_name[actor_index]
            actor['id'] = actor_id
            actors.append(actor)

        poster_path = response.xpath('//div[@class="poster"]/a/img/@src').get()
        poster = poster_path.split('.')
        poster[-2] = '_V1_UY500_'
        poster = '.'.join(poster)

        genres = response.xpath(
            '//div[@id="titleStoryLine"]/div[contains(@class, "see-more")]/h4[@class="inline" and contains(text(),"Genres")]/../a/text()').getall()

        details = response.xpath('//div[@id = "titleDetails"]')

        languages = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Language")]/../a/text()').getall()

        countries = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Country")]/../a/text()').getall()

        budget = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Budget")]/../text()[normalize-space()]').get()

        worldwide_gross = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Cumulative Worldwide Gross")]/../text()[normalize-space()]').get()

        runtime = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Runtime")]/../time/text()').get()

        try:
            budget = budget.strip()
            worldwide_gross = worldwide_gross.strip()
            runtime = runtime.strip()
        except:
            try:
                worldwide_gross = worldwide_gross.strip()
                runtime = runtime.strip()
            except:
                try:
                    runtime = runtime.strip()
                except:
                    pass
        
        imdb_id = response.url.split('/')
        imdb_id = imdb_id[-2]

        res = {
            'imdb_id' : imdb_id,
            'name': movie_name,
            'year': release_year,
            'rating': rating_val,
            'poster' : f'{imdb_id}.jpg',
            'genres': genres,
            'languages': languages,
            'countries': countries,
            'runtime': runtime,
            'crew' : {
                'stars': actors,
                'writers': writers[:2],
                'directors' : directors
            }
        }

        if budget:
            res['budget'] = budget
        elif worldwide_gross:
            res['worldwide_gross'] = worldwide_gross

        # result = dict()
        # result['info'] = res

        # yield res
        
        med = MediaItem()
        med['id'] = imdb_id
        med['details'] = res
        med['image_urls'] = [poster]

        yield med
            


    def get_series_details(self, response):
        title_wrapper = response.xpath('//div[@class="title_wrapper"]')[0]
        movie_name = title_wrapper.xpath('.//h1/text()').get()
        movie_name = unicodedata.normalize("NFKD", movie_name)
        movie_name = movie_name.strip()

        rating_bar = response.xpath('//div[@class = "imdbRating"]')

        rating_val = rating_bar.xpath(
            './/div[@class = "ratingValue"]/strong/@title').get()

        rating_val = rating_val.replace(
            'based on', '').replace('user ratings', '').strip()
        rating_val = rating_val.split()

        rating_val = {
            'rate': float(rating_val[0]),
            'rates_amount': rating_val[1]
        }

        creators = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Creators")]/../a/text()').getall()

        if not creators:
            creators = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Creator")]/../a/text()').getall()

        # creators_id = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Creators")]/../a/@href').getall()
        # if not creators_id:
        #     creators_id = response.xpath('//div[@class = "credit_summary_item"]/h4[contains(text(),"Creator")]/../a/@href').getall()

        # creators_id = [creator.split('/') for creator in creators_id]
        # creators_id = [[c for c in creator if c] for creator in creators_id]
        # creators_id = [creator[1] for creator in creators_id if len(creator) > 1]

        # creators = creators_id

        try:
            actors_list = response.xpath(
                '//table[@class = "cast_list"]/tr')[1:6]
        except:
            actors_list = response.xpath(
                '//table[@class = "cast_list"]/tr')[1:]

        actors_name = actors_list.xpath('.//td[not(@id) and not(@class)]/a/text()').getall()
        actors_name = [actor.strip() for actor in actors_name]

        actors_id = actors_list.xpath(
            './/td[not(@id) and not(@class)]/a/@href').getall()
        actors_id = [actor.split('/') for actor in actors_id]
        actors_id = [[a for a in actor if a] for actor in actors_id]
        actors_id = [actors[1] for actors in actors_id]

        actors = list()

        for actor_id in actors_id:
            actor_index = actors_id.index(actor_id)
            actor = dict()
            actor['name'] = actors_name[actor_index]
            actor['id'] = actor_id
            actors.append(actor)

        poster_path = response.xpath('//div[@class="poster"]/a/img/@src').get()
        poster = poster_path.split('.')
        poster[-2] = '_V1_UY500_'
        poster = '.'.join(poster)

        genres = response.xpath(
            '//div[@id="titleStoryLine"]/div[contains(@class, "see-more")]/h4[@class="inline" and contains(text(),"Genres")]/../a/text()').getall()

        details = response.xpath('//div[@id = "titleDetails"]')

        languages = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Language")]/../a/text()').getall()

        countries = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Country")]/../a/text()').getall()

        budget = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Budget")]/../text()[normalize-space()]').get()

        worldwide_gross = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Cumulative Worldwide Gross")]/../text()[normalize-space()]').get()

        runtime = details.xpath(
            './/div[@class = "txt-block"]/h4[@class="inline" and contains(text() , "Runtime")]/../time/text()').get()

        try:
            budget = budget.strip()
            worldwide_gross = worldwide_gross.strip()
            runtime = runtime.strip()
        except:
            try:
                worldwide_gross = worldwide_gross.strip()
                runtime = runtime.strip()
            except:
                try:
                    runtime = runtime.strip()
                except:
                    pass
        
        runtime = runtime.replace('min' , '').strip()
        runtime = int(runtime)
        
        imdb_id = response.url.split('/')
        imdb_id = imdb_id[-2]

        res = {
            'imdb_id' : imdb_id,
            'name': movie_name,
            'rating': rating_val,
            'poster' : f'{imdb_id}.jpg',
            'genres': genres,
            'languages': languages,
            'countries': countries,
            'each_episode_runtime':  runtime,
            'crew' : {
                'stars': actors ,
                'creators': creators
            }
        }

        if budget:
            res['budget'] = budget
        elif worldwide_gross:
            res['worldwide_gross'] = worldwide_gross

        result = dict()
        result['info'] = res

        imdb_id = res['imdb_id']
        self.seasons_list.update({imdb_id : {'years': [] , 'seasons': []}})

        last_season_url = 'https://www.imdb.com/' + response.xpath('//div[@class = "seasons-and-year-nav"]/div/a/@href').get()

        last_chars = 4
        last_season = [int(last_season_url[-last_chars + i:]) for i in range(last_chars) if last_season_url[-last_chars + i:].isdigit()]
        last_season = last_season[0]
        season_urls = []
        if last_season >= 1:
            for r in range(last_season):
                prv_season = last_season - (last_season - r) + 1
                prv_url = last_season_url[-3:].replace(str(last_season) , str(prv_season))
                prv_url = last_season_url[:-3] + prv_url
                season_urls.append(prv_url)
        
        for url in season_urls:
            yield scrapy.Request(url=url , callback=self.series_season , meta = {'imdb_id' : imdb_id})

        res['years'] = self.seasons_list[imdb_id]['years']
        res['seasons'] = self.seasons_list[imdb_id]['seasons']

        med = MediaItem()
        med['id'] = imdb_id
        med['details'] = res
        med['image_urls'] = [poster]

        yield med

    def series_season(self,response):
        imdb_id = response.meta['imdb_id']

        eplist = response.xpath("//div[contains(@class , 'eplist')]")                                                                                                                                    
        eps = eplist.xpath('//div[contains(@class,"list_item")]')
        eps = [e.replace('\n','').replace(' ','')[-4:] for e in eps.xpath("div[@class='info']/div[@class='airdate']/text()").getall()]
        eps_number = len(eps)
        eps_years = list(set(eps))

        episodes = [{'ep_number': i + 1} for i in range(eps_number)]

        current_url = response.request.url
        last_chars = 4
        current_season = [int(current_url[-last_chars + i:]) for i in range(last_chars) if current_url[-last_chars + i:].isdigit()]
        current_season = current_season[0]

        for year in eps_years:
            if not year in self.seasons_list[imdb_id]['years']:
                if year != "" and year != None:
                    self.seasons_list[imdb_id]['years'].append(year)

        season_info = {
            'season_number': current_season ,
            'episodes' : episodes
        }
        
        self.seasons_list[imdb_id]['seasons'].append(season_info)


    def list_of_cast_details(self,response):
        cast_list = response.meta['cast_list']
        base_url = 'https://www.imdb.com/name/'
        for cast in cast_list:
            url = base_url + cast
            yield scrapy.Request(url = url , callback = self.cast_details)

    def cast_details(self, response):
        crew_id = response.request.url.split('/')
        crew_id = [c for c in crew_id if c]
        crew_id = crew_id[-1]

        name = response.xpath(
            '//h1[@class="header"]/span[@class="itemprop"]/text()').get()

        head_shot = response.xpath('//img[@id = "name-poster"]/@src').get()
        if not head_shot:
            head_shot = 'https://m.media-amazon.com/images/G/01/imdb/images/nopicture/medium/name-2135195744._CB466677935_.png'

        born_date = response.xpath('//h4[contains(text(),"Born")]/../time/@datetime').get()

        res = {
            'imdb_id': crew_id,
            'headshot': head_shot,
            'name': name,
            'birth_date' : born_date,
        }

        yield res

    # async def list_images(self, response):
    #     images_unites = 10
    #     try:
    #         dont_empty = response.meta['dont_empty']
    #         try:
    #             delete_list = response.meta['delete_list']
    #             images_unites = 10 - len(delete_list)
    #             for delete in delete_list:
    #                 self.img_list.remove(delete)
    #         except:
    #             pass
    #     except:
    #         self.img_list.clear()

    #     if len(self.img_list) < 80:
    #         images = response.xpath('//div[@class = "media_index_thumb_list"]/a[not(contains(@title , "event" or "oscar"))]/@href').getall()
    #         images = ['https://www.imdb.com/' + image for image in images]

    #         self.img_list.extend(images)
    #         self.img_list = self.img_list[:100]
             
    #         next_page = response.xpath('//div[@id = "right"]/a[contains(text() , "Next")]/@href').get()

    #         if next_page == None:
    #             ten_imgs = random.sample(self.img_list ,  k= images_unites)

    #             for image in ten_imgs:
    #                 img_url = image

    #                 yield SplashRequest(img_url, self.get_image,
    #                         endpoint='render.html',
    #                         args={'wait': 0.1}
    #                     )
    #         else:
    #             next_page_url = 'https://www.imdb.com/' + next_page
    #             yield scrapy.Request(url=next_page_url , callback=self.list_images , meta={'dont_empty' : True})
    #     else:
    #         ten_imgs = random.sample(self.img_list ,  k= images_unites)

    #         for image in ten_imgs:
    #             img_url = image

    #             yield SplashRequest(img_url, self.get_image,
    #                     endpoint='render.html'
    #                     # args={'wait': 0.1}
    #                 )

    def list_images(self, response):
        images_unites = 15
        try:
            dont_empty = response.meta['dont_empty']
        except:
            self.img_list.clear()

        if len(self.img_list) < 80:
            images = response.xpath('//div[@class = "media_index_thumb_list"]/a[not(contains(@title , "event" or "oscar"))]/@href').getall()
            images = ['https://www.imdb.com/' + image for image in images]

            self.img_list.extend(images)
            self.img_list = self.img_list[:100]
             
            next_page = response.xpath('//div[@id = "right"]/a[contains(text() , "Next")]/@href').get()

            if next_page == None:
                ten_imgs = random.sample(self.img_list ,  k= images_unites)

                for image in ten_imgs:
                    img_url = image
                    
                    yield scrapy.Request(url = img_url, callback = self.get_image)
            else:
                next_page_url = 'https://www.imdb.com/' + next_page
                yield scrapy.Request(url=next_page_url , callback=self.list_images , meta={'dont_empty' : True})
        else:
            ten_imgs = random.sample(self.img_list ,  k= images_unites)

            for image in ten_imgs:
                img_url = image

                yield scrapy.Request(url = img_url, callback = self.get_image)

    def get_image(self, response):
        img_src = response.xpath('/html/head/meta[@itemprop="image"]/@content').get()
        img_src = img_src.split('.')
        img_src[-2] = '_V1_'
        img_src = '.'.join(img_src)

        res = dict()
        res['img'] = img_src

        yield res

    # def get_image(self,response):
    #     print('hello')
    #     img = response.xpath('//img[@class = "pswp__img"]')
    #     img_style = img.xpath('//img/@style').get()
    #     img_style = img_style.replace('px;' , ' ')
    #     img_size = [int(s) for s in img_style.split() if s.isdigit()]
    #     img_width = img_size[0]
    #     img_height = img_size[1]
    #     if img_width > img_height:
    #         img_src = img.xpath('//img/@src').get()
    #         res = dict()
    #         res['img'] = img_src

    #         yield res
