from config import CLIENT_SECRET, CLIENT_ID, REDIRECT_URI, TOKEN_ENDPOINT
from google.appengine.api import urlfetch
from urllib import urlencode
import json


def fetch_access_token(code):
    params = {'client_id': CLIENT_ID,
              'client_secret': CLIENT_SECRET,
              'redirect_uri': REDIRECT_URI,
              'grant_type': 'authorization_code',
              'code': code}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = urlfetch.fetch(TOKEN_ENDPOINT, method='POST', payload=urlencode(params), headers=headers)  # Getting Token
    return json.loads(res.content)