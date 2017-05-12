from flask import Flask, render_template, redirect, request
from google.appengine.api import urlfetch
import json
from models.user import User
from models.session import Session
from urllib import urlencode
from config import OAUTH_ENDPOINT, CLIENT_ID, SCOPE, REDIRECT_URI
from services.oauth_services import fetch_access_token

app = Flask(__name__)


@app.route('/')
def index():
    if 'sessionID' in request.cookies:
        client_uuid = request.cookies.get('sessionID')
        user = Session.get_by_id(client_uuid)
        if user: return 'Welcome {}'.format(user.name)  # redirect('/showcontacts')

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

    token_data = fetch_access_token(request.args.get('code'))

    headers = {'Authorization': 'Bearer {}'.format(token_data['access_token'])}
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    res = urlfetch.fetch(url, headers=headers, method='GET')  # Getting userinfo
    user_data = json.loads(res.content)

    User.set_user(user_data, token_data)
    uuid = Session.set_session(user_data)

    res = redirect('/')
    res.set_cookie('sessionID', uuid)

    return res


@app.route('/showcontacts')
def show_contacts():
    return 'Under Progress'


if __name__ == '__main__':
    app.run(debug=True)
