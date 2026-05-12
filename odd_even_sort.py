import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def odd_even_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    n = len(data)
    isSorted = False
    
    while not isSorted:
        isSorted = True
        
        if not Pauza_Krok(): return None
        
        # --- nieparzyste ---
        for i in range(1, n - 1, 2):
            drawData(data=data, colorArray=["blue" if x == i or x == i+1 else "red" for x in range(len(data))])
            if not gb.Czekaj(): return None
            if not Pauza_Krok(): return None
            
            gb.porownanie += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                isSorted = False
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
                
        # --- parzyste ---
        for i in range(0, n - 1, 2):
            drawData(data=data, colorArray=["green" if x == i or x == i+1 else "red" for x in range(len(data))])
            if not gb.Czekaj(): return None
            if not Pauza_Krok(): return None
            
            gb.porownanie += 1
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                isSorted = False
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
                
    drawData(data=data, colorArray=["green" for x in range(len(data))])
