import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# import plotly.plotly as py
# import plotly.tools as tls
# import matplotlib.mlab as mlab
# from matplotlib import colors
# from matplotlib.ticker import PercentFormatter
# import re

df = pd.read_csv("seeds.data", header=None)


# df = pd.read_fwf("seeds_dataset.txt")
# print(df)
pd.set_option('display.expand_frame_repr', False)
print(df.describe())
debug = True
liczbakolumn=7

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


srednie = []
lista = []
wariancjatab = []
odchylenietab = []
wariancja = 0

# region Podziel kazda kolumne na  osobne listy
for index, row in df.iterrows():
    lista.append(df[index].tolist())
    if index == liczbakolumn:
        break
# endregion
# region Podziel listy po sredniej
for index, row in df.iterrows():
    srednie.append(mean(lista[index + 1]))
    if index == liczbakolumn:
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
# for index, item in enumerate(wariancjatab, start=0):   # Python indexes start at zero
#     print("Wariancja w kolumnie",index,"wynosi",item)
# print()

# Index_1_kolumny wybiera ktora kolumna chcemy sie zajac
# Trzab zrobic do niej wybor
index_1_kolumny = wariancjatab.index(min(wariancjatab))
index_2_kolumny = wariancjatab.index(max(wariancjatab))


# print("Najmniejsza wariancja to", min(wariancjatab))
# print("Jest to kolumna o indeksie", index_1_kolumny)
# print("Najwieksza wariancja to", max(wariancjatab))
# print("Jest to kolumna o indeksie", index_2_kolumny)


# Tutaj zrobic metode
def analizastatystyczna(ktora_kolumna):
    # Przedzialy klasowe
    ilosc_przedzialow_klasowych = np.floor(1 + 3.222 * np.log(len(lista[0])))
    x_max = max(lista[ktora_kolumna+1])
    x_min = min(lista[ktora_kolumna+1])
    rozstep_z_proby = x_max - x_min
    h = rozstep_z_proby / ilosc_przedzialow_klasowych
    alfa = 0.01
    a = x_min - alfa / 2
    moda = max(set(lista[ktora_kolumna+1]), key=lista[ktora_kolumna+1].count)
    if debug:
        print("-------------------Analizuje kolumne o numerze",ktora_kolumna,"---------------------------")
        print("Kolumna", ktora_kolumna+1)
        print("Odchylenie std", ktora_kolumna+1, "to", odchylenietab[ktora_kolumna])
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
        print(np.percentile(df[ktora_kolumna+1], [25, 50, 75]))
    lista[ktora_kolumna+1].sort()
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

    tabela1 = split_list(lista[ktora_kolumna+1], Punkty)

    def oblicz_kwartyl(numer_kwartyla, index_kol):
        q = len(lista[index_kol+1]) * (numer_kwartyla / 4)
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
        Liczebnosc_proby = len(lista[index_kol+1])
        KWARTYL = tabela1[ktory_przedzial][0] + (
                (((numer_kwartyla / 4) * Liczebnosc_proby - ni) / len(tabela1[ktory_przedzial])) * deltai)

        return KWARTYL

    if debug:
        print("Kwartyl", 1)
        print(oblicz_kwartyl(1, ktora_kolumna))
        print("Kwartyl", 3)
        print(oblicz_kwartyl(3, ktora_kolumna))
        print("-----------------Koniec analizy  kolumny----------------------------------------------------")
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


# plt.hist(lista[index_1_kolumny+1])
# plt.show()
print("Dane  statystyczne w formacie:")
print("[liczba pom, srednia, sigma, min, 1/4q, moda, 3/4q, max]")
for x in range(0, liczbakolumn+1):
    print(analizastatystyczna(x))
    bin_edges = Punkty
    plt.hist(lista[x], bins=bin_edges)
    plt.grid(True)
    label = "Histogram dla kolumny" + str(x)
    plt.xlabel(label)
    plt.show()
    xlabel = ""

# from sys import exit
# exit()
