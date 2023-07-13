"""
URL configuration for megano project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from my_auth.views import SignInView, SignUpView, signOut, ProfileApiView, ChangePWDView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sing_in/', SignInView.as_view, name='login'),
    path("sign-up/", SignUpView.as_view(), name="register"),
    path('sign-out/', signOut, name='logout'),
    path("profile/", ProfileApiView.as_view(), name="profile"),
    path("profile/password/", ChangePWDView.as_view(), name="change_pwd"),
    path("", include("frontend.urls"))
]
