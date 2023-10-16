from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm

# Create your views here.

def sign_in(request):
    if request.method == 'GET':
        #if request.user.is_authenticated:
            #return redirect('login')

        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)

            if user:
                login(request, user)
                return redirect('login')

        return render(request,'user/login.html',{'form': form})

def sign_out(request):
    logout(request)
    return redirect('login')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            return render(request, 'user/register.html', {'form': form})
