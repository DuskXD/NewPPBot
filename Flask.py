from flask import Flask
from flask import request
import psycopg2
import requests
# conn = psycopg2.connect(
#     dbname = "ppbot",
#     user = "postgres",
#     password = "DaS3VLQZ@IOp",
#     host = "127.0.0.1",
#     port = "5432"
#
# )


app = Flask(__name__)


leader_id_api_url_auth = 'https://apps.leader-id.ru/api/v1/oauth/token'
leader_id_api_url_events = 'https://apps.leader-id.ru/api/v1/events'
client_id = 'fce7f1d5-c662-4f8a-bf44-0915e81687e9'
client_secret = 'kFpy0P3obIC6UPuafXC664gL41zo2P7n'
redirect_uri = 'http://your_redirect_uri.com'
params = {
    "client_id": "84310388-38b5-471c-8893-f0c3161c125f",
    "client_secret": "jRDqrTNrYdumYuKKnLnbwc0gXxuORbP2",
    "grant_type": "client_credentials"
}


@app.route('/auth', methods=['GET'])
def auth():
    code = request.args.get('code')
    if code:
        auth_headers = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': code

        }
        access_token_response = requests.post(leader_id_api_url_auth, headers=auth_headers)
        if access_token_response.status_code == 200:
            access_token = access_token_response.json()['access_token']
            refresh_token = access_token_response.json()['refresh_token']
            user_id = access_token_response.json()['user_id']
            #добавить пользователя в бд с аксесс и рефреш токенами
            # events_headers = {
            #
            #     'Authorization': f'Bearer {access_token}'
            # }
            # events_response = request.get(leader_id_api_url_auth, headers = events_headers)
            return f'Аутентификация прошла успешно. Access token: {access_token}, refresh_token: {refresh_token}, user_id: {user_id}'
        else:
            return 'Ошибка аутентификации'
    else:
        return 'Код не был получен'

if __name__ == '__main__':
    app.run()
