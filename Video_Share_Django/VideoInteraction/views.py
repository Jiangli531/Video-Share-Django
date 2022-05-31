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
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        try:
            like_user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        liked_user = video.videoUpUser
        if LikeRecord.objects.filter(likeUser=like_user, likeVideo=video).exists():
            return JsonResponse({'error': 4001, 'msg': "已点赞"})
        LikeRecord.objects.create(likeUser=like_user, likedUser=liked_user, likeVideo=video)
        video.videoLikeNum = video.videoLikeNum + 1
        liked_user.TotalLikeNum = liked_user.TotalLikeNum + 1 # 更新用户点赞总数
        liked_user.save()
        video.save()
        return JsonResponse({'error': 0, 'msg': "点赞成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancellike(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        try:
            like_user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        liked_user = video.videoUpUser
        if LikeRecord.objects.filter(likeUser=like_user, likedVideo=video).exists():
            LikeRecord.objects.get(likeUser=like_user, likedUser=liked_user, likeVideo=video).delete()
            liked_user.TotalLikeNum = liked_user.TotalLikeNum - 1 # 更新用户点赞总数
            liked_user.save()
            video.videoLikeNum = video.videoLikeNum - 1
            video.save()
            return JsonResponse({'error': 0, 'msg': "取消点赞成功"})
        else:
            return JsonResponse({'error': 4001, 'msg': "还未点赞"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def favourites(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        if Favourites.objects.filter(favorUser=user, favorVideo=video).exists():
            return JsonResponse({'error': 4001, 'msg': "已收藏"})
        else:
            Favourites.objects.create(favorUser=user, favorVideo=video)
            video.videoFavorNum = video.videoFavorNum + 1
            video.save()
            return JsonResponse({'error': 0, 'msg': "收藏成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancalfavourites(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        if Favourites.objects.filter(favorUser=user, favorVideo=video).exists():
            Favourites.objects.get(favorUser=user, favorVideo=video).delete()
            video.videoFavorNum = video.videoFavorNum - 1
            video.save()
            return JsonResponse({'error': 0, 'msg': "取消收藏成功"})
        else:
            return JsonResponse({'error': 4001, 'msg': "还未收藏"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def comment(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        comment = request.POST.get('comment')
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4001, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4002, 'msg': "视频不存在"})
        commentted_user = video.videoUpUser
        VideoComment.objects.create(commentUpUser=commentted_user, commentComUser=user, commentVideo=video,
                                    commentContent=comment)
        video.videoCommentNum = video.videoCommentNum + 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "评论成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def cancelcomment(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        comment = request.POST.get('comment')
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        commentted_user = video.videoUpUser
        try:
            VideoComment.objects.get(commentUpUser=commentted_user, commentComUser=user, commentVideo=video,
                                    commentContent=comment).delete()
        except:
            return JsonResponse({'error': 4001, 'msg': "评论不存在"})
        video.videoCommentNum = video.videoCommentNum - 1
        video.save()
        return JsonResponse({'error': 0, 'msg': "取消评论成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def editcomment(request):
    if request.method == 'POST':
        userID = request.POST.get('userID')
        videoID = request.POST.get('videoID')
        comment = request.POST.get('comment')
        new_comment = request.POST.get('newComment')
        try:
            user = UserInfo.objects.get(userID=userID)
        except:
            return JsonResponse({'error': 4002, 'msg': "用户不存在"})
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4003, 'msg': "视频不存在"})
        commentted_user = video.videoUpUser
        try:
            pre_comment = VideoComment.objects.get(commentUpUser=commentted_user, commentComUser=user, commentVideo=video,
                                    commentContent=comment)
        except:
            return JsonResponse({'error': 4001, 'msg': "评论不存在"})
        pre_comment.commentContent = new_comment
        pre_comment.save()
        return JsonResponse({'error': 0, 'msg': "编辑成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})


@csrf_exempt  # 跨域设置
def complaintvideo(request):
    if request.method == 'POST':
        videoID = request.POST.get('videoID')
        complaint_userID = request.POST.get('complaintUserID')
        complain_reason = request.POST.get('complainReason')
        try:
            video = VideoInfo.objects.get(videoID=videoID)
        except:
            return JsonResponse({'error': 4001, 'msg': "视频不存在"})
        complaint_user = UserInfo.objects.get(userID=complaint_userID)
        complainted_user = video.videoUpUser
        AuditRecord.objects.create(auditVideo=video, complainUser=complaint_user, complainedUser=complainted_user,
                                   complainReason=complain_reason)
        return JsonResponse({'error': 0, 'msg': "投诉成功"})
    else:
        return JsonResponse({'error': 2001, 'msg': "请求方式错误"})
