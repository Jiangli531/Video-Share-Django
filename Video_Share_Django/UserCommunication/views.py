import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Weblogin.models import UserInfo
from UserCommunication.models import UserConnection
from UserCommunication.models import UserLetter
from utils.response_code import SUCCESS


@csrf_exempt  # 跨域设置
def followuser(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.create(followerUser=user, followedUser=followeduser)
        followeduser.FansNum = followeduser.FansNum + 1
        followeduser.save()
        user.ConcernsNum = user.ConcernsNum + 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelfollow(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        followeduserid = request.POST.get('followeduserid')
        user = UserInfo.objects.get(userID=userid)
        followeduser = UserInfo.objects.get(userID=followeduserid)
        UserConnection.objects.get(followerUser=user, followedUser=followeduser).delete()
        followeduser.FansNum = followeduser.FansNum - 1
        followeduser.save()
        user.ConcernsNum = user.ConcernsNum - 1
        user.save()
        return JsonResponse({'error': 0, 'msg': "取消关注成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def sendletter(request):
    if request.method == 'POST':
        letteruserid = request.POST.get('letteruserid')
        lettereduserid = request.POST.get('lettereduserid')
        lettertext = request.POST.get('lettertext')
        letteruser = UserInfo.objects.get(userID=letteruserid)
        lettereduser = UserInfo.objects.get(userID=lettereduserid)
        UserLetter.objects.create(letterUser=letteruser, letteredUser=lettereduser, letterText=lettertext)
        return JsonResponse({'error': 0, 'msg': "私信已发送"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def enterhomepage(request):
    if request.method == 'POST':
        entereduserid = request.POST.get('entereduserid')
        entereduser = UserInfo.objects.get(userID=entereduserid)
        username = entereduser.username
        userportrait = entereduser.userPortrait
        userinformation = entereduser.userInformation
        usersex = entereduser.userSex
        userbirthday = entereduser.userBirthday
        fansnum = entereduser.FansNum
        playnum = entereduser.TotalPlayNum
        concernsnum = entereduser.ConcernsNum
        msg_list = []
        msg_item = {
            'userid': entereduserid,
            'username': username,
            'userportrait': userportrait,
            'userinformation': userinformation,
            'usersex': usersex,
            'userbirthday': userbirthday,
            'fansnum': fansnum,
            'playnum': playnum,
            'concernsnum': concernsnum,
        }
        msg_list.append(msg_item)
        video_list = []
        for video in entereduser.Video.all():
            video_item = {
                'videoid': video.videoID,
                'videotitle': video.videoTitle,
                'videoplaynum': video.videoPlayNum,
                'videocommentnum': video.videoCommentNum,
                'videopublishtime': video.videoPublishTime,
                'videopublishuser': video.videoPublishUser.username,
                'videocover': video.videoCover,
            }
            video_list.append(video_item)
        fanslist = []
        for user in UserConnection.objects.filter(followedUser=entereduser):
            fans_item = {
                'userid': user.userID,
                'username': user.username,
                'userportrait': user.userPortrait,
                'userinformation': user.userInformation,
            }
            fanslist.append(user)

        concernslist = []
        for user in UserConnection.objects.filter(followerUser=entereduser):
            concerns_item = {
                'userid': user.userID,
                'username': user.username,
                'userportrait': user.userPortrait,
                'userinformation': user.userInformation,
            }
            concernslist.append(user)

        return JsonResponse({'error': SUCCESS, 'msg_list': json.dumps(msg_list, ensure_ascii=False),
                             'video_list': json.dumps(video_list, ensure_ascii=False),
                             'fanslist': json.dumps(fanslist, ensure_ascii=False),
                             'concernslist': json.dumps(concernslist, ensure_ascii=False)})

    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
