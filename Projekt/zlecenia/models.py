from django.db import models
from django.core.exceptions import ValidationError


class Filament(models.Model):
    KOLORY_CHOICES = [
        ('#000000', 'Czarny'),
        ('#FFFFFF', 'Biały'),
        ('#FF0000', 'Czerwony'),
        ('#0000FF', 'Niebieski'),
        ('#00FF00', 'Zielony'),
        ('#FFFF00', 'Żółty'),
        ('#FFA500', 'Pomarańczowy'),
        ('#808080', 'Szary'),
        ('#FFD700', 'Złoty'),
        ('#C0C0C0', 'Srebrny'),
        ('#8B4513', 'Brązowy'),
        ('#FF69B4', 'Różowy'),
    ]

    nazwa = models.CharField(max_length=50)
    kolor = models.CharField(max_length=7, choices=KOLORY_CHOICES, default='#000000')
    cena_za_szpule = models.DecimalField(max_digits=6, decimal_places=2)
    waga_poczatkowa = models.IntegerField(default=1000)
    waga_aktualna = models.IntegerField(default=1000)

    def procent_zuzycia(self):
        if self.waga_poczatkowa > 0:
            return int((self.waga_aktualna / self.waga_poczatkowa) * 100)
        return 0

    def __str__(self):
        return f"{self.nazwa} ({self.get_kolor_display()}) - zostało {self.waga_aktualna}g"


class Zlecenie(models.Model):
    STATUS_CHOICES = [
        ('OCZEKUJACE', 'Oczekujące'),
        ('W_TRAKCIE', 'W trakcie druku'),
        ('ZAKONCZONE', 'Zakończone'),
        ('ANULOWANE', 'Anulowane'),
    ]

    nazwa_detalu = models.CharField(max_length=100)

    filament_glowny = models.ForeignKey(Filament, related_name='zlecenia_glowne', on_delete=models.PROTECT)
    zuzycie_glowny_g = models.IntegerField(verbose_name="Zużycie główne (g)")

    filament_dodatkowy = models.ForeignKey(Filament, related_name='zlecenia_dodatkowe', on_delete=models.SET_NULL,
                                           null=True, blank=True, verbose_name="Filament dodatkowy (opcja)")
    zuzycie_dodatkowy_g = models.IntegerField(default=0, null=True, blank=True, verbose_name="Zużycie dodatkowe (g)")

    czas_druku_minuty = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='OCZEKUJACE')
    koszt_calkowity = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def clean(self):
        if self.pk is None and self.zuzycie_glowny_g > self.filament_glowny.waga_aktualna:
            raise ValidationError(f"Brak materiału! Główny ma tylko: {self.filament_glowny.waga_aktualna}g.")
        if self.filament_dodatkowy and self.zuzycie_dodatkowy_g:
            if self.pk is None and self.zuzycie_dodatkowy_g > self.filament_dodatkowy.waga_aktualna:
                raise ValidationError(f"Brak materiału! Dodatkowy ma tylko: {self.filament_dodatkowy.waga_aktualna}g.")

    def save(self, *args, **kwargs):
        cena_g = float(self.filament_glowny.cena_za_szpule) / self.filament_glowny.waga_poczatkowa
        koszt = self.zuzycie_glowny_g * cena_g

        if self.filament_dodatkowy and self.zuzycie_dodatkowy_g:
            cena_d = float(self.filament_dodatkowy.cena_za_szpule) / self.filament_dodatkowy.waga_poczatkowa
            koszt += self.zuzycie_dodatkowy_g * cena_d

        self.koszt_calkowity = round(koszt, 2)

        if self.pk:
            stary_status = Zlecenie.objects.get(pk=self.pk).status
            if stary_status != 'ZAKONCZONE' and self.status == 'ZAKONCZONE':
                self.filament_glowny.waga_aktualna -= self.zuzycie_glowny_g
                self.filament_glowny.save()

                if self.filament_dodatkowy and self.zuzycie_dodatkowy_g:
                    self.filament_dodatkowy.waga_aktualna -= self.zuzycie_dodatkowy_g
                    self.filament_dodatkowy.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nazwa_detalu} [{self.status}]"