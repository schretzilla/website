from django.shortcuts import render

def home(request):
    return render(request, 'portfolio/home.html', context=None)

def self_help(request):
    return render(request, 'portfolio/self-help.html', context=None)

def percent(request):
    return render(request, 'portfolio/percent.html', context=None)

def projects(request):
    return render(request, 'portfolio/projects.html', context=None)

def sacm(request):
    return render(request, 'portfolio/sacm.html', context=None)