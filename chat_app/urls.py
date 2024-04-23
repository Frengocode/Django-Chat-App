# chat/urls.py

from django.urls import path, include
from . import views
from .views import MessageDeleteView, ChatDeleteView, UserProfileView, MessageUpdateView, UserProfileUpdateView, SettingsView, SubscribeView, user_to_do, UserToDoFormView, GetSubscribers, UserToDoDelete, UserToDoUpdateView, PasswordChangeView
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='sign_up'),
    path('user_detail/<int:pk>/', views.UserDetail.as_view(), name='get_users'),
    path('search_users/', views.Search.as_view(), name='get_users'),
    path('profile_photo/', views.UserProfilePhotoCreateView.as_view(), name='photo'),
    path('recommended_users/', views.recommended_users, name='user_with_his_user_regison'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
    path('', views.user_chats, name='user_chats'),
    path('logout/', views.logout_view, name='logout'),
    path('message_delete/<int:pk>/',  MessageDeleteView.as_view(), name='messages_delete'),
    path('delete_chat/<int:pk>/',  ChatDeleteView.as_view(), name='chat_delete'),
    path('user_profile/',  UserProfileView.as_view(), name='user_profiles'),
    path('message/update/<int:pk>/',  MessageUpdateView.as_view(), name='message_update'),
    path('update/',  UserProfileUpdateView.as_view(), name='update_view'),
    path('settings/profile/', SettingsView.as_view(), name='profile_settings'),
    path('follow/user/<int:pk>/', SubscribeView.as_view(), name='follow_to_user'),
    path('my/to/do/', user_to_do, name='to_do'),
    path('my/to/do/uploud/form/', UserToDoFormView.as_view(), name='to_do_form'),
    path('user/followers/<str:username>/', GetSubscribers.as_view(), name='get_followers'),
    path('user/to/do/delete/<int:pk>/', UserToDoDelete.as_view(), name='to_do_delete'),
    path('user/to/do/update/<int:pk>/', UserToDoUpdateView.as_view(), name='todo_update_form'),
    path('user/password/update/', PasswordChangeView.as_view(), name='password_change')



]
