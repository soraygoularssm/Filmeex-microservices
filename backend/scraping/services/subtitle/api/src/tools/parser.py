import requests

def parse_data(data):
    api_url = 'http://subtitle_microservice_crawler:9082/crawl.json'

    response = requests.post(url=api_url, data=data)

    return response
