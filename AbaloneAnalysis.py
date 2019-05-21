# Politechnika Łódzka 2018
# Bartłomiej Jencz grupa 4 216783
# Analiza danych
# Data set abalone
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sys import exit

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def MainMenu():
    print("--------------------------------------------------")
    print("|    1.Wyswietl dane statstyczne z modułu Pandas |")
    print("|    2.Wyswietl dane liczone wzorami             |")
    print("|    3.Narysuj histogramy                        |")
    print("|    4.Naryszuj wykresy pudelkowe                |")
    print("|    5.Zmien opcje debugowania                   |")
    print("|    6.Zmien opcje rysowania wykresow            |")
    print("|    9.Zakoncz program                           |")
    print("--------------------------------------------------")
    selection = int(input("Wybierz opcje: "))
    if selection == 1:
        # dosmt
        print("Wybrales opcje 1")
    elif selection == 2:
        print("Wybrales opcje 2")
    elif selection == 3:
        print("Wybrales opcje 3")
    elif selection == 4:
        print("Wybrales opcje 4")
    elif selection == 5:
        print("Wybrales opcje 5")
    elif selection == 6:
        print("Wybrales opcje 6")
    elif selection == 9:
        print("Wyjscie")
        exit()
    else:
        print("Zly wybor. Wybierz 1-3")
        MainMenu()
    return selection

# Main ROUTINE

# <editor-fold desc="drugi rodzaj wczytania danych - obsolete">
# headers = ['Sex','Length','Diameter','Height','Whole weight','Shucked weight','Viscera weight','Shell weight','Rings']
# df = pd.read_csv("abalone.data", names=headers, header=None)1
# </editor-fold>

df = pd.read_csv("abalone.data", header=None)
debug = False
wyswietlanie_wykresow = True
srednie = []
lista = []
wariancjatab = []
odchylenietab = []
wariancja = 0
liczbakolumn = 8

# region Podziel kazda kolumne na  osobne listy
for index, row in df.iterrows():
    lista.append(df[index].tolist())
    if index == liczbakolumn:
        break
# endregion

# region Podziel listy po sredniej
for index, row in df.iterrows():
    srednie.append(mean(lista[index + 1]))
    if index + 1 == liczbakolumn:
        break
# endregion

print()

# region Podziel listy na wariancje i odchylenia
for j in range(liczbakolumn + 1):
    wariancja = 0
    if j == liczbakolumn:
        break
    for i in range(len(lista[0])):
        wariancja += (lista[j + 1][i] - srednie[j]) * (lista[j + 1][i] - srednie[j])
    wariancja = (wariancja / len(lista[0]))
    wariancjatab.append(wariancja)
    odchylenietab.append(np.sqrt(wariancja))
    if j == liczbakolumn:
        break
# endregion

# Index_1_kolumny wybiera ktora kolumna chcemy sie zajac
# Trzab zrobic do niej wybor
index_1_kolumny = wariancjatab.index(min(wariancjatab))
index_2_kolumny = wariancjatab.index(max(wariancjatab))
wybor = MainMenu()


