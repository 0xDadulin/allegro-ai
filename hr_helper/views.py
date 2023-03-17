import openai
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from .models import Opis

from .prompts import prompt2
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
API_KEY = os.getenv('OPENAI_KEY')
openai.api_key = API_KEY

@login_required
def generuj_opis(request):
    ulepszony_opis = ''
    title = request.POST.get('title')
    ton = request.POST.get('ton')
    dlugosc = request.POST.get('dlugosc')
    tekst = request.POST.get('tekst')
    settings = [title,ton,dlugosc,tekst]
    if tekst != None:
        print(f'tekst{tekst}')
        ulepszony_opis = ulepsz_opis(ton, dlugosc, tekst, title)
        opis_model = Opis(user=request.user, title=title, text=ulepszony_opis)
        opis_model.save()
        return HttpResponse(ulepszony_opis)
    return render(request, 'index.html', {'opis': ulepszony_opis})

def ulepsz_opis(ton, dlugosc, tekst,title):
    # Wywołanie API OpenAI i przetworzenie tekstu
    prompt = f"Ton opisu:{ton},długość:{dlugosc},opis produktu: {tekst}, tytuł:{title}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": prompt2},
            {"role": "user",
             "content": prompt}
        ]
    )
    opis = response['choices'][0]['message']['content']
    return opis


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('generuj-opis')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('generuj-opis')
    else:
        print('błąd')
        return HttpResponse(status=405)