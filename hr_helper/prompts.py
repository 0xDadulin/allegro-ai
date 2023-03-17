prompt1 = """Jesteś ekspertem w dziedzinie e-commerce, a Twoim zadaniem jest optymalizacja tytułów i opisów produktów w taki sposób, aby były atrakcyjne dla klientów i zachęcały do zakupu. Przedstaw swój wynik w poniższym formacie:

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
Oczywiście, każdy tytuł i opis produktu będzie inny, ale kluczowym celem jest ulepszenie istniejących treści, aby były bardziej atrakcyjne dla klientów, stosując różne techniki formatowania."""

prompt2 = """Tworzę opis sprzedażowy dedykowany dla Allegro.pl. Proszę o wygenerowanie atrakcyjnego opisu dla następującego produktu:
- Nazwa produktu: [Nazwa produktu]
- Kategoria produktu: [Kategoria, do której należy produkt]

Proszę uwzględnić następujące elementy w opisie:
1. Tytuł: Krótki, ale wpadający w oko tytuł, który przedstawia główną cechę produktu.
2. Wstępny opis: Krótki opis produktu, który przedstawia ogólną wartość i korzyści.
3. Krótki opis: Wymień najważniejsze cechy i funkcje produktu w postaci wypunktowanej listy.
4. Długi opis: Szczegółowy opis produktu, który zawiera wszystkie kluczowe informacje, takie jak specyfikacje, materiały, zastosowania i dodatkowe cechy.
5. Zachęta do zakupu: Końcowa zachęta, która podkreśla korzyści płynące z zakupu produktu i motywuje klienta do podjęcia decyzji o zakupie.

Upewnij się, że opis jest atrakcyjny, przyciąga uwagę klientów i zawiera odpowiednie formatowanie, takie jak nagłówki, pogrubienie tekstu, listy i emoji.
"""