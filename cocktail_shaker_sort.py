import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def cocktail_shaker_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    n = len(data)
    swapped = True
    start = 0
    end = n - 1

    def getColorArray(left, right, first, second, highlight):
        colorArray = []
        for x in range(n):
            if x < left or x > right:
                colorArray.append("blue")
            elif x == first or x == second:
                colorArray.append(highlight)
            else:
                colorArray.append("red")
        return colorArray
    
    while swapped:
        swapped = False
        
        # --- Bubble Sort w prawo ---
        for i in range(start, end):
            if not Pauza_Krok(): return None
            
            drawData(data=data, colorArray=getColorArray(start, end, i, i + 1, "yellow"))
            if not gb.Czekaj(): return None

            gb.porownanie += 1
            swapped_now = False

            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                swapped = True
                swapped_now = True

            if swapped_now:
                drawData(data=data, colorArray=getColorArray(start, end, i, i + 1, "green"))
                if not gb.Czekaj(): return None
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

        if not swapped: break
        swapped = False
        end -= 1
        
        # ---- Bubble Sort w lewo ----
        for i in range(end - 1, start - 1, -1):
            if not Pauza_Krok(): return None
            
            drawData(data=data, colorArray=getColorArray(start, end, i, i + 1, "yellow"))
            if not gb.Czekaj(): return None

            gb.porownanie += 1
            swapped_now = False

            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                gb.zmiany += 1
                gb.zapisy += 3
                swapped = True
                swapped_now = True

            if swapped_now:
                drawData(data=data, colorArray=getColorArray(start, end, i, i + 1, "green"))
                if not gb.Czekaj(): return None
                
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        start += 1
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])
