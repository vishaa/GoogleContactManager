import os
is_dev = os.environ.get('SERVER_SOFTWARE','').startswith('Development')

config = {};

config["CLIENT_ID"] = "416442779372-0ta38dd6esfmepfoprg53omos1v9jhrf.apps.googleusercontent.com"
config["CLIENT_SECRET"] = "4NhDKjukCRAl1mxHXpfvkU8W"
config["CONTACT_SCOPE"] = "https://www.google.com/m8/feeds/"
config["PROFILE_SCOPE"] = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
config["OAUTH_ENDPOINT"] = "https://accounts.google.com/o/oauth2/v2/auth"
config["TOKEN_ENDPOINT"] = "https://www.googleapis.com/oauth2/v4/token"

config["PROFILE_REDIRECT_URI"] = "http://vishaagan1994.appspot.com/loginCallback"
config["CONTACTS_REDIRECT_URI"] = "http://vishaagan1994.appspot.com/oauth2callback"

if is_dev:
    config["PROFILE_REDIRECT_URI"] = "http://localhost:10080/loginCallback"
    config["CONTACTS_REDIRECT_URI"] = "http://localhost:10080/oauth2callback"
