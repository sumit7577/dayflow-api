from django.urls import include, path
from rest_framework import routers
from app import views

urlpatterns = [
    path('signup/',views.SignupView.as_view({"post":"create"})),
    path('profile/',views.ProfileView.as_view({'get':"list","put":"update","patch": "partial_update"})),
    path("login/",views.LoginView.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]