from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from Weblogin.models import UserInfo
from VideoManager.models import VideoInfo
from VideoInteraction.models import LikeRecord
from VideoInteraction.models import Favourites
from VideoInteraction.models import VideoComment
from VideoManager.models import AuditRecord


@csrf_exempt  # 跨域设置
def like(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        likeuser = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        likeduser = video.videoUpUser
        LikeRecord.objects.create(likeUser=likeuser, likedUser=likeduser, likeVideo=video)
        video.videoLikeNum = video.videoLikeNum + 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "点赞成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancellike(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        likeuser = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        likeduser = video.videoUpUser
        LikeRecord.objects.get(likeUser=likeuser, likedUser=likeduser, likeVideo=video).delete()
        video.videoLikeNum = video.videoLikeNum - 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "取消点赞成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def favourites(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        user = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        Favourites.objects.create(favorUser=user, favorVideo=video)
        video.videoFavorNum = video.videoFavorNum + 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancalfavourites(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        user = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        Favourites.objects.get(favorUser=user, favorVideo=video).delete()
        video.videoFavorNum = video.videoFavorNum - 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "取消收藏成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def comment(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        comment = request.POST.get('commit')
        fathercomment = request.POST.get('fathercomm')
        user = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        commentteduser = video.videoUpUser
        VideoComment.objects.create(commentUpUser=commentteduser, commentComUser=user, commentVideo=video,
                                    commentContent=comment, parentComment=fathercomment)
        video.videoCommentNum = video.videoCommentNum + 1
        return JsonResponse({'error': 0, 'msg': "评论成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelcomment(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        comment = request.POST.get('commit')
        fathercomment = request.POST.get('fathercomm')
        user = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        commentteduser = video.videoUpUser
        VideoComment.objects.get(commentUpUser=commentteduser, commentComUser=user, commentVideo=video,
                                    commentContent=comment, parentComment=fathercomment).delete()
        video.videoCommentNum = video.videoCommentNum - 1
        return JsonResponse({'error': 0, 'msg': "取消评论成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def editcomment(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        videoid = request.POST.get('videoid')
        comment = request.POST.get('commit')
        fathercomment = request.POST.get('fathercomm')
        newcomment = request.POST.get('newcomment')
        user = UserInfo.objects.get(userID=userid)
        video = VideoInfo.objects.get(videoid=videoid)
        commentteduser = video.videoUpUser
        precomment = VideoComment.objects.get(commentUpUser=commentteduser, commentComUser=user, commentVideo=video,
                                    commentContent=comment, parentComment=fathercomment)
        precomment.commentContent = newcomment
        precomment.save()
        return JsonResponse({'error': 0, 'msg': "编辑成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def complaintvideo(request):
    if request.method == 'POST':
        videoid = request.POST.get('videoid')
        complaintuserid = request.POST.get('complaintuserid')
        complainreason = request.POST.get('complainreason')
        video = VideoInfo.objects.get(videoid=videoid)
        complaintuser = UserInfo.objects.get(userID=complaintuserid)
        complainteduser = video.videoUpUser
        AuditRecord.objects.create(auditVideo=video, complainUser=complaintuser, complainedUser=complainteduser,
                                   complainReason=complainreason, adminUser=None, auditTime=None, auditResult=None)
        return JsonResponse({'error': 0, 'msg': "投诉成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
