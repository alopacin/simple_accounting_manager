# zainicjowanie klasy menager
class Manager:
    def __init__(self):
        self.warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.stan_magazynu = dict()
        self.historia_akcji = []
        self.akcja = 0
        self.stan_konta = 1000
        self.filename = 'history.txt'
        self._load_data()

# funkcja odpowiadajaca za odczyt danych z pliku tekstowego i przypisywanie wartosci do zmiennych
    def _load_data(self):
        with open(self.filename, 'r') as f:
            for line in f:
                if 'Stan konta' in line:
                    account, money = line.strip().split('&&')
                    self.stan_konta = float(money)
                elif '%%' in line:
                    k, v = line.strip().split('%%')
                    self.stan_magazynu[k] = v
                elif '&&' in line:
                    line = line.strip().replace('&&', '')
                    self.historia_akcji.append(line)

    def assign(self, inquiry):
        if inquiry in self.warunki :
            return self.execute(inquiry)
        else:
            return 'Wpisałeś nieprawidłową wartość.Spróbuj jeszcze raz!'

    def execute(self, zapytanie):
        # jezeli podanej wartosci nie ma na liscie warunkow program pyta uzytkownika jeszcze raz co chce zrobic
            if zapytanie not in self.warunki :
                print('Wpisałeś nieprawidłową wartość.Spróbuj jeszcze raz!')

        # dodanie i odjecie przez uzytkownika kwoty z konta
            elif zapytanie == 'saldo':
                while True :
                    zapytanie_o_saldo = int(input('Wybierz 1 jeżeli chcesz dodać kwotę. Wybierz 2 jeżeli chcesz odjąć kwotę: '))
                    if zapytanie_o_saldo == 1 :
                        saldo = float(input('Wpisz kwotę: '))
                        self.stan_konta += saldo
                        print(f'Dodano {saldo} $ do konta')
                        akcja = f'Dodano {saldo} $ do konta'
                        self.historia_akcji.append(akcja)
                        break
                    elif zapytanie_o_saldo == 2 :
                        saldo = int(input('Wpisz kwotę: '))
                        self.stan_konta -= saldo
                        print(f'Odjęto {saldo} $ z konta')
                        akcja = f'Odjęto {saldo} $ z konta'
                        self.historia_akcji.append(akcja)
                        break
                    else :
                        print('Podano nieprawidłową liczbę')

        # sprzedaz, ktora dodaje kwote wpisana przez uzytkownika do salda i odejmuje dane produkty z magazynu
            elif zapytanie == 'sprzedaz' :
                nazwa_produktu = input('Podaj jaki produkt ma zostać sprzedany: ')
                if nazwa_produktu not in self.stan_magazynu:
                    print('Nie ma takiego produktu w magazynie!')
                else:
                    cena_produktu = float(input('Podaj cenę: '))
                    liczba_sztuk = int(input('Podaj ilość: '))
                    laczna_cena = cena_produktu * liczba_sztuk
                    produkt_do_sprzedazy = self.stan_magazynu[nazwa_produktu]['ilość']
                    if produkt_do_sprzedazy < liczba_sztuk:
                        print('Nie ma takiej ilości!')
                    else:
                        produkt_do_sprzedazy -= liczba_sztuk
                        self.stan_konta += laczna_cena
                        self.stan_magazynu[nazwa_produktu]['ilość'] -= liczba_sztuk
                        print(f'Sprzedano {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $')
                        akcja = f'Sprzedano {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $'
                        self.historia_akcji.append(akcja)

        # zakup, ktory odejmuje kwote z konta i dodaje produkty do magazynu
            elif zapytanie == 'zakup' :
                nazwa_produktu = input('Podaj jaki produkt ma zostać zakupiony: ')
                if nazwa_produktu not in self.stan_magazynu:
                    cena_produktu = float(input('Podaj cenę produktu: '))
                    liczba_sztuk = int(input('Podaj liczbę zakupionych sztuk: '))
                    laczna_cena = cena_produktu * liczba_sztuk
                    if laczna_cena > self.stan_konta :
                        print('Brakuje pieniędzy na zakup')
                    elif laczna_cena < self.stan_konta:
                        self.stan_magazynu[nazwa_produktu] = {'ilość': liczba_sztuk, 'cena': cena_produktu}
                        self.stan_konta -= laczna_cena
                        print(f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $')
                        akcja = f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $'
                        self.historia_akcji.append(akcja)
                else:
                    print('Taki produkt znajduje się już na magazynie')

        # podaje stan konta w $
            elif zapytanie == 'konto' :
                print(f'Stan konta to :{self.stan_konta} $')

        # wyswietla wszystkie produkty ich ilosc i cene jakie sa w magazynie
            elif zapytanie == 'lista':
                print('Lista produktów w magazynie:')
                for k, v in self.stan_magazynu.items():
                    print(f'{k} : {v}')

        # wyswietla tylko jeden produkt podany przez uzytkownika
            elif zapytanie == 'magazyn':
                pytanie = input('Zapas jakiego produktu chcesz zobaczyć?: ')
                if pytanie not in self.stan_magazynu:
                    print('Nie ma takiego produktu w magazynie!')
                else:
                   print(f'{pytanie} : {self.stan_magazynu.get(pytanie)}')

        # historia dokonanych przez uzytkownika akcji, ktore zapisuja sie na liscie
            elif zapytanie == 'przeglad' and len(self.historia_akcji) > 0:
                while True:
                    while True:
                        try:
                            liczba_od = int(input('Podaj początek zakresu: '))
                            liczba_do = int(input('Podaj koniec zakresu: '))
                            break
                        except ValueError :
                            print(self.historia_akcji)
                    if liczba_od <= 0 or liczba_do > len(self.historia_akcji) :
                        print(f'Podałeś liczby spoza zakresu. Oto liczba dotychczasowych akcji : {len(self.historia_akcji)}')
                    else :
                        print(self.historia_akcji[liczba_od - 1 :liczba_do])
                        break

# funkcja odpowiadajaca za zapis do pliku
    def save_to_file(self):
        with open(self.filename, 'w') as f:
            f.write(f'Stan konta&&{self.stan_konta}\n')
        with open(self.filename, 'a') as f:
            for k, v in self.stan_magazynu.items():
                f.write(k + '%%')
                f.write(str(v) + '\n')
            for k in self.historia_akcji:
                f.write(k + '&&\n')


# wlasciwa czesc programu
if __name__ == "__main__":
    manager = Manager()
    while True:
        print("1.Wpisz 'saldo' aby dodać lub odjąć kwotę z konta"
              "\n2.Wpisz 'sprzedaz' aby wybrać SPRZEDAŻ"
              "\n3.Wpisz 'zakup' aby wybrać ZAKUP"
              "\n4.Wpisz 'konto' aby wyświetlić stan konta"
              "\n5.Wpisz 'lista' aby wyświetlić pełny stan magazynu"
              "\n6.Wpisz 'magazyn' aby wyświetlić ilość konkretnego produktu na stanie"
              "\n7.Wpisz 'przeglad' aby wyświetlić historię zmian"
              "\n8.Wpisz 'koniec' aby zakończyć działanie programu")

        inquiry = input("Co wybierasz? : ")

        # Jeżeli użytkownik wpisuje "koniec", program kończy działanie
        if inquiry == "koniec":
            manager.save_to_file()
            break

        manager.assign(inquiry)


