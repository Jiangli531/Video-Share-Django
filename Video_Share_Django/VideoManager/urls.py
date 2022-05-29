from django.urls import path
from .views import *

urlpatterns = [
    path('uploadvideo/', uploadvideo),
    path('deletevideo/', deletevideo),
    path('auditvideo/', auditvideo),
]