from .tools.serializer import json_data, json_serializer
from .tools.parser import parse_data
from .tools.translator import TranslatorCls

def _retrive_data(target,callback , meta = None):
        if meta:
            json_el = json_data(url=target, callback=callback , meta = meta)
        else:
            json_el = json_data(url=target, callback=callback)

        response_el = parse_data(json_el)
        print(response_el.json())
        res_el = json_serializer(response_el)

        return res_el

class Movies:
    @staticmethod
    def get_tops():
        top_list_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

        list_el = _retrive_data(top_list_url,'get_top_250')

        return list_el

    @staticmethod
    def get_id(name, year, crawl_url = 'http://localhost:9001/crawl.json'):
        if name and year:
            search_url = f'https://www.imdb.com/find?q={name}&s=tt&ttype=ft&ref_=fn_ft'

            movie_id = _retrive_data(search_url,'get_id', meta = {'year': year , 'tv': False})
            
            return movie_id
    
        return {'error' : 'arguments missing'}

    @staticmethod
    def get_details(movies):
        if movies:
            url = 'https://www.imdb.com/'
            movie_els = _retrive_data(url , 'get_list_of_details', meta = {'media_list': movies , 'tv':False} )
            
            movies_res = list()
            for movie_el in movie_els:
                try:
                    translator = TranslatorCls()
                    genres = movie_el['genres']
                    countries = movie_el['countries']
                    genres = [translator.genre_translator(genre) for genre in genres]
                    genres = [genre.strip() for genre in genres]
                    countries = [translator.country_translator(
                        country) for country in countries]
                    movie_el['genres'] = genres
                    movie_el['countries'] = countries

                    try:
                        movie_el['runtime'] = movie_el['runtime'].replace(
                            'min', '')
                        movie_el['runtime'] = int(movie_el['runtime'])
                    except:
                        movie_el['runtime'] = 100

                except:
                    pass

                movies_res.append(movie_el)
            
            return movies_res

    @staticmethod
    def get_images(movie_id , meta = None , movie_images = None):
        if movie_id:
            url = 'http://www.imdb.com'
            url_ext = f'/title/{movie_id}/mediaindex?refine=still_frame'
            url = url + url_ext

            if meta != None:
                movie_images_el = _retrive_data(url , 'list_images' , meta = meta)
            else:
                movie_images_el = _retrive_data(url , 'list_images')

            try:
                movie_images_el = movie_images_el.extend(movie_images)
            except:
                pass

            if len(movie_images_el) < 10:
                meta = {'dont_empty' : True , 'delete_list': movie_images_el}
                Movies.get_images(meta , movie_images_el)

            movie_images_el = _retrive_data(url , 'list_images')

            return {'images' : movie_images_el}

        else:
            print('no movie id')
            return None
    
    @staticmethod
    def get_cast(cast_list):
        if cast_list:
            url = 'https://www.imdb.com/'
            movie_els = _retrive_data(url , 'list_of_cast_details', meta = {'cast_list': cast_list} )
            return movie_els 

class Series:
    @staticmethod
    def get_tops():
        top_list_url = 'https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250'

        list_el = _retrive_data(top_list_url,'get_top_250')

        return list_el
    
    @staticmethod
    def seasons(imdb_id,season):
        url = f'https://www.imdb.com/title/{imdb_id}/episodes?season={season}'

        list_el = _retrive_data(url,'series_all_seasons')

        return list_el

    @staticmethod
    def get_id(name, year, crawl_url = 'http://localhost:9001/crawl.json'):
        if name and year:
            search_url = f'https://www.imdb.com/find?q={name}&s=tt&ttype=tv&ref_=fn_tv'

            series_id = _retrive_data(search_url,'get_id', meta = {'year': year , 'tv':True})
            
            return series_id
    
        return {'error' : 'arguments missing'}

    @staticmethod
    def get_details(series):
        if series:
            url = 'https://www.imdb.com/'
            series_els = _retrive_data(url , 'get_list_of_details', meta = {'media_list': series , 'tv':True})
            
            series_res = list()
            for series_el in series_els:
                try:
                    translator = TranslatorCls()
                    genres = series_el['genres']
                    countries = series_el['countries']
                    genres = [translator.genre_translator(genre) for genre in genres]
                    genres = [genre.strip() for genre in genres]
                    countries = [translator.country_translator(
                        country) for country in countries]
                    series_el['genres'] = genres
                    series_el['countries'] = countries

                    # try:
                    #     series_el['runtime'] = series_el['runtime'].replace(
                    #         'min', '')
                    #     series_el['runtime'] = int(series_el['runtime'])
                    # except:
                    #     series_el['runtime'] = 100

                except:
                    pass

                series_res.append(series_el)
            
            return series_res

    # @staticmethod
    # def get_images(movie_id , meta = None , movie_images = None):
    #     if movie_id:
    #         url = 'http://www.imdb.com'
    #         url_ext = f'/title/{movie_id}/mediaindex?refine=still_frame'
    #         url = url + url_ext

    #         if meta != None:
    #             movie_images_el = _retrive_data(url , 'list_images' , meta = meta)
    #         else:
    #             movie_images_el = _retrive_data(url , 'list_images')

    #             try:
    #             movie_images_el = movie_images_el.extend(movie_images)
    #         except:
    #             pass

    #         if len(movie_images_el) < 10:
    #             meta = {'dont_empty' : True , 'delete_list': movie_images_el}
    #             get_images(meta , movie_images_el)

    #         movie_images_el = _retrive_data(url , 'list_images')

    #         return {'images' : movie_images_el}

    #     else:
    #         print('no movie id')
    #         return None