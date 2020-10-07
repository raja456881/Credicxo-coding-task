
from django.urls import path
from.import views

urlpatterns = [
    path('adminregister', views.AdminRegistration.as_view(), name='adminregister'),
    path('studentregister', views.StudentRegistration.as_view(), name='studentregister'),
    path('teachesregister', views.TeachesRegistration.as_view(),name='teachesregister'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('restpassword', views.Resetpasswordview.as_view()),
    path('password-rest/<uidb64>/<token>/', views.PasswordTokenCheckApi.as_view(), name='password-rest-confirm'),
    path('password-reset-complete', views.setnewpassword.as_view(), name='password-reset-complete'),
    path('teacherview', views.teacherview.as_view(), name="teacherview"),
    path("adminview", views.Adminview.as_view(), name='adminview'),
    path("studentview", views.studenview, name='studentview')
]