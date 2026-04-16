import time
import math
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

# --- Insertion Sort z insertion_sort.py ---
def insertion_sort_range(data, start, end, drawData, update_Matryki):
    #gb.czas_startu = time.time() myslia ze powoduje problem z czasem
    
    for i in range(start + 1, end + 1):
        key = data[i]
        j = i - 1
        
        if not Pauza_Krok(): return False
        
        # Logika kolorou z insertrion_sort.py
        colorArray = []
        for x in range(len(data)):
            if x == i:
                colorArray.append("yellow")
            elif x >= start and x < i:
                colorArray.append("blue")
            else:
                colorArray.append("red")
        
        drawData(data=data, colorArray=colorArray)

        while j >= start and data[j] > key:
            gb.porownanie += 1
            if not Pauza_Krok(): return False
            
            # Z 
            colorArray = []
            for x in range(len(data)):
                if x == j:
                    colorArray.append("purple")  # Porównywany/przesuwany element
                elif x == j + 1:
                    colorArray.append("yellow")  # aktywny element
                elif x >= start and x <= i:
                    colorArray.append("blue")    # Posortowana partycja
                else:
                    colorArray.append("red")     # Niesortowana partycja

            drawData(data=data, colorArray=colorArray)
            time.sleep(gb.time_tick)
            
            data[j + 1] = data[j]
            gb.zapisy += 1
            gb.zmiany += 1
            j -= 1
            
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

        data[j + 1] = key
        gb.zapisy += 1
        if not Pauza_Krok(): return False

    return True

# --- Heapify z heap_sort.py ---
def heapify_range(data, n, i, start, end_range, drawData, update_Matryki):
    largest = i
    # Adjust child indices based on start offset
    left = 2 * (i - start) + 1 + start
    right = 2 * (i - start) + 2 + start
    
    # Oblicz bezwzględny indeks, w którym heap konczy się w tym zakresie
    heap_end_idx = start + n

    if not Pauza_Krok(): return False

    # Kolory z heap_sort.py 
    colorArray = []
    for x in range(len(data)):
        if x >= heap_end_idx and x <= end_range:
            colorArray.append("blue")   # Elementy już posortowane (poza kopcem) zostają sinie
        elif x == i:
            colorArray.append("yellow") # Aktualny rodzic
        elif x == left or x == right:
            colorArray.append("purple") # Dzieci
        elif x >= start and x < heap_end_idx:
            colorArray.append("red")    # Reszta nieposortowanego kopca
        else:
            colorArray.append("red")    # poza zakresem
            
    drawData(data=data, colorArray=colorArray)
    time.sleep(gb.time_tick)

    gb.porownanie += 1
    if left < heap_end_idx and data[left] > data[largest]:
        largest = left

    gb.porownanie += 1
    if right < heap_end_idx and data[right] > data[largest]:
        largest = right

    if largest != i:
        data[i], data[largest] = data[largest], data[i]
        gb.zmiany += 1
        gb.zapisy += 3
        
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
        if heapify_range(data, n, largest, start, end_range, drawData, update_Matryki) is False:
            return False
    return True


