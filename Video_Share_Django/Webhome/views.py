from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from Webhome.form import *
from Weblogin.models import *
from utils.response_code import *


@csrf_exempt
def userinfo_edit(request):
    if request.method == 'POST':

        detail_form = DetailInfoForm(request.POST)

        if detail_form.is_valid():
            username = detail_form.cleaned_data.get('username')
            userInformation = detail_form.cleaned_data.get('userInformation')
            userSex = detail_form.cleaned_data.get('userSex')
            userBirthday = detail_form.cleaned_data.get('userBirthday')

            user_id = request.session.get('id')

            if user_id.exists():
                try:
                    user = UserInfo.objects.get(userID=user_id)
                except:
                    return JsonResponse({'error': EditStatus.USER_NOT_EXIST, 'msg': '用户不存在'})

                user.username = username
                user.userInformation = userInformation
                user.userSex = userSex
                user.userBirthday = userBirthday
                user.save()

                return JsonResponse({'error': SUCCESS, 'msg': '修改成功'})

            else:
                return JsonResponse({'error': EditStatus.USER_NOT_LOGIN, 'msg': '用户未登录'})

        else:
            return JsonResponse({'error': FORM_ERROR})

    return JsonResponse({'error': DEFAULT})
