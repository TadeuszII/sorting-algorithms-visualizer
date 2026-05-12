import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

start_czasu = time.time()



def bubble_sort(*,data, drawData, update_Matryki) -> list:


    gb.czas_startu = time.time()
    for i in range(len(data)-  1):
        for j in range(len(data) - 1 - i):

            # Pauza / krok
            if not Pauza_Krok():
                return None
            
            gb.porownanie += 1
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                gb.zmiany += 1
                gb.zapisy += 3

            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

            drawData(data=data, colorArray=["green" if x == j or x == j+1 else "red" for x in range(len(data))])
            if not Pauza_Krok():
                return None
            if not gb.Czekaj():
                return None

        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

