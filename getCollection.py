import requests
from bs4 import BeautifulSoup
import json
import re
import os

h_pic = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
    "accept-encoding": "gzip, deflate, br", 
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6", 
    "cache-control": "max-age=0", 
    "referer": "https://www.pixiv.net/", 
    "sec-ch-ua": "\"Microsoft Edge\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"", 
    "sec-ch-ua-mobile": "?0", 
    "sec-ch-ua-platform": "\"Windows\"", 
    "sec-fetch-dest": "document", 
    "sec-fetch-mode": "navigate", 
    "sec-fetch-site": "cross-site", 
    "sec-fetch-user": "?1", 
    "upgrade-insecure-requests": "1", 
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62"
}
headers = {
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Cache-Control": "max-age=0",
"Cookie": "",
"Sec-Ch-Ua-Mobile": "?0",
"Sec-Ch-Ua-Platform": "\"Windows\"",
"Sec-Fetch-Dest": "document",
"Sec-Fetch-Mode": "navigate",
"Sec-Fetch-Site": "same-origin",
"Sec-Fetch-User": "?1",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188}"
}

def downPic(url): 
    # print(url)
    pic = requests.get(url, headers=h_pic)
    if pic.status_code >= 400: 
        return False
    if "_p0." in url: 
        fileName = url.replace("_p0.",'.').split('/')[-1]
    else: 
        fileName = url.split('/')[-1]
    with open("pics/" + fileName, 'wb') as picF: 
        picF.write(pic.content)
    print("Downloaded: "+fileName)
    return True

def getWorkPics(workId): 
    targetUrl = "https://www.pixiv.net/artworks/" + workId
    page = requests.get(targetUrl, headers=headers)
    pageBS = BeautifulSoup(page.text, "html.parser")
    preload_data = pageBS.find("meta", id="meta-preload-data")
    if preload_data is None: 
        return
    jsonContent = json.loads(preload_data.get("content"))
    originalUrl = jsonContent["illust"][workId]["urls"]["original"]
    picNum = 0
    while True: 
        try: 
            matchRes = re.findall(r"_p.*\.", originalUrl)[0]
        except: 
            matchRes = re.findall(r"_.*\.", originalUrl)[0]
        originalUrl = originalUrl.replace(matchRes, "_p" + str(picNum) + '.')
        if not downPic(originalUrl): 
            return False
        picNum += 1

def getUserCollection(userNum, cookie=""): 
    offset = 0
    limit = 100
    userNum = str(userNum)
    if not os.path.exists("pics"): 
        os.mkdir("pics")

    return
    while True: 
        print(offset)
        pageUrl = "https://www.pixiv.net/ajax/user/" + userNum + "/illusts/bookmarks?tag=&offset=" + str(offset) + "&limit=" + str(limit) + "&rest=show"
        page = requests.get(pageUrl, headers=headers)
        jsonContent = json.loads(page.text)
        jsonError = jsonContent["error"]
        if jsonError: 
            break
        offset += limit
        jsonBody = jsonContent["body"]
        works = jsonBody["works"]
        if len(works) == 0: 
            break
        for item in works: 
            id = str(item["id"])
            if os.path.exists("pics/" + id + '.png') or os.path.exists("pics/" + id + '.jpg'): 
                continue
            if not getWorkPics(id): 
                continue

if __name__ == "__main__": 
    # getWorkPics(str(93548319))

    if os.path.exists("config.json"): 
        with open("config.json") as jsonF: 
            configData = json.load(jsonF)
        userId = configData["userId"]
        cookie = configData["cookie"]
        
        proxyEnable = configData["proxy_enable"]
        proxyHttp = configData["proxy_http"]
        proxyHttps = configData["proxy_https"]
        # print(userId)
        # print(cookie)
        # print(proxyEnable)
        if proxyEnable: 
            os.environ["http_proxy"] = proxyHttp
            os.environ["https_proxy"] = proxyHttps
            # print(proxyHttp)
            # print(proxyHttps)
        # getUserCollection(77636301)
    else: 
        print("Need user config! ")
    