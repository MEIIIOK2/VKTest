from django.urls import path
from . import views
urlpatterns = [

    path('verify/<uidb64>/<token>/',views.urlinfo),
    path('register/',views.register),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('avatar/upload/',views.upload_image),
    path('avatar/',views.get_image),
    path('csrf/',views.get_csrf),
    
]