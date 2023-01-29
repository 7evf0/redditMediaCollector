import praw
import requests
from tqdm import tqdm
import sys
import shutil
import json

reddit = praw.Reddit(
    client_id="Sw9CaRUEZK0cEvfn49gSDw",
    client_secret="gVgj4UJXpZfNmynd9pCxtoyollhaMQ",
    user_agent="apiConnection by u/tevf0"
)

subReddit = input("Enter the name of subreddit: ")
lim =  int(input("Enter the amount of posts you want to download from: "))

postList = iter(reddit.subreddit(subReddit).hot(limit=lim))

for i in tqdm(range(0,lim), desc="Loading: ", file=sys.stdout):
    submission = next(postList)
    mediaUrl = str(submission.url)
    imageFormats = ("image/png", "image/jpg", "image/jpeg", "image/gif", "video/mp4")

    try:
        # main url request

        req = requests.get(mediaUrl, stream=True, timeout=5)
        if req.headers["content-type"] in imageFormats and req.status_code == 200:

            req.raw.decode_content = True
            fileType = req.headers["content-type"].split('/')[1]
            link = "C:\\Users\\tevfi\\Desktop\\deneme\\" + str(i + 1) + "." + fileType
            with open(link ,"wb") as f:
                shutil.copyfileobj(req.raw, f)

        # lower media url request (mostly for videos)

        mediaJSON = eval(str(submission.media))
        mediaUrl = mediaJSON["reddit_video"]["fallback_url"]
        req = requests.get(mediaUrl, stream=True, timeout=5)

        if req.status_code == 200:
            req.raw.decode_content = True
            fileType = req.headers["content-type"].split('/')[1]
            link = "C:\\Users\\tevfi\\Desktop\\deneme\\" + str(i + 1) + "(vid)." + fileType
            with open(link ,"wb") as f:
                shutil.copyfileobj(req.raw, f)

    except:
        pass

    
