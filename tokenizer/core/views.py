from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Token
from datetime import date
from django.http import JsonResponse


def redir(request):
    return redirect('index')


def index(request):
    # Get the first token by position (lowest number)
    token = Token.objects.first()

    if request.method == "POST":
        action = request.POST.get("action")
        updated = False
        if action == "plus":
            try:
                token.number = str(int(token.number) + 1).zfill(3)
                updated = True
            except ValueError:
                pass
        elif action == "minus":
            try:
                token.number = str(int(token.number) - 1).zfill(3)
                updated = True
            except ValueError:
                pass
        elif action == "set":
            new_value = request.POST.get("value")
            if new_value is not None:
                token.number = new_value
                updated = True
        if updated:
            token.date = date.today()
            token.save()
        return redirect("index")

    context = {
        'title': 'Tokenizer',
        'token': token,
    }
    return render(request, 'core/index.html', context)


def pageNotFound(request, exception):
    context = {'title': '404'}
    return render(request, 'core/404.html', context)

# --------------------------------------------------

@csrf_protect
def login(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                return render(request, 'core/login.html', {'error': True})
    return render(request, 'core/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')


def token_data(request):
    token = Token.objects.first()
    return JsonResponse({
        'number': token.number,
        'title': token.title,
        'description': token.description,
        # 'date': token.date.strftime('%d.%m.%Y'),
        'date': token.date.strftime('%b. %d, %Y'),
    })

def add_token(request):
    token = Token.objects.first()
    token.number = str(int(token.number) + 1).zfill(3)
    token.date = date.today()
    token.save()

    return JsonResponse({'success': True})