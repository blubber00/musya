from flask import Flask
from flask import request
import start_bot
import requests
from settings import api_token
from settings import forwarding

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        try:
            start_musya(r)
        except IndexError as e:
            print(e)
            start_bot.out_of_rande(r)
            return('<Response 200>')
        return('<Response 200>')
    return('<h1>Hello bot</h1>')

def start_musya(data):
    if 'callback_query' in data:
        start_bot.callback_query_sort(data['callback_query'])
    else:
        start_bot.get_text(data['message'])

def main_start():
    url = f'https://api.telegram.org/bot{api_token}/deleteWebhook'
    requests.post(url)
    url = f"https://api.telegram.org/bot{api_token}/setWebhook?url={forwarding}"
    requests.post(url)
    app.run()
    

if __name__ == '__main__':
    main_start()