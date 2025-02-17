from django.contrib.auth.decorators import login_required 
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            
            session_key = request.session.session_key
            if user:
                auth.login(request, user)
                messages.success(request, 'Ви увійшли в систему')
                
                if session_key:
                    Cart.objects.filter(
                        session_key=session_key
                    ).update(user=user)

                # Перевіряємо наявність next у POST-запиті
                next_url = request.POST.get('next')
                if next_url and next_url != reverse('user:logout'):
                    return HttpResponseRedirect(next_url)
                
                # Якщо next відсутній, перенаправляємо на головну
                return HttpResponseRedirect(reverse('main:home'))
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
            session_key = request.session.session_key
            user = form.instance
            auth.login(request, user)
            
            if session_key:
                Cart.objects.filter(
                    session_key=session_key
                ).update(user=user)
                
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
        form = ProfileForm(
            data=request.POST,
            instance=request.user,
            files=request.FILES)
        
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


def users_cart(request):
    return render(request, 'users/users_cart.html')