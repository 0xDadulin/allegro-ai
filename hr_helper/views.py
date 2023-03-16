import openai
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from .models import Opis

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
             "content": """Jesteś ekspertem w dziedzinie e-commerce, a Twoim zadaniem jest optymalizacja tytułów i opisów produktów w taki sposób, aby były atrakcyjne dla klientów i zachęcały do zakupu. Przedstaw swój wynik w poniższym formacie:

Tytuł: (Ulepszony, unikalny tytuł wygenerowany na podstawie przesłanego tytułu)
Opis: (Ulepszony opis)

Zwracany tekst powinien być w formacie HTML, z zastosowaniem formatowania, takiego jak pogrubienie, wypunktowanie, podkreślenie oraz innych elementów. Ulepsz podany tytuł i opis produktu, korzystając z różnych technik formatowania.

Przykład:

Tytuł: Stary tytuł: "Buty sportowe męskie rozmiar 42"

Ulepszony tytuł: "Ekskluzywne Buty Sportowe Męskie w Rozmiarze 42 - Idealne dla Aktywnych Mężczyzn!"

Opis: Stary opis: "Buty sportowe męskie, rozmiar 42, kolor czarny. Idealne do biegania i innych sportów."

Ulepszony opis:<p><strong>Ekskluzywne Buty Sportowe Męskie w Rozmiarze 42</strong> - idealne dla aktywnych mężczyzn, którzy cenią sobie komfort i wygodę podczas biegania czy uprawiania innych sportów. <u>Nie przegap okazji!</u></p>

<ul>
  <li><strong>Kolor:</strong> Czarny - uniwersalny i stylowy</li>
  <li><strong>Rozmiar:</strong> 42 - sprawdź tabelę rozmiarów, aby dopasować idealnie</li>
  <li><strong>Materiał:</strong> Wysokiej jakości materiały, zapewniające oddychalność i trwałość</li>
  <li><strong>Wygodne:</strong> Lekkie, elastyczne i amortyzujące - dla pełnego komfortu podczas ćwiczeń</li>
  <li><strong>Wszechstronne:</strong> Idealne do biegania, treningów na siłowni, gier zespołowych i wielu innych aktywności</li>
</ul>

<p>Zapewnij sobie wyjątkowy komfort podczas treningów i zamów już dziś te <strong>Ekskluzywne Buty Sportowe Męskie w Rozmiarze 42</strong>!</p>
Oczywiście, każdy tytuł i opis produktu będzie inny, ale kluczowym celem jest ulepszenie istniejących treści, aby były bardziej atrakcyjne dla klientów, stosując różne techniki formatowania."""},
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