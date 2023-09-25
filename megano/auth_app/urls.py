from django.urls import path
from .views import (
    ProfileApiView,
    ChangePWDView,
    ChangeAvatarView,
    SignInView,
    SignUpView,
    signOut,
)

app_name = "auth_app"

urlpatterns = [
    path("sign-in/", SignInView.as_view(), name="login"),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path("sign-out/", signOut, name="logout"),
    path("profile/", ProfileApiView.as_view(), name="profile"),
    path("profile/password/", ChangePWDView.as_view(), name="change_pwd"),
    path("profile/avatar/", ChangeAvatarView.as_view(), name="change_avatar"),
]
