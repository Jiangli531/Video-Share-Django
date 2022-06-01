from django.urls import path
from .views import *

urlpatterns = [
    path('like/', like),
    path('cancellike/', cancellike),
    path('favourites/', favourites),
    path('cancalfavourites/', cancelfavourites),
    path('comment/', comment),
    path('cancelcomment/', cancelcomment),
    path('editcomment/', editcomment),
    path('complaintvideo/', complaintvideo),

]