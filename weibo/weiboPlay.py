import requests

url = "https://api.weibo.com/2/comments/create.json"

playload = {
"access_token":"2.00EN534CCWN2eC06a8928bddfJWpkC",
"comment":"Test!",
"id":1515422624413
}

r = requests.post(url,data = playload)
