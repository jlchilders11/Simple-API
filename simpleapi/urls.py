"""simpleapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import logout_then_login
from django.urls import include, path

from rest_framework import routers 

from .core import views

router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='Login'),
    path('logout/', logout_then_login, name='Logout'),
    path('tokens/', views.AuthTokenListView.as_view(), name='TokenList'),
    path('tokens/create/', views.AuthTokenCreateView.as_view(), name='TokenCreate'),
    path('tokens/<slug:slug>/delete', views.AuthTokenDeleteView.as_view(), name='TokenDelete'),
]
