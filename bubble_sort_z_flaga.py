import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def bubble_sort_z_flaga(*, data, drawData, update_Matryki) -> list:

    gb.czas_startu = time.time()
    n = len(data)
    
    for i in range(n - 1):
        # --- Flaga optymalizacyjna ---
        swapped = False 
        
        for j in range(n - 1 - i):

            # Pauza / krok
            if not Pauza_Krok():
                return None
            
            colorArray = ["blue" if x >= n - i else "red" for x in range(n)]
            colorArray[j] = "yellow"
            colorArray[j + 1] = "yellow"
            drawData(data=data, colorArray=colorArray)
            if not gb.Czekaj():
                return None

            gb.porownanie += 1
            swapped_now = False
            
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                
                # -- Ustawiamy flagę, że dokonano zmiany --
                swapped = True 
                swapped_now = True
                
                gb.zmiany += 1
                gb.zapisy += 3

            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
            

            colorArray = ["blue" if x >= n - i else "red" for x in range(n)]
            colorArray[j] = "green" if swapped_now else "yellow"
            colorArray[j + 1] = "green" if swapped_now else "yellow"
            drawData(data=data, colorArray=colorArray)
            
            if not Pauza_Krok():
                return None
            if not gb.Czekaj():
                return None

        # Aktualizacja metryk po zakończeniu pętli wewnętrznej
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        
        # --- STOPPER ---
        # Jeśli po całym przejściu nie było ani jednej zamiany, stopujemy.
        if not swapped:
            break
        
    # -- Final --
    drawData(data=data, colorArray=["green" for x in range(len(data))])
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
