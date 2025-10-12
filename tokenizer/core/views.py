from django.shortcuts import redirect, render
from .models import Token


def redir(request):
    return redirect('index')


def index(request):
    # Get the first token by position (lowest number)
    token = Token.objects.first()

    context = {
        'title': 'Tokenizer',
        'token': token,
    }
    return render(request, 'core/index.html', context)


def pageNotFound(request, exception):
    context = {'title': '404'}
    return render(request, 'core/404.html', context)
