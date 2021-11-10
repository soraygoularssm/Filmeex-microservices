import requests

def parse_data(data):
    api_url = 'http://imdb_microservice_crawler:9080/crawl.json'

    response = requests.post(url=api_url, data=data)

    return response
