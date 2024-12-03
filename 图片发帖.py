import requests
from requests_oauthlib import OAuth1

# 替换为你的实际 API 凭证
API_KEY = "YoC1K5OggaaTeAuWvdz3goZN4"
API_SECRET_KEY = "aq4y8kDhp6Sl2x502kSSULHdyi8CYPTJL930GehSvKY2FWLVv1"
ACCESS_TOKEN = "536554881-bZ5XSIZH6LxPqNsBLPawG9jY75Qx1l0sNaT16D2Z"
ACCESS_TOKEN_SECRET = "4D57HjX6fXrXLIOOmVeZqXUoKl6bPg2mc3EozdKCqrl1R"

# OAuth1 验证
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# 上传图片
def upload_image(image_path):
    """
    上传图片到 Twitter，并返回 media_id
    """
    url = "https://upload.twitter.com/1.1/media/upload.json"

    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(url, auth=auth, files=files)

    if response.status_code == 200:
        media_id = response.json().get("media_id_string")
        print(f"Image uploaded successfully! Media ID: {media_id}")
        return media_id
    else:
        print(f"Failed to upload image: {response.status_code}")
        print(response.text)
        return None

# 发布推文
def post_tweet_with_image(media_id, text):
    """
    使用上传的图片发布推文
    """
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": text,
        "media": {"media_ids": [media_id]}
    }

    response = requests.post(url, auth=auth, json=payload)

    if response.status_code == 201:
        print("Tweet posted successfully!")
        print(response.json())
    else:
        print(f"Failed to post tweet: {response.status_code}")
        print(response.text)

# 主函数
def upload_and_post_image(image_path, tweet_text):
    """
    完整流程：上传图片 -> 发布推文
    """
    media_id = upload_image(image_path)
    if media_id:
        post_tweet_with_image(media_id, tweet_text)

# 图片路径和推文内容
image_path = "aa1.png"  # 替换为你的图片路径
tweet_text = "币圈搞钱路径。#BTC #比特币"  # 替换为你的推文内容

# 执行上传并发布推文
upload_and_post_image(image_path, tweet_text)