from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # Import User model from Django's auth module
from blogapp.models import Blog
from userapp.models import FriendRequest
from django.contrib import messages



def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Basic validation
        if not firstname or not lastname or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        # Check if email already exists (since you use email as username)
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")

        # Create user
        user = User.objects.create_user(
            username=email,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully.")
        return redirect("login")

    return render(request, "registers.html")


def home(request):
    blogs = Blog.objects.all()
    
    # Attach 'is_saved' attribute for each blog
    # for blog in blogs:
        # blog.is_saved = request.user.is_authenticated and blog.saved_by.filter(id=request.user.id).exists()
    return render(request, "home.html", {"blogs": blogs})


def loginview(request):
    if request.user.is_authenticated:   
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")  # Redirect to home after successful login
        else:
            messages.error(request,"invalid email or password. ")
            return redirect("login")  # Fix redirect loop issue

    return render(request, "login.html")


@login_required(login_url="login")  # Redirect to login page if not authenticated
def logoutview(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout


def Settings(request):
    if request.user.is_authenticated:
        return render(request, "settings.html")
    return redirect("login")


def lang(request):
    return render(request, "lang.html")

def helSupport(request):
    return render(request, "helpsupport.html")

def hh(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "h.html")    

def Livechat(request):
    return render(request, "vc.html")


def podcs(request):
    return render(request,"podcats.html")

def dashboard(request):
        return render(request, "das.html")
    
def ss(request):
    pass    



    
    
           