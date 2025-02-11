from django.contrib.auth.decorators import login_required 
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from traitlets import Instance
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm



def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, 'Ви увійшли в систему')
                return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = UserLoginForm()
    context = {
        'title': 'Логін',
        'form': form
    }
    
    return render(request, 'users/login.html', context)



def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ви зареєструвались')
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserRegistrationForm()
    
    context = {
        'title': 'Реєстрація',
        'content': 'Реєстрація',
        'form': form
    }
    return render(request, 'users/registration.html', context)




@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)   
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено')
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'title': 'Профіль',
        'form': form
    }
    return render(request, 'users/profile.html', context)




@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Ви вийшли з системи')
    return redirect(reverse('main:home'))