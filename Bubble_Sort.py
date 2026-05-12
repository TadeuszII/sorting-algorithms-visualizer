import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

start_czasu = time.time()



def bubble_sort(*,data, drawData, update_Matryki) -> list:


    gb.czas_startu = time.time()
    n = len(data)
    for i in range(len(data)-  1):
        for j in range(len(data) - 1 - i):

            # Pauza / krok
            if not Pauza_Krok():
                return None

            colorArray = ["blue" if x >= n - i else "red" for x in range(n)]
            colorArray[j] = "yellow"
            colorArray[j + 1] = "yellow"
            drawData(data=data, colorArray=colorArray)
            if not gb.Czekaj():
                return None
            
            gb.porownanie += 1
            swapped = False
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                gb.zmiany += 1
                gb.zapisy += 3
                swapped = True

            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

            colorArray = ["blue" if x >= n - i else "red" for x in range(n)]
            colorArray[j] = "green" if swapped else "yellow"
            colorArray[j + 1] = "green" if swapped else "yellow"
            drawData(data=data, colorArray=colorArray)
            if not Pauza_Krok():
                return None
            if not gb.Czekaj():
                return None

        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

