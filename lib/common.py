import time

import datetime

from wechatpy import WeChatClient

from friendplatform.settings import WEIXIN_APPID, WEIXIN_APPSECRET
from lib.url_request import UrlRequest
from weixin.models import Customer, StudyMember, Member, Expert


def create_timestamp():
    return int(time.time())


def subcribe_save_openid(openid):
    createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    customer_dict = {'openid': openid,
                     'createtime': createtime
                     }
    customers = Customer.objects.filter(openid=openid)

    if len(customers) == 0:
        Customer.objects.create(**customer_dict)
    else:
        print('customer exists already')


def get_openid(code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code'.format(
        WEIXIN_APPID, WEIXIN_APPSECRET, code)

    url_req = UrlRequest()
    resp = url_req.url_request(url)
    return resp['openid']


def get_user_info(openid):
    client = WeChatClient(WEIXIN_APPID, WEIXIN_APPSECRET)
    user = client.user.get(openid)
    return user


def is_studymember(openid):
    member = Member.objects.filter(open_id=openid)
    if member:
        studymember = StudyMember.objects.filter(member=member.first())
        if studymember:
            return True
    return False


def is_expertmember(openid):
    member = Member.objects.filter(open_id=openid)
    if member:
        expert = Expert.objects.filter(member=member.first())
        if expert:
            return True
    return False
