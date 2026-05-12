import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

def shell_sort(*, data, drawData, update_Matryki):
    gb.czas_startu = time.time()
    n = len(data)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            
            # --- Rysowanie stanu początkowego dla elementu 'temp' ---
            if not Pauza_Krok(): return None
            
            # Tworzymy tablicę kolorów pokazującą "ścieżkę" (gap)
            colorArray = []
            for x in range(n):
                if x == i:
                    colorArray.append("yellow") # Element brany do wstawienia
                elif x == i - gap:
                    colorArray.append("purple") # Element do porównania
                elif (x % gap) == (i % gap):
                    colorArray.append("gray")   # Elementy z tej samej grupy (gap)
                else:
                    colorArray.append("white")  # Tło
            
            drawData(data=data, colorArray=colorArray)
            time.sleep(gb.time_tick)

            # --- Pętla przesuwająca elementy (Insertion Sort z odstępem) ---
            while j >= gap:
                gb.porownanie += 1
                if data[j - gap] <= temp:
                    break
                
                # Wizualizacja przed przesunięciem
                colorArray = []
                for x in range(n):
                    if x == j:
                        colorArray.append("yellow")     # Dziura
                    elif x == j - gap:
                        colorArray.append("purple")     # Element za duży, będzie przesunięty
                    elif (x % gap) == (i % gap):
                        colorArray.append("gray")       # Ścieżka
                    else:
                        colorArray.append("white")
                
                drawData(data=data, colorArray=colorArray)
                if not Pauza_Krok(): return None
                time.sleep(gb.time_tick)
                
                # --- Przesunięcie ---
                data[j] = data[j - gap]
                gb.zapisy += 1
                gb.zmiany += 1
                
                # Wizualizacja po przesunięciu (Flash na zielono)
                colorArray[j] = "green" 
                drawData(data=data, colorArray=colorArray)
                time.sleep(gb.time_tick)

                j -= gap
                
                # Aktualizacja metryk
                czas = time.time() - gb.czas_startu
                update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
                
            # --- Wstawienie elementu na właściwe miejsce ---
            data[j] = temp
            gb.zapisy += 1
            
            # Wizualizacja wstawienia
            colorArray = []
            for x in range(n):
                if x == j:
                    colorArray.append("green")  # Wstawiony element (sukces)
                elif (x % gap) == (i % gap):
                    colorArray.append("gray")
                else:
                    colorArray.append("white")

            drawData(data=data, colorArray=colorArray)
            if not Pauza_Krok(): return None
            time.sleep(gb.time_tick)

            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
            
        gap //= 2
    
    # --- Finał: Cała tablica na zielono ---
    drawData(data=data, colorArray=["green" for x in range(len(data))])
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
