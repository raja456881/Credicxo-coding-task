from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from django.db import transaction
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None,):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError("Users should have a email")
        user=self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.save()
        return user
    def create_student(self, username, email, password=None,):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError("Users should have a email")
        user=self.model(username=username, email=self.normalize_email(email))
        user.is_student=True
        user.set_password(password)
        user.save()
        return user
    def create_admin(self, username, email, password=None,):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError("Users should have a email")
        user=self.model(username=username, email=self.normalize_email(email))
        user.is_admin=True
        user.is_staff=True
        user.set_password(password)
        user.save()
        return user
    def create_teacher(self, username, email, password=None,):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError("Users should have a email")
        user=self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)
        user.is_teacher=True
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not a none')
        user=self.create_user(username, email, password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user





class User(AbstractBaseUser, PermissionsMixin):
    username=models.CharField(max_length=225, unique=True, db_index=True, editable=False)
    email = models.EmailField(db_index=True, unique=True)
    is_active =models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_student=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_teacher=models.BooleanField(default=False)
    groups =models.ManyToManyField(Group,
                             related_name="%(class)ss",
                             related_query_name="%(class)s",
                             blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    @property
    def token(self):
        refresh=RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'acress':str(refresh.access_token)
        }
    def __str__(self):
        return self.email


class Student(User, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





class Teacher(User, PermissionsMixin):


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']




class Admin(User, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']






