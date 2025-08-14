from django.shortcuts import render


def index(request):
    """this main page"""

    return render(request, 'webapp/index.html')
