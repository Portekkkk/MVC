# 3D Print Manager PRO
**Autor:** Dawid Portuś
**Numer indeksu:** 61767

## Spis treści
1. [Przeznaczenie systemu](#przeznaczenie-systemu)
2. [Specyfikacja modułów](#specyfikacja-modułów)
3. [Architektura MVC / MVT](#architektura-mvc--mvt)
4. [Zależności zewnętrzne](#zależności-zewnętrzne)
5. [Instrukcja wdrożenia](#instrukcja-wdrożenia)
6. [Środowisko testowe](#środowisko-testowe)

---

## Przeznaczenie systemu
3D Print Manager PRO to aplikacja webowa przeznaczona do zarządzania kolejką zadań dla farm drukarek 3D oraz monitorowania stanów magazynowych materiałów eksploatacyjnych. System automatyzuje proces wyceny detali, wspierając zaawansowane wydruki wielokolorowe.

## Specyfikacja modułów
* **Moduł Magazynu:** Ewidencja szpul filamentów z parametrami: waga początkowa, waga aktualna, cena zakupu oraz predefiniowany kolor (obsługa kodowania HEX).
* **Silnik Kalkulacyjny:** Automatyczne obliczanie kosztów produkcji na podstawie deklarowanego zużycia materiału. Logika uwzględnia zmienne ceny różnych materiałów i potrafi sumować koszty dla wydruków z wstawkami (dwukolorowych).
* **Automatyzacja Stanów:** Zintegrowany mechanizm aktualizacji – zmiana statusu zlecenia na "Zakończone" wyzwala przeliczenie i redukcję wagi przypisanych szpul w bazie danych.
* **Dashboard Operacyjny:** Interfejs prezentujący kluczowe metryki systemu w czasie rzeczywistym, wykorzystujący wskaźniki postępu z gradientem ostrzegawczym dla kończących się materiałów.
* **Moduł Administracyjny:** Pełen dostęp do operacji CRUD z poziomu wbudowanego panelu zarządzania, z zabezpieczoną autoryzacją.

## Architektura MVC / MVT
Projekt opiera się na architekturze MVT (Model-View-Template) frameworka Django, będącej bezpośrednią realizacją klasycznego wzorca projektowego MVC (Model-View-Controller):
* **Model (`models.py`):** Definiuje schemat bazy danych (relacyjne tabele `Filament` i `Zlecenie`) oraz hermetyzuje logikę biznesową, w tym walidację dostępności materiałów i kalkulację kosztów.
* **View / Szablon (`dashboard.html`):** Warstwa prezentacji odpowiedzialna za renderowanie interfejsu użytkownika w przeglądarce.
* **Controller / Widok Django (`views.py`):** Moduł sterujący strumieniem danych – agreguje informacje z bazy i przekazuje je do warstwy prezentacji.

## Zależności zewnętrzne
Interfejs użytkownika wykorzystuje następujące biblioteki zewnętrzne:
1. **Chart.js** – renderowanie responsywnego wykresu (Doughnut Chart) na podstawie danych przekazywanych z backendu, prezentującego aktualny rozkład statusów na produkcji.
2. **Bootstrap 5 & Bootstrap Icons** – framework CSS zapewniający responsywność siatki (Grid), standaryzację komponentów interfejsu (tabele, odznaki, wskaźniki postępu) oraz ikonografię.

## Instrukcja wdrożenia
Aplikacja jest gotowa do uruchomienia w środowisku deweloperskim. Aby zainicjować projekt lokalnie, należy wykonać następujące polecenia w terminalu:

1. Pobranie repozytorium:
   `git clone https://github.com/Portekkkk/MVC/tree/de5f3dc72acd38f25e0da39dfa9d80b3b3ec59a1/Projekt`
2. Instalacja środowiska:
   `pip install django`
3. Inicjalizacja konta administratora (wymagane do zarządzania rekordami):
   `python manage.py createsuperuser`
4. Uruchomienie serwera aplikacji:
   `python manage.py runserver`
5. Dostęp: 
   * Aplikacja główna: `http://127.0.0.1:8000/`
   * Panel administracyjny: `http://127.0.0.1:8000/admin`

## Środowisko testowe
W repozytorium znajduje się plik bazy danych `db.sqlite3` zawierający zbiór danych testowych. Zostały one przygotowane w celu natychmiastowej weryfikacji logiki biznesowej:
* **Weryfikacja magazynu:** Przypisano szpule o krytycznym poziomie materiału, co demonstruje responsywność interfejsu (zmiana barw wskaźników na żółty/czerwony).
* **Weryfikacja kalkulacji:** W kolejce znajdują się zlecenia wielokolorowe, udowadniające poprawność wyliczania i sumowania kosztów z różnych źródeł materiałowych.
* **Weryfikacja wykresów:** Rozkład różnych statusów zleceń pozwala na ewaluację poprawnego działania skryptów Chart.js.
