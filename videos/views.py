from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video, Comment
from .forms import VideoForm
from .forms import CommentForm
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def home(request):
    videos = Video.objects.all()
    return render(request, 'videos/home.html', {'videos': videos})



# ログインビューをカスタマイズ
class CustomLoginView(auth_views.LoginView):
    form_class = CustomLoginForm

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # ユーザーをログアウト
    return redirect('home')  # ログアウト後にホームページにリダイレクト

@login_required  # ログイン必須
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'videos/upload_video.html', {'form': form})  # 正しいパスを指定


@login_required
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id, uploaded_by=request.user)
    if request.method == 'POST':
        video.delete()
        return redirect('home')
    return render(request, 'videos/delete_video.html', {'video': video})


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all().order_by('-created_at')  # コメント一覧
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.video = video
                comment.user = request.user
                comment.save()
                return redirect('video_detail', video_id=video.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()
    return render(request, 'videos/video_detail.html', {
        'video': video,
        'comments': comments,
        'form': form,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # メール送信
            send_mail(
                subject=f"問い合わせ: {name}",
                message=message,
                from_email=email,
                recipient_list=['tky2402049@stu.o-hara.ac.jp'],  # 受信先のメールアドレス
            )
            messages.success(request, '問い合わせを送信しました。')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'videos/contact.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'アカウント {username} が作成されました。ログインしてください。')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})