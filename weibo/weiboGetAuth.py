from weibo import APIClient
import webbrowser

APP_KEY='2428375950'
APP_SECRET='94a890eaec1d81accff336fd3c856769'

CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

url=client.get_authorize_url()
webbrowser.open_new(url)

print 'input'
code = raw_input()

r = client.request_access_token(code)
access_token = r.access_token 
expires_in = r.expires_in
print(r)

