from django.shortcuts import render,redirect
from .forms import RegisterForm,UpdateProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from blogapp.models import Blog
# Create your views here.
def signup(request):
    forms= RegisterForm()
    if request.method == 'POST':
        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request,"Account Created Successfully")
            return redirect ('index')
    context ={"forms":forms}
    return render(request, "core/signup.html",context)


def signin( request):
    if request.method =="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request,email=email,password = password)
        if user is not None:
            login(request,user)
            return redirect("index")
        else:
            messages.warning(request,"Invalid Credentials")
            return redirect("signin")

    context = {}
    return render(request, 'core/login.html',context)


def signout(request):
    logout(request)
    return  redirect('index')

def profile(request):
    user= request.user
    blog = Blog.objects.filter(user = user)

    context={"user": user,"blogs": blog}
    return render(request,'core/profile.html',context)


@login_required(login_url="signin")
def update_profile(request):
    if request.user.is_authenticated:
        user = request.user
        form = UpdateProfileForm(instance=user)
        if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance = user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile created Successfully!")
                return redirect("profile")

    context={"form": form}
    return render(request,'core/update_profile.html',context)