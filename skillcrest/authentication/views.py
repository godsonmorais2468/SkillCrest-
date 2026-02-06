import random
from django.views import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from .models import User, EmailOTP
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'authentication/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🔴 CRITICAL FIX
            user.set_password(form.cleaned_data['password'])

            user.is_active = False
            user.save()

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            EmailOTP.objects.update_or_create(
                email=user.email,
                defaults={'otp': otp}
            )

            request.session['verify-email'] = user.email

            try:
                send_mail(
                    subject="SkillCrest Email Verification",
                    message=f"Your OTP is {otp}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(request, f"Email failed: {e}")
                return redirect('signup')

            messages.success(request, "OTP sent! Check Mailinator inbox.")
            return redirect('verify-otp')

        return render(request, 'authentication/signup.html', {'form': form})




class VerifyOTP(View):
    def get(self, request):
        return render(request, 'authentication/verify-otp.html')

    def post(self, request):
        otp_input = request.POST.get('otp')
        email = request.session.get('verify-email')

        if not email:
            messages.error(request, "Session expired. Please signup again.")
            return redirect('signup')

        try:
            otp_record = EmailOTP.objects.get(email=email, otp=otp_input)
            user = User.objects.get(email=email)
            user.is_active = True
            user.is_email_verified = True
            user.save()
            otp_record.delete()  # remove used OTP

            messages.success(request, "Email verified successfully! You can now login.")
            return redirect('login')

        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'authentication/verify-otp.html')




class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            selected_role = form.cleaned_data.get('role')

            # 🔹 Role verification
            if user.role != selected_role:
                messages.error(request, "Invalid role selected for this account.")
                return redirect('login')

            # 🔹 Email verification check
            if not user.is_email_verified:
                messages.error(request, "Please verify your email before login.")
                return redirect('login')

            login(request, user)

            # 🔹 Role-based redirect (optional but recommended)
            if user.role == 'trainer':
                return redirect('profile')  # later you can change to trainer dashboard
            else:
                return redirect('profile')  # student profile

        return render(request, 'authentication/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'authentication/forgot-password.html')



class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')  # manual auth check

        return render(request, 'authentication/profile.html', {
            'user': request.user
        })