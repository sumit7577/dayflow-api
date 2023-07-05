from django.urls import include, path, re_path
from rest_framework import routers
from app import views

urlpatterns = [
    path('signup/',views.SignupView.as_view({"post":"create"})),
    path('profile/',views.ProfileView.as_view({'get':"list"})),
    path('profile/<pk>/',views.ProfileView.as_view({"put":"update","patch":"partial_update"})),
    path("login/",views.LoginView.as_view()),
    path("validate/",views.OtpView.as_view()),
    re_path('^search/(?P<username>.+)/$', views.SearchView.as_view({'get':"list"})),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]