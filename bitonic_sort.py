import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def compAndSwap(data, i, j, dire, drawData, update_Matryki):
    if not Pauza_Krok(): return False
    
    drawData(data=data, colorArray=["yellow" if x == i or x == j else "red" for x in range(len(data))])
    if not gb.Czekaj(): return False
    if not Pauza_Krok(): return False
    
    gb.porownanie += 1
    if (dire == 1 and data[i] > data[j]) or (dire == 0 and data[i] < data[j]):
        data[i], data[j] = data[j], data[i]
        gb.zmiany += 1
        gb.zapisy += 3
        
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
    return True

def bitonicMerge(data, low, cnt, dire, drawData, update_Matryki):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            if compAndSwap(data, i, i + k, dire, drawData, update_Matryki) is False: 
                return False
        if bitonicMerge(data, low, k, dire, drawData, update_Matryki) is False: return False
        if bitonicMerge(data, low + k, k, dire, drawData, update_Matryki) is False: return False
    return True

def bitonicSortRec(data, low, cnt, dire, drawData, update_Matryki):
    if cnt > 1:
        k = cnt // 2
        if bitonicSortRec(data, low, k, 1, drawData, update_Matryki) is False: return False
        if bitonicSortRec(data, low + k, k, 0, drawData, update_Matryki) is False: return False
        if bitonicMerge(data, low, cnt, dire, drawData, update_Matryki) is False: return False
    return True

def bitonic_sort(*, data, drawData, update_Matryki, isPowerOfTwo):
    gb.czas_startu = time.time()
    # Bitonic sort najlepiej działa dla danych o długości potęgi 2
    if bitonicSortRec(data, 0, len(data), 1, drawData, update_Matryki) is False: return None
    
    if isPowerOfTwo: # Jezeli liczba elementów jest kolejną liczbą dwójki 2^k znaczy będzie dobrze posortowane.
        drawData(data=data, colorArray=["green" for x in range(len(data))])
    else: # Nie jest dobrze posortowana
        drawData(data=data, colorArray=["red" for x in range(len(data))])
        
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
