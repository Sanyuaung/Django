from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    return HttpResponse('About Page')

def contact(request):
    return HttpResponse('contact Page')

def dashboard(request):
    return HttpResponse('dashboard Page')

# Create your views here.
