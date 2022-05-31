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
            userID = detail_form.cleaned_data.get('userID')
            userInformation = detail_form.cleaned_data.get('userInformation')
            userSex = detail_form.cleaned_data.get('userSex')
            userBirthday = detail_form.cleaned_data.get('userBirthday')
            username = detail_form.cleaned_data.get('username')
            try:
                user = UserInfo.objects.get(userID=userID)
            except:
                return JsonResponse({'error': EditStatus.USER_NOT_EXISTS, 'msg': '用户不存在'})
            if user.username != username: #  要更改新的用户名，需要判断用户名是否重复
                repeated = UserInfo.objects.filter(username=username)
                if repeated.exists():
                    return JsonResponse({'error': 4003, 'msg': '用户名重复'})
            if username == '':
                user.username = None
            else:
                user.username = username
            if userInformation == '':
                user.userInformation = None
            else:
                user.userInformation = userInformation
            if userSex == '':
                user.userSex = None
            else:
                user.userSex = userSex
            if userBirthday == '':
                user.userBirthday = None
            else:
                user.userBirthday = userBirthday
            user.save()

            return JsonResponse({'error': SUCCESS, 'msg': '修改成功'})

        else:
            return JsonResponse({'error': FORM_ERROR})

    return JsonResponse({'error': DEFAULT})


@csrf_exempt
def upload_portrait(request):
    if request.method == 'POST':
        portrait = request.POST.get('portrait')
        userID = request.POST.get('userID')

        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': EditStatus.USER_NOT_EXISTS, 'msg': '用户不存在'})
        # print(portrait)
        if portrait is None:
            return JsonResponse({'error': 4001, 'msg': '头像为空'})

        user.userAvatar = portrait
        user.save()

        return JsonResponse({'error': SUCCESS, 'msg': '修改成功'})

    return JsonResponse({'error': DEFAULT})