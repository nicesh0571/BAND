from django.urls import path
from . import views

urlpatterns = [
    path('', views.camera_page, name='camera'),  # camera.html → index.html 사용 시 바꿔도 OK
    path('video_feed/', views.video_feed, name='video_feed'),
    path('label_info/', views.get_label_info, name='label_info'),
]
