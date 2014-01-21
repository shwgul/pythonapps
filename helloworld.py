import webapp2
import sys
import urllib2
import urllib
import json
import urlparse
def parse_str(str):
    nvps={};
    list = str.rsplit("&")
    for el in list:
        nvplist = el.rsplit("=")
        nvps[nvplist[0]]=nvplist[1]
    return nvps
 
def getAccessTokenDetails(app_id,app_secret,redirect_url,code):
    list ={}
    url =  "https://graph.facebook.com/oauth/access_token?client_id="+app_id+"&redirect_uri="+redirect_url+"&client_secret="+app_secret+"&code="+code;    
    req = urllib2.Request(url)
    try: 
        response= urllib2.urlopen(req)
        str=response.read()
        #you can replace it with urlparse.parse_qs
        list = parse_str(str)
 
    except Exception, e:
        print e
    return list
 
def getUserDetails(access_token):
    list={}
    url = "https://graph.facebook.com/me?access_token="+access_token;
    req = urllib2.Request(url)
    try: 
        response= urllib2.urlopen(req)
        str=response.read()
        list = json.dumps(str)
    except Exception, e:
        print e
 
    return list
 
class MainPage(webapp2.RequestHandler):
    def get(self):        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
        CODE = self.request.get("code")
        APP_ID = "498168906966525"
        APP_SECRET = "b80451100b6afe0256d8805b0513f720"
        REDIRECT_URL='http://coolpydev.appspot.com/login'
        details = getAccessTokenDetails(APP_ID, APP_SECRET, REDIRECT_URL, CODE)
        if not details["access_token"] is None:
            jsonText =getUserDetails(details["access_token"])
            jsonText =json.loads(jsonText)
            userInfo =json.loads(jsonText)
            self.response.write("Name: "+ userInfo['name'])
        
class Welcome(webapp2.RequestHandler):
    def get(self):
         self.response.headers['Content-Type'] = 'text/html'
         self.response.write("<html>")
         self.response.write("<body>")
         self.response.write("Hi, login here <a href=\"http://www.facebook.com/dialog/oauth/?client_id=498168906966525&redirect_uri=http://coolpydev.appspot.com/login&state=RANDOM_NUMBER_PREVENT_CSRF&scope=email,read_friendlists&response_type=code\">Login</a>");
         self.response.write("</body>")
         self.response.write("</html>")
application = webapp2.WSGIApplication([
    ('/', Welcome),
    ('/login', MainPage),
], debug=True)
