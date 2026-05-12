import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def gnome_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    index = 0
    n = len(data)

    def getColorArray(current, previous=None, highlight="yellow"):
        colorArray = []
        for x in range(n):
            if x < current:
                colorArray.append("blue")
            else:
                colorArray.append("red")

        if previous is not None and 0 <= previous < n:
            colorArray[previous] = "purple"
        if 0 <= current < n:
            colorArray[current] = highlight
        return colorArray
    
    while index < n:
        if not Pauza_Krok(): return None
        
        previous = index - 1 if index > 0 else None
        drawData(data=data, colorArray=getColorArray(index, previous))
        if not gb.Czekaj(): return None
        
        gb.porownanie += 1
        if index == 0:
            index += 1
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        elif data[index] >= data[index - 1]:
            index += 1
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        else:
            data[index], data[index - 1] = data[index - 1], data[index]
            gb.zmiany += 1
            gb.zapisy += 3
            drawData(data=data, colorArray=getColorArray(index, index - 1, highlight="green"))
            if not gb.Czekaj(): return None
            index -= 1
            
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
            
    drawData(data=data, colorArray=["green" for x in range(len(data))])
