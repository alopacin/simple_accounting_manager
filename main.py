# zainicjowanie klasy manager
class Manager:
    def __init__(self):
        self.warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
        self.stan_magazynu = dict()
        self.historia_akcji = []
        self.akcja = 0
        self.stan_konta = 1000
        self.filename = 'history.txt'
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
            return decorate

    def execute(self, name):
        if name not in self.actions:
            print('Błąd')
        else:
            self.actions[name](self)

    def load_data(self):
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
manager = Manager()
manager.load_data()
while True:
     print("1.Wpisz 'saldo' aby dodać lub odjąć kwotę z konta"
             "\n2.Wpisz 'sprzedaz' aby wybrać SPRZEDAŻ"
             "\n3.Wpisz 'zakup' aby wybrać ZAKUP"
             "\n4.Wpisz 'konto' aby wyświetlić stan konta"
             "\n5.Wpisz 'lista' aby wyświetlić pełny stan magazynu"
             "\n6.Wpisz 'magazyn' aby wyświetlić ilość konkretnego produktu na stanie"
             "\n7.Wpisz 'przeglad' aby wyświetlić historię zmian"
             "\n8.Wpisz 'koniec' aby zakończyć działanie programu")

        zapytanie = input("Co wybierasz? : ")

# jezeli podanej wartosci nie ma na liscie warunkow program pyta uzytkownika jeszcze raz co chce zrobic
if zapytanie not in manager.actions and zapytanie != 'koniec':
        print('Wpisałeś nieprawidłową wartość.Spróbuj jeszcze raz!')

        # dodanie i odjecie przez uzytkownika kwoty z konta
        elif zapytanie in manager.actions:
            manager.execute(zapytanie)

        # sprzedaz, ktora dodaje kwote wpisana przez uzytkownika do salda i odejmuje dane produkty z magazynu
        elif zapytanie == 'sprzedaz':
            manager.execute(zapytanie)

        # zakup, ktory odejmuje kwote z konta i dodaje produkty do magazynu
        elif zapytanie == 'zakup':
            manager.execute(zapytanie)

        # podaje stan konta w $
        elif zapytanie == 'konto':
            manager.execute(zapytanie)

        # wyswietla wszystkie produkty ich ilosc i cene jakie sa w magazynie
        elif zapytanie == 'lista':
            manager.execute(zapytanie)

        # wyswietla tylko jeden produkt podany przez uzytkownika
        elif zapytanie == 'magazyn':
            manager.execute(zapytanie)

        # historia dokonanych przez uzytkownika akcji, ktore zapisuja sie na liscie
        elif zapytanie == 'przeglad' and len(manager.historia_akcji) > 0:
            manager.execute(zapytanie)

        # Jeżeli użytkownik wpisuje "koniec", program kończy działanie
        if zapytanie == "koniec":
            manager.save_to_file()
            break


@manager.assign('zmiana stanu konta')
def balance_request(self):
    while True:
        zapytanie_o_saldo = int(input('Wybierz 1 jeżeli chcesz dodać kwotę. Wybierz 2 jeżeli chcesz odjąć kwotę: '))
        if zapytanie_o_saldo == 1:
            saldo = float(input('Wpisz kwotę: '))
            self.stan_konta += saldo
            print(f'Dodano {saldo} $ do konta')
            akcja = f'Dodano {saldo} $ do konta'
            self.historia_akcji.append(akcja)
            break
        elif zapytanie_o_saldo == 2:
            saldo = int(input('Wpisz kwotę: '))
            self.stan_konta -= saldo
            print(f'Odjęto {saldo} $ z konta')
            akcja = f'Odjęto {saldo} $ z konta'
            self.historia_akcji.append(akcja)
            break
        else:
            print('Podano nieprawidłową liczbę')

@manager.assign('sprzedaz')
def to_sale(self):
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

@manager.assign('zakup')
def to_purchase(self):
    nazwa_produktu = input('Podaj jaki produkt ma zostać zakupiony: ')
    if nazwa_produktu not in self.stan_magazynu:
        cena_produktu = float(input('Podaj cenę produktu: '))
        liczba_sztuk = int(input('Podaj liczbę zakupionych sztuk: '))
        laczna_cena = cena_produktu * liczba_sztuk
        if laczna_cena > self.stan_konta:
            print('Brakuje pieniędzy na zakup')
        elif laczna_cena < self.stan_konta:
            self.stan_magazynu[nazwa_produktu] = {'ilość': liczba_sztuk, 'cena': cena_produktu}
            self.stan_konta -= laczna_cena
            print(f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $')
            akcja = f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $'
            self.historia_akcji.append(akcja)
    else:
        print('Taki produkt znajduje się już na magazynie')

@manager.assign('stan konta')
def show_account_balance(self):
    return f'Stan konta to :{self.stan_konta} $'

@manager.assign('lista produktow')
def show_list_of_products(self):
    print('Lista produktów w magazynie:')
    for k, v in self.stan_magazynu.items():
            return f'{k} : {v}'

@manager.assign('pokaz produkt')
def show_product(self):
    pytanie = input('Zapas jakiego produktu chcesz zobaczyć?: ')
    if pytanie not in self.stan_magazynu:
        print('Nie ma takiego produktu w magazynie!')
    else:
        return f'{pytanie} : {self.stan_magazynu.get(pytanie)}'

@manager.assign('historia')
def show_action_history(self):
    while True:
        while True:
            try:
                liczba_od = int(input('Podaj początek zakresu: '))
                liczba_do = int(input('Podaj koniec zakresu: '))
                break
            except ValueError:
                print(self.historia_akcji)
        if liczba_od <= 0 or liczba_do > len(self.historia_akcji):
            print(f'Podałeś liczby spoza zakresu. Oto liczba dotychczasowych akcji : {len(self.historia_akcji)}')
        else:
            print(self.historia_akcji[liczba_od - 1:liczba_do])
            break





