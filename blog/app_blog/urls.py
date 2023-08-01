from django.urls import path
from .views import (Logout,
                    register_view,
                    MainView,
                    login_view,
                    ProfileListView,
                    ProfileView,
                    UserDetailView,
                    PostCreateView,
                    PostDeleteView,
                    )

app_name = 'app_blog'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('login/', login_view, name='login'),
    path('logout/', Logout.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('profile_list/', ProfileListView.as_view(), name='profile_list'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_detail/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('posts/<int:post_id>/delete/', PostDeleteView.as_view(), name='post_delete')

]
