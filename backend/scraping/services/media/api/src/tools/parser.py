import requests

def parse_data(data):
    api_url = 'http://media_microservice_crawler:9081/crawl.json'

    response = requests.post(url=api_url, data=data)

    # print(response)

    return response
