from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from friendplatform.settings import WECHAT_TOKEN, NUMBER_TYPE
from lib.common import create_timestamp, subcribe_save_openid, get_openid


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echostr = request.GET.get('echostr', '')

        try:
            check_signature(WECHAT_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echostr = 'error'
        return HttpResponse(echostr, content_type="text/plain")
    if request.method == 'POST':
        msg = parse_message(request.body)
        if msg.type == 'text' or msg.type == 'image' or msg.type == 'voice':
            reply = '<xml><ToUserName><![CDATA[' + msg.source + ']]></ToUserName><FromUserName><![CDATA[' + msg.target + \
                    ']]></FromUserName><CreateTime>' + str(create_timestamp()) + '</CreateTime><MsgType><![CDATA[transfer_customer_service]]></MsgType></xml>'
            return HttpResponse(reply, content_type="application/xml")
        elif msg.type == 'event':
            subcribe_event = SubscribeEvent(msg)
            if msg.event == subcribe_event.event:
                reply_msg = '欢迎来到，全球高端白领交友平台，我们终于等到你了'
                reply = create_reply(reply_msg, msg)
                openid = msg.source
                subcribe_save_openid(openid)
            else:
                return 'success'
        else:
            return 'success'
        response = HttpResponse(reply.render(), content_type="application/xml")

        return response
    else:
        print('error')


def privatecenter(request):
    template_name = 'weixin/privatecenter.html'

    open_id = get_open_id(request)
    headimgurl = ''
    nickname = 'nickname'

    context = {
        'open_id': open_id,
        'headimgurl': headimgurl,
        'nickname': nickname
    }

    response = render(request, template_name, context)
    return response


def latest(request):
    template_name = 'weixin/latest.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
    }

    response = render(request, template_name, context)
    return response


def history(request):
    template_name = 'weixin/history.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
    }

    response = render(request, template_name, context)
    return response


def expert(request):
    template_name = 'weixin/experts.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
    }

    response = render(request, template_name, context)
    return response


def join(request):
    template_name = 'weixin/join.html'

    open_id = get_open_id(request)
    years = {}
    months = {}
    days = {}
    start_value = 2030

    for i in range(80):
        years[i+1] = start_value - i

    start_value = 1

    for i in range(12):
        months[i+1] = start_value + i

    start_value = 1

    for i in range(31):
        days[i+1] = start_value + i

    context = {
        'open_id': open_id,
        'years': years,
        'months': months,
        'days': days,
        'number_type': NUMBER_TYPE
    }

    response = render(request, template_name, context)
    return response


@csrf_exempt
def join2(request):
    template_name = 'weixin/join2.html'
    if request.method == 'POST':
        name = request.POST.get('name', None)
        sex = request.POST.get('sex', None)
        number_type = request.POST.get('number-type', None)
        number = request.POST.get('number', None)
        number_location = request.POST.get('number-location', None)
        phone_number = request.POST.get('phone-number', None)
        birth_year = request.POST.get('birth-year', None)
        birth_month = request.POST.get('birth-month', None)
        birth_day = request.POST.get('birth-day', None)

        context = {
            'name': name,
            'sex': sex,
            'number_type': number_type,
            'number': number,
            'number_location': number_location,
            'phone_number': phone_number,
            'birth_year': birth_year,
            'birth_month': birth_month,
            'birth_day': birth_day
        }
        response = render(request, template_name, context)
        return response


@csrf_exempt
def upload(request):
    return HttpResponse('')


def beauty(request):
    template_name = 'weixin/beauties.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id,
    }

    response = render(request, template_name, context)
    return response


def get_open_id(request):
    code = request.GET.get('code', None)

    if code and not request.session.get('openid', default=None):
        openid = get_openid(code)
        request.session['openid'] = openid
        print('save session', openid)
    else:
        openid = request.session.get('openid', default=None)
        print('session get', openid)

    return openid
