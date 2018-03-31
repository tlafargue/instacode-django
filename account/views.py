from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.decorators import login_required

def avantage(request):
    return render(request, 'Avantage_python.html')

def cestquoi(request):
    return render(request, 'quoi.html')

def home(request):
    return render(request, 'instacode.html')

def dashboard(request):
    return render(request, 'account/Dashboard.html')

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'account/Login.html')

def logout_view(request):
    logout(request)
    return render(request, 'instacode.html')


def mention(request):
    return render(request, 'mentions_legales.html')

def nav(request):
    return render(request, 'test.html')

def outils(request):
    return render(request, 'outils.html')

def profile(request,username):
    if (request.user.is_authenticated)==False:
        return redirect('login')

    person = request.user
    context ={'user': person}
    return render(request, 'account/Profile.html',context)

def register_view(request):
    title= "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('account/Loggedin.html')
    return render(request, 'account/registration.html', {"form": form})





