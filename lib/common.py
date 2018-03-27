import time

import datetime

from friendplatform.settings import WEIXIN_APPID, WEIXIN_APPSECRET
from lib.url_request import UrlRequest
from weixin.models import Customer


def create_timestamp():
    return int(time.time())


def subcribe_save_openid(openid):
    createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    customer_dict = {'openid': openid,
                     'createtime': createtime
                     }
    print('openid is,', openid)
    customers = Customer.objects.filter(openid=openid)

    if customers:
        Customer.objects.create(**customer_dict)


def get_openid(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
        WEIXIN_APPID, WEIXIN_APPSECRET, code)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp['openid']
