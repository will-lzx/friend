from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from friendplatform.settings import WECHAT_TOKEN
from lib.common import create_timestamp, subcribe_save_openid, get_openid


@csrf_exempt
def wx(request):
    if request.method == 'GET':
        print('wx get msg')
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

    context = {
        'open_id': open_id,
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
