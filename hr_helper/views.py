import openai
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
from collections import defaultdict
from .models import UlepszonyTekst
from .forms import UlepszonyTekstForm
from dotenv import load_dotenv
from .prompts import get_prompt
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objs as go
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from collections import namedtuple, Counter


load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
API_KEY = os.getenv('OPENAI_KEY')
openai.api_key = API_KEY


@login_required
def generuj_opis(request):
    ulepszony_tekst = 'test'
    if request.method == 'POST':
        form = UlepszonyTekstForm(request.POST,initial=request.POST)
        if form.is_valid():
            ton = form.cleaned_data['ton']
            zastosowanie = form.cleaned_data['zastosowanie']
            tekst = form.cleaned_data['tekst']
            system_prompt = get_prompt(zastosowanie)
            # Przykład użycia funkcji ulepsz_opis
            ulepszony_tekst,tokens = ulepsz_opis(ton, tekst,system_prompt)
            liczba_slow = len(ulepszony_tekst.split())

            ulepszony_tekst_model = UlepszonyTekst(
                uzytkownik=request.user,
                ton=ton,
                zastosowanie=zastosowanie,
                tekst=tekst,
                ulepszony_tekst=ulepszony_tekst,
                tokens=tokens,
                liczba_slow=liczba_slow,
                created_at=timezone.now(),
            )
            ulepszony_tekst_model.save()

            # Przekształć obiekt modelu na słownik i następnie na JSON
            ulepszony_tekst_dict = model_to_dict(ulepszony_tekst_model)
            return JsonResponse(ulepszony_tekst_dict)
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
    tokens = response['usage']['total_tokens']
    return opis,tokens


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

@login_required
@csrf_exempt
def toggle_ulubiony(request, pk):
    if request.method == 'POST':
        tekst = UlepszonyTekst.objects.get(pk=pk)
        tekst.ulubiony = not tekst.ulubiony
        tekst.save()
        return HttpResponse('success')
    else:
        return HttpResponse('error', status=400)


@csrf_exempt
@login_required
def aktualizuj_opis(request, pk):
    if request.method == 'POST':
        try:
            ulepszony_tekst = UlepszonyTekst.objects.get(pk=pk, uzytkownik=request.user)
            ulepszony_tekst.ulepszony_tekst = request.POST['ulepszony_tekst']
            ulepszony_tekst.save()
            return JsonResponse({'status': 'success'})
        except UlepszonyTekst.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    else:
        return JsonResponse({'status': 'error'}, status=405)


def profil(request):
    # Pobierz dane z ostatnich 30 dni
    data_od = timezone.now() - timedelta(days=30)
    data_do = timezone.now()
    teksty_uzytkownika = UlepszonyTekst.objects.filter(uzytkownik=request.user, created_at__range=(data_od, data_do))

    # Grupuj dane według dnia i oblicz sumę słów dla każdego dnia
    grouped_data = teksty_uzytkownika.annotate(day=TruncDate('created_at')).values('day').annotate(sum_words=Sum('liczba_slow')).order_by('day')

    # Inicjuj dane dla każdego z ostatnich 30 dni z zerową liczbą słów
    daily_data = defaultdict(int)
    for i in range(30):
        day = (timezone.now() - timedelta(days=i)).date()
        daily_data[day] = 0

    # Aktualizuj dane z bazy danych
    for record in grouped_data:
        daily_data[record['day']] = record['sum_words']

    # Przygotuj dane do wykresu
    data = go.Bar(
        x=list(daily_data.keys()),
        y=list(daily_data.values()),
        text=[f"Zużycie: {v}" for v in daily_data.values()],
        hovertemplate="%{text}<br>%{x}",
        name=""
    )

    layout = go.Layout(title="Zużycie słów przez użytkownika w ostatnich 30 dniach",
                       xaxis=dict(title="Data"), yaxis=dict(title=""))
    fig = go.Figure(data=[data], layout=layout)

    div = plot(fig, output_type='div', include_plotlyjs=False)

    #Statystyki użycia zastosowań
    Usage = namedtuple('Usage', ['name', 'count'])
    zastosowania = UlepszonyTekst.objects.values_list('zastosowanie', flat=True)
    zastosowania_count = Counter(zastosowania)
    usages = []

    for choice, choice_name in UlepszonyTekst._meta.get_field('zastosowanie').choices:
        usages.append(Usage(name=choice_name, count=zastosowania_count.get(choice, 0)))

    # Posortuj listę usages od największej wartości do najmniejszej
    usages = sorted(usages, key=lambda x: x.count, reverse=True)


    #Obliczanie zaoszczędzonych zasobów
    user = request.user
    liczba_slow = UlepszonyTekst.objects.filter(uzytkownik=user).aggregate(Sum('liczba_slow'))['liczba_slow__sum'] or 0

    zaoszczedzony_czas = (liczba_slow / 1000) * 60
    zaoszczedzone_pieniadze = zaoszczedzony_czas * 20

    return render(request, 'profil.html', {'wykres': div,'usages': usages,'zaoszczedzony_czas': zaoszczedzony_czas,
    'zaoszczedzone_pieniadze': zaoszczedzone_pieniadze})