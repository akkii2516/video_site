from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # 標準のログインビュー
    path('logout/', views.logout_view, name='logout'),  # カスタムログアウトビュー
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # 動画詳細
    path('contact/', views.contact, name='contact'),  # 問い合わせページ
    path('signup/', views.signup, name='signup'),
]
