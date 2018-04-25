import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.events import SubscribeEvent
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from friendplatform.settings import WECHAT_TOKEN, NUMBER_TYPE, START_YEAR
from lib.common import create_timestamp, subcribe_save_openid, get_openid, get_user_info
from weixin.models import Issue, Member, Pic, Expert, StudyMember
import logging

log = logging.getLogger('django')


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
            reply_template = "<xml><ToUserName><![CDATA[{}]]></ToUserName>" \
                             "<FromUserName><![CDATA[{}]]></FromUserName>" \
                             "<CreateTime>{}</CreateTime>" \
                             "<MsgType><![CDATA[text]]></MsgType>" \
                             "<Content><![CDATA[{}]]></Content></xml>"

            content = '公众号首页暂不支持自动回复客服消息，请转到-我的->建议与反馈中留言，给您带来的不便，敬请谅解'

            reply = reply_template.format(msg.source, msg.target, str(create_timestamp()), content)
            return HttpResponse(reply, content_type="application/xml")
        elif msg.type == 'event':
            subcribe_event = SubscribeEvent(msg)
            if msg.event == subcribe_event.event:
                reply_msg = '欢迎来到，全球高端白领交友平台，我们终于等到你了'
                reply = create_reply(reply_msg, msg)
                log.info('create reply successfully')
                openid = msg.source
                subcribe_save_openid(openid)
            else:
                return 'success'
        else:
            return 'success'
        response = HttpResponse(reply.render(), content_type="application/xml")

        return response
    else:
        log.info('error')
        return 'error'


def privatecenter(request):
    template_name = 'weixin/privatecenter.html'

    open_id = get_open_id(request)

    #user = get_user_info(open_id)
    #headimgurl = user['headimgurl']
    #nick_name = user['nickname']
    headimgurl = ''
    nick_name = 'test'
    context = {
        'open_id': open_id,
        'headimgurl': headimgurl,
        'nickname': nick_name
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


def join(member_type, open_id):
    years = {}
    months = {}
    days = {}
    start_value = START_YEAR

    for i in range(80):
        years[i+1] = start_value - i

    start_value = 1

    for i in range(12):
        months[i+1] = start_value + i

    start_value = 1

    for i in range(31):
        days[i+1] = start_value + i

    context = {
        'member_type': member_type,
        'open_id': open_id,
        'years': years,
        'months': months,
        'days': days,
        'number_type': NUMBER_TYPE
    }

    return context


def expert_join(request):
    template_name = 'weixin/join.html'
    open_id = get_open_id(request)

    member_type = 0
    context = join(member_type, open_id)

    response = render(request, template_name, context)
    return response


def member_join(request):
    template_name = 'weixin/join.html'
    open_id = get_open_id(request)

    member_type = 1
    context = join(member_type, open_id)

    response = render(request, template_name, context)
    return response


def coordinate(request):
    template_name = 'weixin/coordinate.html'
    open_id = get_open_id(request)

    context = {}

    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_member(request):
    template_name = 'weixin/join2.html'
    open_id = get_open_id(request)
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
        home_city = request.POST.get('home-city', None)
        member_type = request.POST.get('member_type', None)
        member_dict = {
            'name': name,
            'phone_number': phone_number,
            'weixin_qq': number_type + ':' + number,
            'sex': sex,
            'birth': datetime.datetime.strptime(str(START_YEAR - int(birth_year) + 1) + '-' + str(birth_month) + '-' + str(birth_day), '%Y-%m-%d'),
            'location': home_city,
            'createtime': datetime.datetime.now(),
            'open_id': open_id,
        }

        try:
            member_exist = Member.objects.filter(open_id=open_id)
            if member_exist:
                template_name = 'weixin/exception.html'
                context = {
                    'exception': '已是会员，无法再次加入'
                }
                response = render(request, template_name, context)
                return response
            Member.objects.create(**member_dict)
        except Exception as ex:
            template_name = 'weixin/exception.html'
            print('create member exception, ', str(ex))
            context = {
                'exception': str(ex)
            }
            response = render(request, template_name, context)
            return response

        context = {
            'member_type': member_type
        }
        response = render(request, template_name, context)
        return response


def test(request):
    template_name = 'weixin/join2.html'

    context = {

    }
    response = render(request, template_name, context)
    return response


@csrf_exempt
def detail_submit(request):
    open_id = get_open_id(request)
    if request.method == 'POST':
        member_type = request.POST.get('member_type', None)
        description = request.POST.get('description', None)

        member = Member.objects.filter(open_id=open_id)
        if member:

            if int(member_type) == 0:
                expert_dict = {
                    'grade': 3,
                    'online': 1,
                    'member_id': member.first().id,
                    'description': description,
                    'createtime': datetime.datetime.now()
                }
                Expert.objects.create(**expert_dict)
            else:
                study_dict = {
                    'member_id': member.first().id,
                    'description': description,
                    'createtime': datetime.datetime.now(),
                    'member_type': 0
                }
                StudyMember.objects.create(**study_dict)




    return HttpResponseRedirect('/weixin/privatecenter')


@csrf_exempt
def issue(request):
    template_name = 'weixin/issue.html'

    open_id = get_open_id(request)

    context = {
        'open_id': open_id
    }

    response = render(request, template_name, context)
    return response


@csrf_exempt
def save_issue(request):
    open_id = get_open_id(request)
    if request.method == 'POST':
        issue_type = request.POST.get('issue-type', None)
        description = request.POST.get('issue', None)

        issue_dict = {'issue_type': issue_type,
                      'description': description,
                      'owner': open_id,
                      'createtime': datetime.datetime.now()}

        try:
            Issue.objects.create(**issue_dict)
        except Exception as ex:
            print(str(ex))
            return HttpResponseRedirect('/weixin/exception/')

        return HttpResponseRedirect('/weixin/privatecenter/')


@csrf_exempt
def about(request):
    template_name = 'weixin/about.html'

    response = render(request, template_name)
    return response


@csrf_exempt
def exception(request):
    template_name = 'weixin/exception.html'

    response = render(request, template_name)
    return response


@csrf_exempt
def upload(request):
    return HttpResponse('')


@csrf_exempt
def save_image(request):
    log.info('start save image...')
    open_id = get_open_id(request)
    binary = request.POST.get('img_src', None)

    pics = Pic.objects.filter(own_id=open_id)

    createtime = datetime.datetime.now()

    pics_len = len(pics)
    pic_dict = {
        'index': pics_len + 1,
        'binary': binary,
        'own_id': open_id,
        'createtime': createtime
    }
    try:
        log.info(' start create pic')
        Pic.objects.create(**pic_dict)
    except Exception as ex:
        return HttpResponse('fail')
    return HttpResponse('success')


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

