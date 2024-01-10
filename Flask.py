from flask import Flask, render_template
from flask import request
import requests
import json


app = Flask(__name__)


leader_id_api_url_auth = 'https://apps.leader-id.ru/api/v1/oauth/token'
leader_id_api_url_events = 'https://apps.leader-id.ru/api/v1/events' # ссылка для поиска мероприятий
client_id = 'fce7f1d5-c662-4f8a-bf44-0915e81687e9'
client_secret = 'kFpy0P3obIC6UPuafXC664gL41zo2P7n'
redirect_uri = 'http://your_redirect_uri.com'
params = {
    "client_id": "84310388-38b5-471c-8893-f0c3161c125f",
    "client_secret": "jRDqrTNrYdumYuKKnLnbwc0gXxuORbP2",
    "grant_type": "client_credentials"
}


@app.route('/')
def start():
    return "Hi"


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    code = request.args.get('code')
    if code:
        auth_headers = {
            'client_id': 'fce7f1d5-c662-4f8a-bf44-0915e81687e9',
            'client_secret': 'kFpy0P3obIC6UPuafXC664gL41zo2P7n',
            'grant_type': 'authorization_code',
            'code': code
        }
        # return data
        try:
            access_token_response = requests.post(leader_id_api_url_auth, data=auth_headers)
        except Exception:
            return 'Ошибка в получении access token'
        if access_token_response.status_code == 200:
            access_token = access_token_response.json()['access_token']
            refresh_token = access_token_response.json()['refresh_token']
            user_id = access_token_response.json()['user_id']
            events_headers = {

                'Authorization': f'Bearer {access_token}'
            }
            try:
                events_response = request.get(leader_id_api_url_auth, headers = events_headers)
            except Exception:
                return 'Ошибка в получении мероприятий'
            if events_response.status_code == 200:
                events = events_response.json()
                event_list = [event['name'] for event in events]
                return f"Мероприятия:\n\n{', '.join(event_list)}"
            else:
                return "Не удалось получить список мероприятий"
            # Далее можно использовать access_token для работы с Leader-ID API
            return f'Аутентификация прошла успешно, code: {code}. Access token: {access_token}, refresh_token: {refresh_token}, user_id: {user_id}'
        else:
            return 'Ошибка аутентификации'
    else:
        return 'Код не был получен'

if __name__ == '__main__':
    app.run()
