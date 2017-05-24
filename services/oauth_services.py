from google.appengine.api import urlfetch
from urllib import urlencode
from config import config
import json


def fetch_access_token(code,redirect_uri):
    params = {'client_id': config.get("CLIENT_ID"),
              'client_secret': config.get("CLIENT_SECRET"),
              'redirect_uri': redirect_uri,
              'grant_type': 'authorization_code',
              'code': code}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = urlfetch.fetch(config.get("TOKEN_ENDPOINT"), method='POST',
                         payload=urlencode(params), headers=headers)  # Getting Token
    return json.loads(res.content)
