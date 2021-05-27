from os import link
import requests
import json

file = open('key_value_api.json', 'r')
KeyValueJson = json.loads(file.read())
file.close()

Dict_fromAPI = []


def returnLinkRequest(key, value, page):
    linkRequests = "https://livescore-api.com/api-client/teams/list.json?key=KEY&secret=VALUE&page=PAGE"
    linkRequests = linkRequests.replace('KEY', key)
    linkRequests = linkRequests.replace('VALUE', value)
    linkRequests = linkRequests.replace('PAGE', page)
    return linkRequests


def LiveScoreMessage():
    # KeyValueJson['key']
    try:
        apiRequest = requests.get(returnLinkRequest(
            KeyValueJson['key'], KeyValueJson['value'], 1))
        ScoreData = json.loads(apiRequest.content)
        totalNumberOfPages = ScoreData['data']['pages']
        for obj in ScoreData['data']['teams']:
            Dict_fromAPI.append(obj)
        for index in range(2, totalNumberOfPages + 1):
            apiRequest = requests.get(returnLinkRequest(
                KeyValueJson['key'], KeyValueJson['value'], 1))
            ScoreData = json.loads(apiRequest.content)
            for obj in ScoreData['data']['teams']:
                Dict_fromAPI.append(obj)
    except Exception as e:
        print(f"Error... {e}")


Dict_fromAPI = sorted(Dict_fromAPI, key=lambda i: i['id'])
LiveScoreMessage()
