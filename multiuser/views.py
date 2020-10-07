from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from.models import Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from.models import User
from django.contrib.auth.models import Group
from .searilizers import StudentRegistrationSerializer,\
    Restpasswordsearilizers, AdminRegistrationSerializer,\
    TeachesRegistrationSerializer, UserLoginSerializer,setnewpasswordsearilizers,studentdetailserializers,adminviewsearilizers
from django.utils.encoding import smart_bytes,smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import utils
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
class StudentRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = StudentRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AdminRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AdminRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TeachesRegistration(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TeachesRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Resetpasswordview(GenericAPIView):
    serializer_class = Restpasswordsearilizers

    def post(self, request):

        seralizers=self.serializer_class(data=request.data)
        email=request.data['email']
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            current=get_current_site(request).domain
            realtivelinj = reverse('password-rest-confirm', kwargs={'uidb64':uidb64, 'token':token})
            url = 'http://' + current + realtivelinj
            body='Hello \n Use link below toreset your password \n'+url
            data={"email_body":body, 'to_email':user.email  ,'subject':'Reset for password'}
            utils.send_mail(data)

        return Response({'success':'We have send you a link  to rest you password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckApi(GenericAPIView):
    def get(self, request,uidb64,token):
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)

            if not  PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not vaild, please request a new one'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'success':True, 'messages':'Credentails Valid','uidb64':uidb64, 'token':token}, status=status.HTTP_201_CREATED)

        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator():
                return Response({'error':'Token is not vaild, please request a new one'}, status=status.HTTP_406_NOT_ACCEPTABLE)




class setnewpassword(GenericAPIView):
    serializer_class = setnewpasswordsearilizers
    def patch(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, "messages":"Password reset success"},status=status.HTTP_200_OK)

class teacherview(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Student.objects.all()
    serializer_class = studentdetailserializers


class Adminview(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.all()
    serializer_class = adminviewsearilizers




def studenview(request):
    if User.is_authenticated and User.is_student:
        user=User.objects.get(username=request.user.username)
        data={
            "name":user.username,
            "email":user.email,
            'id':user.id
        }
    return JsonResponse({'data':data})







