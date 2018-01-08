from weibo import APIClient
import webbrowser

def get_access_token(app_key, app_secret, callback_url):
    client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=callback_url)
    auth_url = client.get_authorize_url()
    webbrowser.open_new(auth_url)
    code = raw_input("Input code:")
    r = client.request_access_token(code)
    access_token = r.access_token
    expires_in = r.expires_in
    print 'access_token:', access_token
    print 'expires_in:', expires_in

    return access_token, expires_in
def init_login():
    app_key = '2428375950'
    app_secret = '94a890eaec1d81accff336fd3c856769'
    callback_url = 'https://api.weibo.com/oauth2/default.html'
    access_token, expires_in = get_access_token(app_key, app_secret,callback_url)
    #print "access_token = %s, expires_in = %s" % (access_token, expires_in)
    # access_token = 'xxxxxxxx'
    # expires_in = 'xxxxxx'
    client = APIClient(app_key=app_key, app_secret=app_secret)
    client.set_access_token(access_token, expires_in)
    return client


def send_pic(client,picpath,message):
    # send a weibo with img
    f = open(picpath, 'rb')
    mes = message.decode('utf-8')
    client.statuses.upload.post(status=mes, pic=f)
    f.close()  
    print u"works"

def send_mes(client,message):
    utext = unicode(message,"UTF-8")
    client.post.statuses__update(status=utext)
    print u"works!"


if __name__ == '__main__':
    client = init_login()
    mes = "TEST"
    send_mes(client,mes)
 

