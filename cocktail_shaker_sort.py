import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def cocktail_shaker_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    n = len(data)
    swapped = True
    start = 0
    end = n - 1
    
    while swapped:
        swapped = False
        
        # --- Bubble Sort w prawo ---
        for i in range(start, end):
            if not Pauza_Krok(): return None
            
            gb.porownanie += 1
            drawData(data=data, colorArray=["green" if x == i or x == i+1 else "red" for x in range(len(data))])
            time.sleep(gb.time_tick)

            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                swapped = True
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

        if not swapped: break
        swapped = False
        end -= 1
        
        # ---- Bubble Sort w lewo ----
        for i in range(end - 1, start - 1, -1):
            if not Pauza_Krok(): return None
            
            gb.porownanie += 1
            drawData(data=data, colorArray=["green" if x == i or x == i+1 else "red" for x in range(len(data))])
            time.sleep(gb.time_tick)

            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                swapped = True
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        start += 1
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])