from django.shortcuts import render

from goods.models import Categories


def index(request):

    context = {
        'title': 'Головна сторінка',
        'content': 'Пивоварня "HOLY"',
    }
    
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Про пивоварню',
        'content': 'Ми Пивоварня "HOLY"',
        'text_on_page': 'Ось чому ми такі класні і афігенні!'
    }
    return render(request, 'main/about.html', context)
