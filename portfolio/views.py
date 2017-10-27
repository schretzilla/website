from django.shortcuts import render

#Resume dependencies
from django.conf import settings
from django.http import HttpResponse


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

def resume(request):
    filePath = settings.BASE_DIR + '/portfolio/static/portfolio/docs/Fall_17.pdf'
    with open(filePath, 'r') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed
    #return render(request, 'portfolio/resume.html', context=None)
    