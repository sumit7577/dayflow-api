from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from app.serializers import *
from app.models import *
from datetime import date, datetime
from rest_framework import mixins
from rest_framework.authtoken.models import Token


# Create your views here.
class SignupView(viewsets.ModelViewSet):
    """Signup new users"""
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(username=serializer.data['user']['username'],email=serializer.data['user']['email'])
        Profile.objects.create(user=user,phone=serializer.data['phone'],
                               proffession=serializer.data.get("proffession"),
                               interest= serializer.data.get("interest"),
                               working_time_start=serializer.data.get("working_time_start"),
                               working_time_end= serializer.data.get("working_time_end"))

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request,*args,**kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

class LoginView(APIView):
    """Login The User Using Auth Token"""
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(profile__phone=request.data["phone"])
                if user:
                    token = Token.objects.get_or_create(user=user)
                    return JsonResponse({"success": True, "message": token[0].key}, status=200)
                return Response({"success": False, "message": "Phone number not found!"}, status=400)
            except Exception as e:
                return Response({"success": False, "message": "Phone number not found!"}, status=400)
        return Response(serializer.errors, status=400)
    
    
class ProfileView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SignupSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
