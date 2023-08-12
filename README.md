# getPixivCollection

- Download your current Pixiv collections. 
- This program will only download images which have not been downloaded yet. 

## requirements

The code is based on Python 3.10. If ran improperly, please follow tips below: 

1. Install packages in **requirements.txt**
``` Shell
pip install -r requirements.txt
```
2. Switch Python version to 3.10 (low possibility, only after trying tips above and it still doesn't work)
3. If proxy is needed to access pixiv, please turn "proxy_enable" on in **config.json**, and make sure that "proxy_http" and "proxy_https" is the correct host with your proxy client (default host is "http://127.0.0.1:7890")