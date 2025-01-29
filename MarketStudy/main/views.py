from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': 'Головна сторінка',
        'content': 'Пивоварня "###"'
    }
    return render(request,'main/index.html', context)

def about(request):
    context = {
        'title': 'Про пивоварню',
        'content': 'Ми Пивоварня "###"',
        'text_on_page': 'Ось чому ми такі класні і афігенні!'
    }
    return render(request,'main/about.html', context)

