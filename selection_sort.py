import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def selection_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if not Pauza_Krok(): return None
            
            gb.porownanie += 1
            drawData(data=data, colorArray=["yellow" if x == min_idx else "green" if x == j else "red" for x in range(len(data))])
            if not gb.Czekaj(): return None
            if not Pauza_Krok(): return None

            if data[j] < data[min_idx]:
                min_idx = j

        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            gb.zmiany += 1
            gb.zapisy += 3
        
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])
