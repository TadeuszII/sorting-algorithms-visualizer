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
            
            gb.porownanie += 1
            
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                
                # -- Ustawiamy flagę, że dokonano zmiany --
                swapped = True 
                
                gb.zmiany += 1
                gb.zapisy += 3

            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
            

            drawData(data=data, colorArray=["green" if x == j or x == j+1 else "red" for x in range(len(data))])
            
            if not Pauza_Krok():
                return None
            time.sleep(gb.time_tick)

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