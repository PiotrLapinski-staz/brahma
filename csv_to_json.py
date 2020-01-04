import csv
import json
import pandas as pd
import numpy as np
#POTRZEBNE DO SPRAWDZENIA CZY LICZBA JEST CAŁKOWITA
def is_int(val):
    if type(val) == int:
        return True
    else:
        return False

path="D:\\POBRANE\\POBRANE OPERA\\KOLOS STAT\\zadania\\MATEUSZ ZDJECIA\\dane_oczyszczone.csv"
csv_meta_path="D:\\bPOZNANIA\\csv_meta.csv"
csv_full_path="D:\\bPOZNANIA\\csv_full.csv"
f2=open(csv_full_path,mode="w",encoding="utf-8")
f3=open(csv_meta_path,mode="w",encoding="utf-8")
# PONIZEJ ZAPISANE BEDA POSZCZEGOLNE ELEMENTY
sesja=[]
cechy=[]
narodowosc=""
grupa=0
wiek=""
data=""
nr_sesji=1
liczba_grup=0
l_akcji = 0
#SLOWNIK Z WERSJAMI JEZYKOWYMI I WIEKOWYMI
jezyki={'L0': ['polski', 'dorośli'], 'L1': ['polski', 'dzieci'], 'L2': ['angielski', 'dorośli'], 'L3': ['angielski', 'dzieci'], 'L4': ['niemiecki', 'dorośli'], 'L5': ['niemiecki', 'dzieci'], 'L6': ['hiszpański', 'dorośli'], 'L7': ['hiszpański', 'dzieci'], 'L8': ['francuski', 'dorośli'], 'L9': ['francuski', 'dzieci'], 'L10': ['czeski', 'dorośli'], 'L11': ['czeski', 'dzieci'], 'L12': ['rosyjski', 'dorośli'], 'L13': ['rosyjski', 'dzieci'], 'L14': ['ukraiński', 'dorośli'], 'L15': ['ukraiński', 'dzieci']}

#METODA DZIELI LISTE POWSTAŁA Z LINIJKI NA JEJ POSZCZEGOLNE ELEMENTY I ZAPISUJE JAKO LISTE
def podział(lista):
    nr_urzadzenia=lista[1].replace(".xml","")
    godzina_akcji=lista[3]
    akcja=lista[4]
    strefa=lista[5]
    nagranie=lista[6].replace("\n","")
    lista2 = [nr_urzadzenia, nr_sesji, godzina_akcji, akcja, strefa, nagranie]

    #Wiek sprawdzimy po akcjach
    #Grupę sprawdzimy po sektorach
    return lista2

with open(path,encoding="utf-8") as plik:
    działanie = 0
    while (0<10000):
        linia= plik.readline()
        linia2 = linia.split(";")
        if linia2[4]=="Włączenie urządzenia":
            działanie= 1
            #print("Włączenie")
        if linia2[4]=="Wyłączenie urządzenia":
            działanie = 2
            #print("Wyłączenie")
            #OD MOMENTU WŁĄCZENIA URZADZENIA
        if działanie == 1:
            sesja.append(linia2)
            #SPRAWDZAMY CZY CZŁONEK GRUPY PO URUCHOMIONYM SEKTORZE
            if linia2[5] != "":
                try:
                    sek=int(linia2[5])

                    if sek<9000 and sek>7999:
                        grupa=1
                        liczba_grup+=1
                    else:
                        grupa=0
                except:
                    linia2[5]=""
            #SPRAWDZAMY CZY DOSZLO DO WYBORU SCIEZKI
            if "ścieżki" in linia2[4].split():
                #print("WYBOR SCIEZKI")
                ścieżka=linia2[4].replace("Wybór ścieżki ","")

                if ścieżka in jezyki.keys():

                    narodowosc=jezyki[ścieżka][0]
                    wiek=jezyki[ścieżka][1]

        #KONIEC ZAPISU DO LSITY
        if działanie == 2:
            #podział danych,
            #zapis danych
            #czyszczenie sesji
            sesja.append(linia2)
            data = linia2[2]
            nr_urz=linia2[1].replace(".xml","")

#Teraz sesja zawiera liste list taką, że [[elementy pierwszej linijki],[el drugiej linii],[el 3 linii]....]
            for i,element in enumerate(sesja):
                l_akcji+=1
                #Dziele kazda linijke na jej poszczegolne elementy
                e2=podział(element)
                #(pobieram godzine rozpoczecia i zakonczenia)
                if i==0:
                    g_rozp=e2[2]
                if i==(len(sesja)-1):
                    g_zak=e2[2]
                #ZAPISUJE OBA PLIKI I KONCZE SESJE CZYSZCZAC ZMIENNE I WRACAJAC DO STANU 0
                for czesc in e2:
                    f2.write(str(czesc)+",")
                f2.write("\n")
            cechy = str(nr_urz)+","+str(nr_sesji)+","+data+","+g_rozp+","+g_zak+','+narodowosc+","+wiek+","+str(grupa)+","+str(l_akcji)
            f3.write(cechy+"\n")
            działanie=0
            l_akcji=0
            grupa=0
            cechy=[]
            sesja=[]
            print("Zapisano sesje"+ str(nr_sesji))
            print(liczba_grup)
            nr_sesji += 1