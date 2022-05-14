"""Video_Share_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/Webhome/', include(('Webhome.urls', 'Webhome'))),
    path('api/Weblogin', include(('Weblogin.urls', 'Weblogin'))),
    path('api/Webshare', include(('Websurf.urls', 'Websurf'))),
    path('api/VideoManager', include(('VideoManager.urls', 'VideoManager'))),
    path('api/UserCommunication', include(('UserCommunication.urls', 'UserCommunication'))),
    path('api/VideoInteraction', include(('VideoManager.urls', 'VideoManager'))),
]
