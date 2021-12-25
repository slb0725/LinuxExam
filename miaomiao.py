#!/usr/bin/python3
import time
import hmac
import hashlib
import base64
import urllib.parse
import io
import requests, json  # 导入依赖库
import sys

class DingDingHandler:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

    def get_url(self):
        timestamp = round(time.time() * 1000)
        secret_enc = self.secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        api_url = "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
            self.token, timestamp, sign
        )
        return api_url

    def ddlinksend(self, link, text, title):
        headers = {"Content-Type": "application/json"}  # 定义数据类型
        data = {
            "msgtype": "link",
            "link": {
                "text": text,
                "title": title, 
                "messageUrl": link,
            },
        }
        res = requests.post(self.get_url(), data=json.dumps(data), headers=headers)  # 发送post请求
        print(res.text)

    def ddtextsend(self, m):
        headers = {"Content-Type": "application/json"}  # 定义数据类型
        data = {
            "msgtype": "text",
            "text": {

                "content":"当前的CPU是"+m
            },
        }
        res = requests.post(self.get_url(), data=json.dumps(data), headers=headers)  # 发送post请求
        print(res.text)

m = sys.argv[1]
token="155ca1f27bd68316cf01205ef138e7bed4f0ca1b3cdf17c3667052f130017038"
secret="SEC86c90c5e3db7d95cddf2eb1c9f90c381cb4f9df827e9de1258ea4bf436837350"
dingDingHandler =DingDingHandler(token,secret)
dingDingHandler.ddtextsend(m)
