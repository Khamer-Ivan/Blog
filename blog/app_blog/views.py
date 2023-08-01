from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth.views import LogoutView
from rest_framework.views import APIView

from .serializers import ProfileSerializer, PostCreateSerializer, PostListSerializer
from .forms import BlogRegisterForm, AuthForm, BlogTextForm
from .models import Profile, Post


def register_view(request: HttpRequest) -> HttpResponse:

    """Регистрация нового пользователя"""

    if request.method == 'POST':
        form = BlogRegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data['password1']

            user = User.objects.create_user(
                username=f'{email}1',
                password=password
            )

            Profile.objects.create(
                user=user,
                name=name,
                email=email,

            )
            username = f'{email}1'
            raw_password = password
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('app_blog:main')
    else:
        form = BlogRegisterForm()
    return render(request, 'app_blog/registration.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:

    """Вход в аккаунт для зарегистрированного пользователя"""

    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('app_blog:main')
            else:
                auth_form.add_error('__all__', 'Check the correctness of the login and password.')
    else:
        auth_form = AuthForm()
    context = {
        'form': auth_form
    }
    return render(request, 'app_blog/login.html', context=context)


class Logout(LogoutView):

    """Выход из аккаунта"""

    next_page = 'app_blog:main'


class MainView(View):

    """Главное меню"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'app_blog/main_page.html')


class ProfileView(View):

    """Страница профиля"""

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, 'app_blog/profile_page.html')


def create_post(request: HttpRequest) -> HttpResponse:

    """Метод создания нового поста"""

    if request.method == 'POST':
        form = BlogTextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')

            Post.objects.create(
                profile=request.user.user,
                title=title,
                body=body,
            )

            return redirect('app_blog:main')
    else:
        form = BlogTextForm()
    return render(request, 'app_blog/post_create.html', {'form': form})


class PostCreateView(APIView):
    def get(self, request: Request) -> HttpResponse:

        """Метод для отрисовки страницы создания поста"""

        form = BlogTextForm()
        return render(request, "app_blog/post_create.html", {'form': form})

    def post(self, request: Request) -> HttpResponse:

        """Метод создания нового поста"""

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('app_blog:profile')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(APIView):
    """Удаление существующего поста"""

    def get(self, request, post_id) -> HttpResponse:
        Post.objects.get(pk=post_id, profile=request.user.user).delete()
        return redirect('app_blog:profile')


class PostDetailsView(DetailView):
    template_name = 'app_blog/post-details.html'
    model = Post
    context_object_name = 'blog'


class ProfileListView(APIView):
    def get(self, request: Request) -> HttpResponse:

        """Метод для представления списка всех юзеров"""

        profiles = Profile.objects.all()
        serialized = ProfileSerializer(profiles, many=True)
        return render(request, 'app_blog/profile_list.html', {'profiles': serialized.data})


class UserDetailView(APIView):

    def get(self, request: Request, **kwargs) -> HttpResponse:

        """Метод для отображения детальной страницы юзера"""

        profile = Profile.objects.get(id=kwargs["pk"])
        posts = Post.objects.filter(profile=profile)
        serialized = PostListSerializer(posts, many=True)
        print(serialized.data)
        return render(request, "app_blog/user_detail.html", {"posts": serialized.data, "profile": profile})
