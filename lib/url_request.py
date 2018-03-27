# -*- coding: UTF-8 -*-
import urllib.request
import urllib.parse
import json

from friendplatform.settings import WEIXIN_APPID, WEIXIN_APPSECRET
from lib.sql_help import MySQL


class UrlRequest:
    appID = WEIXIN_APPID
    appSecret = WEIXIN_APPSECRET
    access_token = ''

    def __init__(self):
        mysql = MySQL()
        access_token = mysql.get_accecc_token()
        self.access_token = access_token

    def url_request(self, url, params=None):
        if params:
            req = urllib.request.Request(url, params)
        else:
            req = urllib.request.Request(url, params)
        res = urllib.request.urlopen(req)
        urlResp = json.loads(res.read())
        return urlResp

    def get_menu(self):
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={0}'.format(self.access_token)
        return self.url_request(url)

    def create_menu(self):
        menu = {
            "button": [
                {
                    "name": "活动",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "最新活动",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri=http%3A%2F%2Frelalive.com%2Fweixin%2Flatest%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect".format(WEIXIN_APPID)
                            # "url": "http://182.61.21.208/weixin/create1/"
                        },
                        {
                            "type": "view",
                            "name": "历史活动",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri=http%3A%2F%2Frelalive.com%2Fweixin%2Fhistory%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect".format(WEIXIN_APPID)
                            # "url": "http://182.61.21.208/weixin/create1/"
                        }
                    ]


                },
                {
                    "name": "姻缘池",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "情感专家",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri=http%3A%2F%2Frelalive.com%2Fweixin%2Fexpert%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect".format(WEIXIN_APPID)
                            # "url": "http://182.61.21.208/weixin/create1/"
                        },
                        {
                            "type": "view",
                            "name": "帅哥美女",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri=http%3A%2F%2Frelalive.com%2Fweixin%2Fbeauty%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect".format(WEIXIN_APPID)
                            # "url": "http://182.61.21.208/weixin/create1/"
                        }
                    ]

                },
                {
                    "name": "我的",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "个人中心",
                            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri=http%3A%2F%2Frelalive%2Fweixin%2Fprivatecenter%2F&response_type=code&scope=snsapi_base&state=123&connect_redirect=1#wechat_redirect".format(WEIXIN_APPID)
                            #"url": "http://182.61.21.208/weixin/others/"
                        }
                    ]
                }]
        }
        data = json.dumps(menu, ensure_ascii=False)

        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'.format(self.access_token)
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('encoding', 'utf-8')
        res = urllib.request.urlopen(req, data.encode())
        urlResp = json.loads(res.read())


if __name__ == '__main__':
    url_request = UrlRequest()
    url_request.create_menu()


