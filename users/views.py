from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm, SignupForm
from .models import UserProfile


def user_profile(request):
    template = "registration/user_profile.html"
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    context = {"profile": profile}
    return render(request, template, context)

def login_user(request):
    template = "registration/login.html"
    form = UserForm()
    context = {"form": form}
    return render(request, template, context)

def _logout(request):
    logout(request)
    return redirect("login_user")

def _login(request):
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            next_url = request.POST.get("next") or "home"

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect("home")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect(next_url)

def signup(request):
    template = "registration/signup.html"
    form = SignupForm()
    context = {"form": form}
    return render(request, template, context)

def signup_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error in the signup form")
    else:
        form = SignupForm()

    template = "registration/signup.html"
    context = {"form": form}
    return render(request, template, context)

def login_api(request):
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = {"STATUS": "OK", "USER_ID": user.pk}
                    return JsonResponse(response, content_type="application/json", safe=False)
                else:
                    response = {"STATUS": "INACTIVE"}
                    return JsonResponse(response, content_type="application/json", safe=False)
            else:
                response = {"STATUS": "INVALID USER CREDENTIALS", "CODE": -1}
                return JsonResponse(response, content_type="application/json", safe=False)
        else:
            response = {"STATUS": "VALIDATION ERROR"}
            return JsonResponse(response, content_type="application/json", safe=False)

def signup_api(request):
    if request.method == "POST":
        form = SignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            response = {"STATUS": "OK", "CODE": 0}
            return JsonResponse(response, content_type="application/json", safe=False)
        else:
            response = {"STATUS": "ERROR", "CODE": -1}
            return JsonResponse(response, content_type="application/json", safe=False)