def analizastatystyczna(ktora_kolumna):
    # Przedzialy klasowe
    ilosc_przedzialow_klasowych = np.floor(1 + 3.222 * np.log(len(lista[0])))
    x_max = max(lista[ktora_kolumna + 1])
    x_min = min(lista[ktora_kolumna + 1])
    rozstep_z_proby = x_max - x_min
    h = rozstep_z_proby / ilosc_przedzialow_klasowych
    alfa = 0.01
    a = x_min - alfa / 2
    moda = max(set(lista[ktora_kolumna + 1]), key=lista[ktora_kolumna + 1].count)
    if debug:
        print("Kolumna", ktora_kolumna + 1)
        print("Odchylenie std", ktora_kolumna + 1, "to", odchylenietab[ktora_kolumna])
        print("Wyznaczam x_max oraz x_min")
        print("x_max", x_max)
        print("x_min", x_min)
        print("Wyznaczam rozstęp z próby")
        print(rozstep_z_proby)
        print("Wyznaczam długość przedziały klasowego h h~R/K")
        print(h)
        print("Za dokladnosc pomiaru  przyjmuje 0.01")
        print("Wyznaczam  lewy  koniec pierwszego przedziału klasowego")
        print(a)
        print("Przedzialy klasowe: ")
        print(ilosc_przedzialow_klasowych)
        print("Miary Statystyczne")
        print("Srednia  z proby  (mediana)")
        print(srednie[ktora_kolumna])
        print("Dominanta")
        print(moda)
        print(np.percentile(df[ktora_kolumna + 1], [25, 50, 75]))
    lista[ktora_kolumna + 1].sort()
    global Punkty
    Punkty = []
    tabela1 = []
    i = 0
    # print("Podzialy:")
    while i < ilosc_przedzialow_klasowych + 1:
        Punkty.append(h * i)
        # print(i, Punkty[i])
        i = i + 1
    if debug:
        print(len(Punkty))
    from bisect import bisect_left

    def split_list(iterable, splitters):
        idxs = [bisect_left(iterable, x) for x in sorted(splitters)]
        return [iterable[x:y] for x, y in zip([0] + idxs, idxs + [len(iterable)]) if x != y]

    tabela1 = split_list(lista[ktora_kolumna + 1], Punkty)

    def oblicz_kwartyl(numer_kwartyla, index_kol):
        q = len(lista[index_kol + 1]) * (numer_kwartyla / 4)
        q = int(q)
        # print(q)
        i = 0
        length = 0
        # print(len(tabela1))
        # print(len(tabela1[0]))
        while i < len(tabela1):
            length = length + len(tabela1[i])
            # print(q, "<", length)
            if q < length:
                # print("znalazlem", i)
                break
            i = i + 1
        ktory_przedzial = i
        i = 0
        ni = 0
        # print("Liczebnosci przedzialow")
        # for x in tabela1:
        #     print(len(x))
        # print("ni")

        # Zliczanie dlugosci przedzialow do kwartyli
        # Skoro bierzemy kwarrtyl 1 a jest przedzialow 8 i wartosc wpada do przedzialu 3 to liczymy liczebnosc przedzialow 1 i 2
        while i < ktory_przedzial:
            ni = ni + len(tabela1[i])
            # print(ni)
            i = i + 1
        # print("liczebnosc przedzialu do kwartylu ",numer_kwartyla, ni)
        # deltai=max(tabela1[ktory_przedzial])-min(tabela1[ktory_przedzial])
        deltai = h
        # print("deltai", deltai)
        # print("dolna granica i-tego przedzialu", tabela1[ktory_przedzial][0])
        Liczebnosc_proby = len(lista[index_kol + 1])
        KWARTYL = tabela1[ktory_przedzial][0] + (
                (((numer_kwartyla / 4) * Liczebnosc_proby - ni) / len(tabela1[ktory_przedzial])) * deltai)
        return KWARTYL

    if debug:
        print("Kwartyl", 1)
        print(oblicz_kwartyl(1, ktora_kolumna))
        print("Kwartyl", 3)
        print(oblicz_kwartyl(3, ktora_kolumna))
    daneStatystyczne = []
    daneStatystyczne.append(len(lista[ktora_kolumna]))
    daneStatystyczne.append(srednie[ktora_kolumna])
    daneStatystyczne.append(odchylenietab[ktora_kolumna])
    daneStatystyczne.append(x_min)
    daneStatystyczne.append(oblicz_kwartyl(1, ktora_kolumna))
    daneStatystyczne.append(moda)
    daneStatystyczne.append(oblicz_kwartyl(3, ktora_kolumna))
    daneStatystyczne.append(x_max)
    return daneStatystyczne


while wybor != 9:

    # region Z modulu Panda wybor==1
    if wybor == 1:
        pd.set_option('display.expand_frame_repr', False)
        print(df.describe())
    # endregion

    # region Dane liczone wzorami wybor==2
    if wybor == 2:
        print("Dane  statystyczne w formacie:")
        print("[liczba pom, srednia, sigma, min, 1/4q, moda, 3/4q, max]")
        for x in range(0, liczbakolumn):
            print(x+1,analizastatystyczna(x))
        print("Kolumna o najmniejszej wariancji to ",index_1_kolumny+1)
        print("Kolumna o największej wariancji to ",index_2_kolumny+1)
    # endregion

    # region Narysuj histogramy wybor==3
    if wybor == 3:
        wybor1 = ''
        if wyswietlanie_wykresow:
            wybor1 = input("Czy chcesz wyswietlic histogramy tylko dla najmniejszych wariancji (T/N) ")
            if wybor1 == "N":
                print("Jesli nie to wyswietlam wszystkie histogramy :)")

        for x in range(0, liczbakolumn):
            dane = analizastatystyczna(x)
            print(dane)
            if wyswietlanie_wykresow and wybor1 == "T":
                if x == index_1_kolumny or x == index_2_kolumny:
                    bin_edges = Punkty
                    plt.hist(lista[x])
                    plt.grid(True)
                    label = "Histogram dla kolumny" + str(x) + " Sigma=" + str(dane[2])
                    plt.xlabel(label)
                    plt.show()
                    xlabel = ""
            elif wyswietlanie_wykresow and wybor1 == "N":
                bin_edges = Punkty
                plt.hist(lista[x])
                plt.grid(True)
                label = "Histogram dla kolumny" + str(x) + " Sigma=" + str(dane[2])
                plt.xlabel(label)
                plt.show()
                xlabel = ""
    # endregion

    # region Narysuj wykrest pudelkowe wybor==4
    if wybor == 4:
        # Wyswietlanie box plotow dla tych z najmniejsza wariancja
        print("Wyswietlam wykresy pudelkowe dla serii z najmniejsza wariancja.")
        df.boxplot(column=index_1_kolumny + 1, return_type='axes')
        plt.show()
        df.boxplot(column=index_2_kolumny + 1, return_type='axes')
        plt.show()
    # endregion

    # region Zmiana opcji debugowania wybor==5
    if wybor == 5:
        if debug == False:
            debug = True
        elif debug == True:
            debug = False
        print("Zmieniles opcje debugowania na", debug)
    # endregion

    # region Zmiana opcji wyswietlania wykresow wybor==6
    if wybor == 6:
        if wyswietlanie_wykresow == True:
            wyswietlanie_wykresow = False
        elif wyswietlanie_wykresow == False:
            wyswietlanie_wykresow = True
        print("Zmieniles opcje wyswietlania wykresow na", wyswietlanie_wykresow)
    # endregion

    wybor = MainMenu()
