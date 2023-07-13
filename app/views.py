from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,filters
from app.serializers import *
from app.models import *
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import math,random,requests

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP


def createOtp(number,otp):
    req=  f"https://www.fast2sms.com/dev/bulkV2?authorization=fCekzJi6gcbUSVFm7prx9oKstaTBWOqAdwj421MYPQRGuvXLynmK6PTyAaJdGCc9xXoiq3N8jvF5U2u0&route=otp&variables_values={otp}&flash=0&numbers={number}"
    makeRequest = requests.get(req)
    return makeRequest.json()

# Create your views here.
class SignupView(viewsets.ModelViewSet):
    """Signup new users"""
    serializer_class = SignupSerializer

    def perform_create(self, serializer):
        user = CustomUser.objects.create_user(username=serializer.data['user']['username'],email=serializer.data['user']['email'])
        return Profile.objects.create(user=user,phone=serializer.data['phone'],
                               proffession=serializer.data.get("proffession"),
                               interest= serializer.data.get("interest"),
                               working_time_start=serializer.data.get("working_time_start"),
                               working_time_end= serializer.data.get("working_time_end"))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        genOtp = generateOTP()
        otp = createOtp(request.data['phone'][2:],genOtp)
        if otp['return']:
            user = self.perform_create(serializer)
            Otp.objects.create(otp=genOtp,number=user)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=201, headers=headers)
        else:
            return Response({"success": False, "message": "Please enter valid phone number!"}, status=400)
        

class LoginView(APIView):
    """Login The User Using Auth Token"""
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = Profile.objects.get(phone=request.data["phone"])
                if user:
                    otps = generateOTP()
                    phone = request.data['phone'][2:]
                    otp = createOtp(phone,otps)
                    if otp['return']:
                        Otp.objects.create(otp=otps,number=user)
                        return JsonResponse({"success": True, "message": "Otp Sent Successfully!"}, status=200)
                    else:
                        return JsonResponse({"success": True, "message": "Please Enter Valid number!"}, status=400)
                return Response({"success": False, "message": "Phone number not found!"}, status=400)
            except Exception as e:
                return Response({"success": False, "message": "Phone number not found!"}, status=400)
        return Response(serializer.errors, status=400)
    
    
class OtpView(APIView):
    def post(self,request):
        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                otp = Otp.objects.filter(number__phone = request.data['phone']).order_by("-id")
                if otp[0].otp ==request.data['otp']:
                    user = CustomUser.objects.get(profile__phone= request.data['phone'])
                    token = Token.objects.get_or_create(user=user)
                    Otp.objects.filter(number__phone=request.data['phone']).delete()
                    return JsonResponse({"success": True, "message": token[0].key}, status=200)
                
                return Response({"success": False, "message": "Please Enter Valid Otp"}, status=400)
            except Exception as e:
                return Response({"success": False, "message": "Phone number not found!"}, status=400)
        return Response(serializer.errors, status=400)

    
    
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        partial = kwargs.pop('partial', False)
        instance = Profile.objects.get(user=self.request.user)
        request.data['phone'] = instance.phone
        request.data['user'] = self.request.user.id
        request.data._mutable = False
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

class SearchView(viewsets.ReadOnlyModelViewSet):
    serializer_class = SignupSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id']


    def get_queryset(self):
        username = self.kwargs['username']
        return Profile.objects.select_related('user').filter(Q(user__username__contains=username))
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)