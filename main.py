from flask import Flask, render_template, redirect, request, abort
from google.appengine.api import urlfetch
import json
from models.user import User
from models.session import Session
from models.contacts import Contacts
from urllib import urlencode
from config import OAUTH_ENDPOINT, CLIENT_ID, SCOPE, REDIRECT_URI
from services.oauth_services import fetch_access_token
from google.appengine.api import taskqueue

app = Flask(__name__)


@app.route('/')
def index():
    if 'sessionID' in request.cookies:
        client_uuid = request.cookies.get('sessionID')
        user = Session.get_by_id(client_uuid)
        if user: return 'Welcome {}'.format(user.name)  # redirect('/showcontacts')

    return render_template('index.html')


@app.route('/google-signin')
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

    taskqueue.add(url='/fetch-contacts',
                  params={'email': user_data.get('email'),
                          'access_token': token_data.get('access_token')},
                  method='GET')

    res = redirect('/')
    res.set_cookie('sessionID', uuid)

    return res


@app.route('/showcontacts')
def show_contacts():
    return 'Under Progress'


@app.route('/fetch-contacts')
def fetch_contacts():
    email = request.args.get('email')
    access_token = request.args.get('access_token')

    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    req_uri = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=5&v=3.0&access_token={}' + \
              access_token
    r = urlfetch.fetch(req_uri, headers=headers, method='GET')
    data = json.loads(r.content)

    feed = data.get('feed')
    entry = feed.get('entry')  # List
    contact_name = entry[0].get('gd$name').get('gd$fullName').get('$t')
    number = entry[0].get('gd$phoneNumber')
    contact_number = number[0].get('$t')
    Contacts.add_contact(email, contact_name, contact_number)

    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
