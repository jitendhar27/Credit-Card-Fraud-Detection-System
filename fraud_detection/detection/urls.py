from django.urls import path
from .views import admin_login, verify_otp

urlpatterns = [
    path("admin-login/", admin_login, name="admin_login"),
    path("verify-otp/", verify_otp, name="verify_otp"),
]
