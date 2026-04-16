import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

# --- Helper: Color Logic (Adapted from your Quick Sort) ---
def getColorArray(dataLen, start, end, activeIdx, isSwaping=False):
    collorArray = []
    for i in range(dataLen):
        # 1. Base Coloring (White)
        collorArray.append("white")

        # 2. Active Partition Range (Gray) - Like Head/Tail in QuickSort
        if i >= start and i <= end:
            collorArray[i] = "gray"

        # 3. Active Writing Index (Yellow/Green) - Like CurrentIndex in QuickSort
        if i == activeIdx:
            if isSwaping:
                collorArray[i] = "green" # Writing/Changing value
            else:
                collorArray[i] = "yellow" # Examining position

    return collorArray

def merge(data, start, mid, end, drawData, update_Matryki):
    # Create temporary copies (Standard Merge Sort logic)
    left_part = data[start:mid + 1]
    right_part = data[mid + 1:end + 1]

    i = 0 # Index for left_part
    j = 0 # Index for right_part
    k = start # Index for main data array (This is our 'currentIndex')

    # --- Merge Loop ---
    while i < len(left_part) and j < len(right_part):
        
        # --- Pauza / krok ---
        if not Pauza_Krok(): return False

        # --- Show current index (Yellow) ---
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=False))
        time.sleep(gb.time_tick)

        gb.porownanie += 1
        
        # Decide which element to pick
        if left_part[i] <= right_part[j]:
            val_to_write = left_part[i]
            i += 1
        else:
            val_to_write = right_part[j]
            j += 1
        
        # --- Visualise Write (Green) ---
        # We perform the write and highlight it green, similar to the swap in QuickSort
        data[k] = val_to_write
        
        gb.zapisy += 1
        gb.zmiany += 1
        
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=True))
        if not Pauza_Krok(): return False
        time.sleep(gb.time_tick)

        # -- Aktualizacja metryk --
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
        k += 1

    # --- Copy remaining elements from Left (if any) ---
    while i < len(left_part):
        if not Pauza_Krok(): return False
        
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=False))
        time.sleep(gb.time_tick)

        data[k] = left_part[i]
        gb.zapisy += 1
        gb.zmiany += 1
        
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=True))
        time.sleep(gb.time_tick)
        
        i += 1
        k += 1
        
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)

    # --- Copy remaining elements from Right (if any) ---
    while j < len(right_part):
        if not Pauza_Krok(): return False
        
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=False))
        time.sleep(gb.time_tick)

        data[k] = right_part[j]
        gb.zapisy += 1
        gb.zmiany += 1
        
        drawData(data=data, colorArray=getColorArray(len(data), start, end, k, isSwaping=True))
        time.sleep(gb.time_tick)
        
        j += 1
        k += 1
        
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
    return True

def merge_sort_recursion(data, start, end, drawData, update_Matryki):
    # Pauza / krok
    if not Pauza_Krok(): return None

    if start < end:
        mid = (start + end) // 2
        
        # 
        
        # --- Recursive Left ---
        if merge_sort_recursion(data, start, mid, drawData, update_Matryki) is None: return None
        
        # --- Recursive Right ---
        if merge_sort_recursion(data, mid + 1, end, drawData, update_Matryki) is None: return None
        
        # --- Merge ---
        if merge(data, start, mid, end, drawData, update_Matryki) is False: return None

    return True

# --- Main Entry Point ---
def merge_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    
    # Start recursion
    if merge_sort_recursion(data, 0, len(data)-1, drawData, update_Matryki) is not None:
        
        # If finished successfully, show full green
        if not gb.stop_signal:
            drawData(data=data, colorArray=["green" for x in range(len(data))])
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)