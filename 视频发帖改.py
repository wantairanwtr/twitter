import os
import requests
from requests_oauthlib import OAuth1
import time

# 替换为你的实际 API 凭证
API_KEY = "YoC1K5OggaaTeAuWvdz3goZN4"
API_SECRET_KEY = "aq4y8kDhp6Sl2x502kSSULHdyi8CYPTJL930GehSvKY2FWLVv1"
ACCESS_TOKEN = "536554881-bZ5XSIZH6LxPqNsBLPawG9jY75Qx1l0sNaT16D2Z"
ACCESS_TOKEN_SECRET = "4D57HjX6fXrXLIOOmVeZqXUoKl6bPg2mc3EozdKCqrl1R"

# OAuth1 验证
auth = OAuth1(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# 初始化上传
def initialize_upload(video_path):
    url = "https://upload.twitter.com/1.1/media/upload.json"
    video_size = os.path.getsize(video_path)

    params = {
        "command": "INIT",
        "media_type": "video/mp4",
        "total_bytes": video_size,
        "media_category": "tweet_video"
    }

    response = requests.post(url, auth=auth, data=params)
    if response.status_code in [200, 202]:
        media_id = response.json()["media_id_string"]
        print(f"Initialized upload. Media ID: {media_id}")
        return media_id
    else:
        print(f"Failed to initialize upload: {response.status_code}")
        print(response.text)
        return None

# 分块上传
def append_upload(video_path, media_id):
    url = "https://upload.twitter.com/1.1/media/upload.json"
    chunk_size = 5 * 1024 * 1024  # 5MB
    with open(video_path, "rb") as video_file:
        index = 0
        while chunk := video_file.read(chunk_size):
            params = {
                "command": "APPEND",
                "media_id": media_id,
                "segment_index": index
            }
            files = {"media": chunk}
            response = requests.post(url, auth=auth, data=params, files=files)

            if response.status_code == 204:
                print(f"Uploaded chunk {index} successfully.")
            else:
                print(f"Failed to upload chunk {index}: {response.status_code}")
                print(response.text)
                return False
            index += 1
    return True

# 完成上传
def finalize_upload(media_id):
    url = "https://upload.twitter.com/1.1/media/upload.json"
    params = {
        "command": "FINALIZE",
        "media_id": media_id
    }
    response = requests.post(url, auth=auth, data=params)

    if response.status_code == 200:
        processing_info = response.json().get("processing_info")
        if processing_info:
            state = processing_info.get("state")
            print(f"Upload finalized. State: {state}")
            return processing_info
        else:
            print("Upload finalized successfully.")
            return None
    else:
        print(f"Failed to finalize upload: {response.status_code}")
        print(response.text)
        return None

# 查询视频处理状态
def check_status(media_id):
    url = f"https://upload.twitter.com/1.1/media/upload.json"
    params = {
        "command": "STATUS",
        "media_id": media_id
    }
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 200:
        return response.json()["processing_info"]
    else:
        print(f"Failed to check status: {response.status_code}")
        print(response.text)
        return None

# 使用 OAuth 1.0a 在 Twitter API v2 发布推文
def post_tweet_with_video(media_id, text):
    tweet_url = "https://api.twitter.com/2/tweets"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "media": {
            "media_ids": [media_id]
        }
    }
    response = requests.post(tweet_url, auth=auth, json=payload)

    if response.status_code == 201:
        print("Tweet posted successfully!")
        print(response.json())
    else:
        print(f"Failed to post tweet: {response.status_code}")
        print(response.text)

# 主流程
def upload_and_post_video(video_path, tweet_text):
    media_id = initialize_upload(video_path)
    if not media_id:
        return

    if not append_upload(video_path, media_id):
        return

    processing_info = finalize_upload(media_id)
    if processing_info:
        state = processing_info.get("state")
        while state not in ("succeeded", "failed"):
            print(f"Checking status: {state}")
            time.sleep(5)  # 每 5 秒检查一次状态
            processing_info = check_status(media_id)
            state = processing_info.get("state")

        if state == "failed":
            print("Video processing failed.")
            return

    post_tweet_with_video(media_id, tweet_text)

# 视频路径和推文内容
video_path = "a1.mp4"
tweet_text = "This is a tweet with a video!"

# 执行上传并发布推文
upload_and_post_video(video_path, tweet_text)
