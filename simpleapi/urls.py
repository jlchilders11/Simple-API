'''
URLs for the Simple API project live here
'''
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.urls import include, path

from rest_framework import routers

from .core import views

#Standard Admin URl stuff
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='Login'),
    path('logout/', logout_then_login, name='Logout'),
]

#Our urls for listing, creating, and deleting tokens
urlpatterns += [
    path('tokens/', views.AuthTokenListView.as_view(), name='TokenList'),
    path('tokens/create/', views.AuthTokenCreateView.as_view(), name='TokenCreate'),
    path('tokens/<slug:slug>/delete', views.AuthTokenDeleteView.as_view(), name='TokenDelete'),
]

#Route and include our API urls under /file
router = routers.DefaultRouter()
router.register(r'file', views.FileViewSet)
urlpatterns += [
    path('api/', include(router.urls)),
]
