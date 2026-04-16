import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def insertion_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        
        if not Pauza_Krok(): return None
        
        drawData(data=data, colorArray=["yellow" if x == i else "blue" if x < i else "red" for x in range(len(data))])

        while j >= 0 and data[j] > key:
            gb.porownanie += 1

            if not Pauza_Krok(): return None

            colorArray = []
            for x in range(len(data)):
                if x == j:
                    colorArray.append("purple")   # Porównywany/przesuwany element
                elif x == j + 1:
                    colorArray.append("yellow")   # aktywny element 
                elif x <= i:
                    colorArray.append("blue")  # Posortowana partycja
                else:
                    colorArray.append("red")      # Niesortowana partycja

            drawData(data=data, colorArray=colorArray)
            time.sleep(gb.time_tick)
            if not Pauza_Krok(): return None
            
            data[j + 1] = data[j]
            gb.zapisy += 1
            gb.zmiany += 1
            j -= 1
            
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

        data[j + 1] = key
        gb.zapisy += 1
        if not Pauza_Krok(): return None

        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

    drawData(data=data, colorArray=["green" for x in range(len(data))])
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)