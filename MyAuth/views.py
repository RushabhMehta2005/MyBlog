from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def home(request):
    return render(request, "MyAuth/home.html", {})


def login_user(request):
    if request.method == "GET":
        form = AuthenticationForm()
        return render(
            request,
            "MyAuth/login.html",
            {
                "form": form,
            },
        )
    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username, password = form.cleaned_data.get(
                "username"
            ), form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged In!")
                return redirect(reverse("MyAuth:home"))
            else:
                messages.error(request, "Invalid Username or Password.")
                return redirect(reverse("MyAuth:login_user"))
        else:
            messages.error(request, "Invalid Form Fields.")
            return redirect(reverse("MyAuth:login_user"))


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect(reverse("MyAuth:home"))


def register_user(request):
    if request.method == "GET":
        form = UserCreationForm()
        return render(
            request,
            "MyAuth/register.html",
            {
                "form": form,
            },
        )
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username, password = form.cleaned_data.get(
                "username"
            ), form.cleaned_data.get("password1")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registered!")
            return redirect(reverse("MyAuth:home"))
        else:
            messages.error(request, "Invalid Username or Password.")
            return redirect(reverse("MyAuth:register_user"))
