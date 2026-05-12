import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def heapify(data, n, i, drawData, update_Matryki):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if not Pauza_Krok(): return False

    colorArray = []
    for x in range(len(data)):
        if x >= n:
            colorArray.append("blue")  # Elementy już posortowane (poza kopcem) zostają sinie
        elif x == i:
            colorArray.append("yellow") # Aktualny rodzic
        elif x == left or x == right:
            colorArray.append("purple") # Dzieci
        else:
            colorArray.append("red")    # Reszta nieposortowanego kopca

    drawData(data=data, colorArray=colorArray)
    time.sleep(gb.time_tick)

    if left < n:
        gb.porownanie += 1
        if data[left] > data[largest]:
            largest = left

    if right < n:
        gb.porownanie += 1
        if data[right] > data[largest]:
            largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        gb.zmiany += 1
        gb.zapisy += 3
        
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
        if heapify(data, n, largest, drawData, update_Matryki) is False:
            return False
    return True

def heap_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    n = len(data)

    # -- Zbuduj maksymalny heap --
    for i in range(n // 2 - 1, -1, -1):
        if heapify(data, n, i, drawData, update_Matryki) is False: return None

    # -- Ekstracja elemntów --
    for i in range(n - 1, 0, -1):
        if not Pauza_Krok(): return None
        
        data[i], data[0] = data[0], data[i]
        gb.zmiany += 1
        gb.zapisy += 3
        
        # Element na końcu [i] jest posortowany olor niebieski
        drawData(data=data, colorArray=["green" if x == i else "blue" if x > i else "red" for x in range(len(data))])
        time.sleep(gb.time_tick)
        
        if heapify(data, i, 0, drawData, update_Matryki) is False: return None
        
    drawData(data=data, colorArray=["green" for x in range(len(data))])