def heap_sort_range(data, start, end, drawData, update_Matryki):
    # Całkowita liczba elementów w tym zakresie
    n_total = end - start + 1
    
    # 1. Budowanie maksymalnego heap
    for i in range(start + (n_total // 2) - 1, start - 1, -1):
        if heapify_range(data, n_total, i, start, end, drawData, update_Matryki) is False: return False

    # 2. ekstracja elementów
    for i in range(end, start, -1):
        if not Pauza_Krok(): return False
        
        data[i], data[start] = data[start], data[i]
        gb.zmiany += 1
        gb.zapisy += 3
        
        # Aktualny rozmiar heap zmniejsza się o 1
        current_heap_size = i - start
        
        
        colorArray = []
        for x in range(len(data)):
            if x == i:
                colorArray.append("green")  # Właśnie umieszczony element
            elif x > i and x <= end:
                colorArray.append("blue")   # Już posortowane
            elif x >= start and x < i:
                colorArray.append("red")    # Pozostała sterta
            else:
                colorArray.append("red")    # Pozostała sterta

        drawData(data=data, colorArray=colorArray)
        time.sleep(gb.time_tick)
        
        # Restore heap property
        if heapify_range(data, current_heap_size, start, start, end, drawData, update_Matryki) is False: return False
        
    return True

# --- Partition z quick ---
# --- 1. Pomoc: logika koloru z quicksort.py ---
def getColorArray(dataLen, head, tail, border, currentIndex, isSwaping=False):
    collorArray = []
    for i in range(dataLen):
        # Base Coloring
        if i >= head and i <= tail:
            collorArray.append("gray")
        else:
            collorArray.append("white")

        if i == tail:
            collorArray[i] = "blue"

        if i == border:
            collorArray[i] = "red"
        
        if i == currentIndex:
            collorArray[i] = "yellow"

        if isSwaping and (i == border or i == currentIndex):
            if i != currentIndex:    # -- currentIndex zostaje zolty --
                collorArray[i] = "green"

        # -- Current index ma najwyższy priorytet --
        if i == currentIndex:
            collorArray[i] = "yellow"

    return collorArray

# --- 2. Partition z quick sort ---
def partition(data, head, tail, drawData, update_Matryki):
    border = head
    pivot = data[tail]
    
    # Initial Draw
    drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=border))
    if not Pauza_Krok(): return None
    time.sleep(gb.time_tick)

    for i in range(head, tail):
        # --- Pauza / krok ---
        if not Pauza_Krok(): return None

        # --- Aby widziec index kazdy raz ---
        drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=i, isSwaping=False))
        time.sleep(gb.time_tick)

        gb.porownanie += 1

        if data[i] < pivot:
            # -- Change Color in the swap -- 
            drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=i, isSwaping=True))
            if not Pauza_Krok(): return None
            time.sleep(gb.time_tick)

            data[border], data[i] = data[i], data[border]

            # -- Metryki --
            gb.zmiany += 1
            gb.zapisy += 3
            
            border += 1

            drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=i))
            if not Pauza_Krok(): return None
            time.sleep(gb.time_tick)

        # -- Aktualizacja metryk --
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

    # --- Swap pivot with border value ---
    drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=tail, isSwaping=True))
    time.sleep(gb.time_tick)
    
    data[border], data[tail] = data[tail], data[border]

    # -- Finalna Aktualizacja Metryk --
    gb.zmiany += 1
    gb.zapisy += 3
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

    return border

# --- Intro Sort Główna Rekursja ---
def intro_sort_util(data, start, end, depth_limit, drawData, update_Matryki):
    if not Pauza_Krok(): return False
    
    size = end - start
    
    # Użyj sortowania Insert Sort dla małych partycji (16)
    if size < 16:
        if insertion_sort_range(data, start, end, drawData, update_Matryki) is False:
            return False
        return True

    # Jeśli rekurencja jest zbyt deep, przełącz na Heap Sort
    if depth_limit == 0:
        if heap_sort_range(data, start, end, drawData, update_Matryki) is False:
            return False
        return True

    # Standardowa partycja QuickSort
    p = partition(data, start, end, drawData, update_Matryki)
    if p is None: return False
    
    if intro_sort_util(data, start, p - 1, depth_limit - 1, drawData, update_Matryki) is False:
        return False
    if intro_sort_util(data, p + 1, end, depth_limit - 1, drawData, update_Matryki) is False:
        return False
    
    return True

# --- Punkt entry ---
def intro_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    depth_limit = 2 * math.log2(len(data))
    
    byloUdany = intro_sort_util(data, 0, len(data) - 1, int(depth_limit), drawData, update_Matryki)
    
    if byloUdany:
        # Finale kolorowanie
        drawData(data=data, colorArray=["green" for x in range(len(data))])
        
        # Finalne metryki 
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)