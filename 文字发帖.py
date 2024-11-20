import requests
from requests_oauthlib import OAuth1

# 替换为你的实际 API 凭证
API_KEY = "YoC1K5OggaaTeAuWvdz3goZN4"
API_SECRET_KEY = "aq4y8kDhp6Sl2x502kSSULHdyi8CYPTJL930GehSvKY2FWLVv1"
ACCESS_TOKEN = "536554881-bZ5XSIZH6LxPqNsBLPawG9jY75Qx1l0sNaT16D2Z"
ACCESS_TOKEN_SECRET = "4D57HjX6fXrXLIOOmVeZqXUoKl6bPg2mc3EozdKCqrl1R"

# Twitter API v2 端点
url = "https://api.twitter.com/2/tweets"

# OAuth1 验证
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# 需要发布的推文内容
payload = {"text": "Hello world!"}

# 发送 POST 请求
response = requests.post(url, auth=auth, json=payload)

# 检查响应
if response.status_code == 201:
    print("Tweet posted successfully!")
    print(response.json())
else:
    print(f"Failed to post tweet: {response.status_code}")
    print(response.text)