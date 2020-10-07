from rest_framework import serializers
from .models import Student, Teaches, Admin
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes,smart_str, force_str,smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from.models import User
from django.contrib.auth.models import Group
from rest_framework.exceptions import AuthenticationFailed
class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    username=serializers.CharField(max_length=34)
    token = serializers.CharField(max_length=255, read_only=True)
    groups=serializers.CharField(max_length=33, read_only=True)
    class Meta:
        model = Student
        fields =  ['email', 'username', 'password', 'token','groups']
    def create(self, validated_data):
        user=Student.objects.create_user(**validated_data)
        group=Group.objects.get(name="Student")
        user.groups.add(group)
        return user

class TeachesRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    groups=serializers.CharField(max_length=33, read_only=True)
    class Meta:
        model = Teaches
        fields =  ['email', 'username', 'password', 'token', 'groups']

    def create(self, validated_data):
        user= Teaches.objects.create_user(**validated_data)
        group=Group.objects.get(name="Teaches")
        user.groups.add(group)
        return user

class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    username=serializers.CharField(max_length=34)
    token = serializers.CharField(max_length=255, read_only=True)
    groups=serializers.CharField(max_length=33, read_only=True)

    class Meta:
        model = Admin
        fields = ['email', 'username', 'password', 'token', 'groups']


    def create(self, validated_data):
        user=Admin.objects.create_user(**validated_data)
        group=Group.objects.get(name="Admin")
        user.groups.add(group)
        return user





class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            userObj = Student.objects.get(email=user.email)
        except Student.DoesNotExist:
            userObj = None

        try:
            if userObj is None:
                userObj = Teaches.objects.get(email=user.email)
        except Teaches.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        try:
            if userObj is None:
                userObj = Admin.objects.get(email=user.email)
        except Admin.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )


        return {
            'email': user.email,
            'token': user.token
        }


class Restpasswordsearilizers(serializers.Serializer):
    email=serializers.EmailField(max_length=34)

    class Meta:
        fields=['email']




class setnewpasswordsearilizers(serializers.Serializer):
    password=serializers.CharField(min_length=6, max_length=68, write_only=True)
    token=serializers.CharField(min_length=1, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password=attrs.get('password', '')
            token=attrs.get('token', '')
            uidb64=attrs.get('uidb64', '')
            id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invaild', 401)
            user.set_password(password)
            user.save()
            return user
        except  Exception as e:
            AuthenticationFailed('The reset link is invaild', 401)
        return super().validate(attrs)


