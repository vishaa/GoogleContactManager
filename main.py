import json
from urllib import urlencode
from urllib2 import Request

from flask import Flask, render_template, redirect, request
from google.appengine.api import urlfetch

app = Flask(__name__)

CLIENT_ID = "416442779372-0ta38dd6esfmepfoprg53omos1v9jhrf.apps.googleusercontent.com"
CLIENT_SECRET = "4NhDKjukCRAl1mxHXpfvkU8W"
SCOPE = "https://www.google.com/m8/feeds/ https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
REDIRECT_URI = "http://vishaagan1994.appspot.com/oauth2callback"
OAUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://www.googleapis.com/oauth2/v4/token"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/googlesignin')
def google_signin():
    params = {'client_id': CLIENT_ID,
              'scope': SCOPE,
              'redirect_uri': REDIRECT_URI,
              'access_type': 'offline',
              'response_type': 'code',
              'prompt': 'consent'}

    return redirect('{}?{}'.format(OAUTH_ENDPOINT, urlencode(params)))


@app.route('/oauth2callback')
def oauth2_callback():
    params = {'client_id': CLIENT_ID,
              'client_secret': CLIENT_SECRET,
              'redirect_uri': REDIRECT_URI,
              'grant_type': 'authorization_code',
              'code': request.args.get('code')}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    res = urlfetch.fetch(TOKEN_ENDPOINT, method='POST', payload=urlencode(params), headers=headers)
    token_data = json.loads(res.content)

    headers = {'Authorization': 'Bearer {}'.format(token_data['access_token'])}
    req_uri = 'https://www.googleapis.com/oauth2/v1/userinfo'
    res = urlfetch.fetch(req_uri, headers=headers, method='GET')
    # user_data = json.loads()

    return str(res.content)


if __name__ == '__main__':
    app.run(debug=True)
