import openai
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
from .models import UlepszonyTekst
from .forms import UlepszonyTekstForm
from dotenv import load_dotenv
from .prompts import get_prompt

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
API_KEY = os.getenv('OPENAI_KEY')
openai.api_key = API_KEY


@login_required
def generuj_opis(request):
    ulepszony_tekst = 'test'
    if request.method == 'POST':
        form = UlepszonyTekstForm(request.POST)
        if form.is_valid():
            ton = form.cleaned_data['ton']
            zastosowanie = form.cleaned_data['zastosowanie']
            tekst = form.cleaned_data['tekst']
            system_prompt = get_prompt(zastosowanie)
            # Przykład użycia funkcji ulepsz_opis
            ulepszony_tekst = ulepsz_opis(ton, tekst,system_prompt)

            ulepszony_tekst_model = UlepszonyTekst(
                uzytkownik=request.user,
                ton=ton,
                zastosowanie=zastosowanie,
                tekst=tekst,
                ulepszony_tekst=ulepszony_tekst,
            )
            ulepszony_tekst_model.save()

            return HttpResponse(ulepszony_tekst)
        else:
            return HttpResponse('Błąd formularza', status=400)
    form = UlepszonyTekstForm()

    return render(request, 'index.html',context = {'form': form,'ulepszony': ulepszony_tekst})


def ulepsz_opis(ton, tekst,system_prompt):
    # Wywołanie API OpenAI i przetworzenie tekstu
    prompt = f"Instrukcja dla gpt-3.5: {tekst},zastosuj taki ton wypowiedzi: {ton},"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": system_prompt},
            {"role": "user",
             "content": tekst}
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