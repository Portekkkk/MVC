from django.shortcuts import render
from .models import Zlecenie, Filament


def dashboard(request):
    zlecenia = Zlecenie.objects.all()
    filamenty = Filament.objects.all()

    oczekujace = zlecenia.filter(status='OCZEKUJACE').count()
    w_trakcie = zlecenia.filter(status='W_TRAKCIE').count()
    zakonczone = zlecenia.filter(status='ZAKONCZONE').count()

    context = {
        'zlecenia': zlecenia,
        'filamenty': filamenty,
        'dane_wykresu': [oczekujace, w_trakcie, zakonczone]
    }

    return render(request, 'zlecenia/dashboard.html', context)