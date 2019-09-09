from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home/home.html')

def dashboard(request):
    ctx = {}
    return render(request, 'home/dashboard.html', ctx)