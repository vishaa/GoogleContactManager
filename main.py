import json
import logging
from urllib import urlencode

from flask import Flask, render_template, redirect, request, jsonify
from google.appengine.api import taskqueue
from google.appengine.api import urlfetch
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

from config import config
from models.contacts import Contacts
from models.session import Session
from models.user import User
from services.oauth_services import fetch_access_token

app = Flask(__name__)


@app.route('/')
def index():
    sessionID = request.cookies.get('sessionID')
    if sessionID and sessionID != '':
        user = Session.get_by_id(sessionID)
        if user:
            return render_template('index.html')
    return render_template('signin.html')


@app.route('/google-signin')
def google_signin():
    params = {'client_id': config.get("CLIENT_ID"),
              'scope': config.get("PROFILE_SCOPE"),
              'redirect_uri': config.get("PROFILE_REDIRECT_URI"),
              'access_type': 'offline',
              'response_type': 'code',
              'prompt': 'consent'}

    return redirect('{}?{}'.format(config.get("OAUTH_ENDPOINT"), urlencode(params)))


@app.route('/loginCallback')
def oauth2_callback():
    if (request.args.get('error') == 'access_denied'):
        return 'You denied the access'
    token_data = fetch_access_token(request.args.get('code'),
                                     config.get("PROFILE_REDIRECT_URI"))

    headers = {'Authorization': 'Bearer {}'.format(token_data['access_token'])}
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    res = urlfetch.fetch(url, headers=headers, method='GET')  # Getting userinfo
    user_data = json.loads(res.content)

    User.set_user(user_data)
    uuid = Session.set_session(user_data)

    res = redirect('/')
    res.set_cookie('sessionID', uuid)

    return res


@app.route('/oauthPermission')
def contacts_oauth():
    uuid = request.cookies.get('sessionID')
    entity = Session.get_by_id(uuid)
    if entity: email=entity.email
    else : return redirect('/')

    user = User.get_by_id(email)
    if user.importing_contacts: return ""

    params = {'client_id': config.get("CLIENT_ID"),
              'scope': config.get("CONTACT_SCOPE"),
              'redirect_uri': config.get("CONTACTS_REDIRECT_URI"),
              'access_type': 'offline',
              'response_type': 'code',
              'prompt': 'consent'}

    return redirect('{}?{}'.format(config.get("OAUTH_ENDPOINT"), urlencode(params)))


@app.route('/oauth2callback')
def import_contacts():
    uuid = request.cookies.get('sessionID')
    entity = Session.get_by_id(uuid)

    if entity:
        email = entity.email
    else:
        return redirect('/')

    if (request.args.get('error') == 'access_denied'):
         return 'You denied the access'

    token_data = fetch_access_token(request.args.get('code'),
                                    config.get("CONTACTS_REDIRECT_URI"))

    user = User.get_by_id(email)
    user.set_token(token_data)
    user.has_imported = False
    user.put()
    taskqueue.add(url='/fetch-contacts',
                  params={'email': email,
                          'access_token': token_data.get('access_token')},
                  method='GET')

    return redirect('/')

@app.route('/contacts')
def list_contacts():
    session_id = request.cookies.get('sessionID')
    if not session_id or session_id == '':
        return jsonify(dict(success=False, error='unauthorized'))
    user = Session.get_by_id(session_id)
    if not user:
        return jsonify(dict(success=False, error='unauthorized'))

    email = user.email
    # logging.info('email : {}'.format(email))
    cursor = request.args.get('cursor')
    if not cursor: cursor = None;
    cursor = Cursor(urlsafe= cursor)
    query = Contacts.query(Contacts.owner == email).order(Contacts.name_lc)
    contacts, next_cursor, more = query.fetch_page(10, start_cursor=cursor)
    #logging.info('cursor: {} more: {}'.format(next_cursor, more))
    data = [contact.to_dict() for contact in contacts]

    return jsonify({
        'cursor': next_cursor.urlsafe(),
        'more': more,
        'contacts': data,
        'success': True
    })


@app.route('/logout')
def logout():
    uuid = request.cookies.get('sessionID')
    entity = Session.get_by_id(uuid)
    if entity: entity.key.delete()
    res = redirect('/')
    res.set_cookie('sessionID', '')
    return res


# ___________________________________________________Handlers_________________________________________________________
@app.route('/fetch-contacts')
def fetch_contacts():
    email = request.args.get('email')
    access_token = request.args.get('access_token')

    user=User.get_by_id(email)

    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    req_uri = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=25000&v=3.0'
    r = urlfetch.fetch(req_uri, headers=headers, method='GET')
    data = json.loads(r.content)

    contact_list = data.get('feed', {}).get('entry', [])  # List

    ndb.delete_multi(Contacts.query(Contacts.owner == email).fetch(keys_only=True))

    for contact in contact_list:

        if ('gd$phoneNumber' not in contact): continue

        name = contact.get('gd$name', {}) \
            .get('gd$fullName', {}) \
            .get('$t', '')
        numbers = [number.get('$t', '') for number in contact.get('gd$phoneNumber', [])]

        Contacts.add_contact(email, name, numbers)

    user.importing_contacts = False
    user.put()

    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
