import os
is_dev = os.environ.get('SERVER_SOFTWARE','').startswith('Development')

CLIENT_ID = "416442779372-0ta38dd6esfmepfoprg53omos1v9jhrf.apps.googleusercontent.com"
CLIENT_SECRET = "4NhDKjukCRAl1mxHXpfvkU8W"
SCOPE = "https://www.google.com/m8/feeds/ https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
OAUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_ENDPOINT = "https://www.googleapis.com/oauth2/v4/token"

REDIRECT_URI = "https://vishaagan1994.appspot.com/"

if is_dev:
    REDIRECT_URI = "http://localhost:10080/oauth2callback"