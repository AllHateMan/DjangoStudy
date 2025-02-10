from django.shortcuts import render

# Create your views here.
def login(request):

    context = {
        'title': 'Головна сторінка',
        'content': 'Пивоварня "HOLY"',
    }
    
    return render(request, 'users/login.html', context)

def registration(request):
    context = {
        'title': 'Реєстрація',
        'content': 'Реєстрація',
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': 'Профіль',
        'content': 'Профіль',
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    pass