from django.urls import path
from .views import *

urlpatterns = [
    path('uploadvideo/', uploadvideo),
    path('deletevideo/', deletevideo),
    path('auditvideo/', auditvideo),
    path('getVideoByID/', getVideoByID),
    path('getVideoIDByCondition/', getVideoIDByCondition),
    path('browseVideo/', browseVideo),
    path('getAuditInfo/', getAuditInfo),
    path('sendResultInfo/', sendResultInfo),
]