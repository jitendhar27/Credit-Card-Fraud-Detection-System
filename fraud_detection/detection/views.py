import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.conf import settings
from .models import AdminUser

# Generate and send OTP
def send_otp(email):
    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
    user = AdminUser.objects.get(email=email)
    user.otp = otp
    user.otp_created_at = now()  # Store OTP creation time
    user.save()

    # Send OTP via email
    send_mail(
        "Your OTP Code",
        f"Your OTP code is {otp}. It is valid for 5 minutes.",
        settings.EMAIL_HOST_USER,  # FIXED: Use email from settings
        [email],
        fail_silently=False,
    )

# Admin login
def admin_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        if user is not None:
            send_otp(email)
            request.session["email"] = email
            return redirect("verify_otp")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")

# OTP verification
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        email = request.session.get("email")

        try:
            user = AdminUser.objects.get(email=email)
        except AdminUser.DoesNotExist:
            return render(request, "verify_otp.html", {"error": "Invalid email"})

        # Check OTP expiration (5-minute validity)
        otp_age = now() - user.otp_created_at
        if otp_age > timedelta(minutes=5):
            return render(request, "verify_otp.html", {"error": "OTP has expired. Request a new one."})

        if user.otp == otp:
            login(request, user)  # Lo
