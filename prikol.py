import requests

def start():
    params = {'lang':'ru', 'type':'json'}
    url = 'https://evilinsult.com/generate_insult.php'
    result = requests.get(url, params)
    message = result.json()['insult']
    return message

