from django.conf import settings
from Weblogin.models import *

from utils.hash import *

import datetime
import random


def make_confirm_string(user):  # generate confirm_code for user (username+c_time)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.username, now)
    ConfirmString.objects.create(code=code, user=user, )
    return code


def send_email_confirm(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自短视频分享网站的的注册确认邮件！！'

    text_content = '''感谢注册短视频分享网站，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册短视频分享网站！请点击<a href="{}/api/Weblogin/confirm/?code={}" target=blank>链接</a>，\
                    完成注册！</p>
                    <p>在这里分享你的学习与生活！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(settings.WEB_FRONT, code, settings.CONFIRM_DAYS)  # url must be corrected

    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def random_str():
    # 用randint()
    code = ''
    for i in range(6):
        n = random.randint(0, 9)
        b = chr(random.randint(65, 90))
        s = chr(random.randint(97, 122))
        code += str(random.choice([n, b, s]))
    return code
