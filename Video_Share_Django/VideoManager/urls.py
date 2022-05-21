from django.urls import path
from .views import *

urlpatterns = [
    path('followuser', followuser),
    path('cancelfollow', cancelfollow),
    path('sendletter', sendletter),
    path('enterhomepage', enterhomepage),

]