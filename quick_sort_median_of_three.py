import time
import globalne_zmienne as gb
from globalne_zmienne import Pauza_Krok

       
start_czasu = time.time()

# ---- zalozenie szybksoci ----
# czas przy ktorym niema animacji 3 kand/ wybora meidany/ wybranego pivota
czas_niema_anim = 0.5

def partition(*, data, head, tail, drawData , update_Matryki):
    mid = (head + tail) // 2
    a = data[head]
    b = data[mid]
    c = data[tail]
    
    # ---- 3 Kandydaty head/mid/tail ----
    if gb.time_tick >= czas_niema_anim:
        drawData(
            data=data,
            colorArray=[
                "purple" if i in (head, mid, tail) else
                "gray" if head <= i <= tail else "white"
                for i in range(len(data))
            ]
        )
    if not Pauza_Krok():
        return None
    if not gb.Czekaj():
        return None
        


    # wybór mediany
    if (a <= b <= c) or (c <= b <= a):
        pivot_index = mid
    elif (b <= a <= c) or (c <= a <= b):
        pivot_index = head
    else:
        pivot_index = tail
    
    gb.porownanie += 3 # dodajem porownanie
    
    # ---- Wybrany pivot "Pink" ----
    if gb.time_tick >= czas_niema_anim:
        drawData(
            data=data,
            colorArray=[
                "pink" if i == pivot_index else
                "purple" if i in (head, mid, tail) else
                "gray" if head <= i <= tail else "white"
                for i in range(len(data))
            ]
        )
    if not Pauza_Krok():
        return None
    if not gb.Czekaj():
        return None


    #  ---- Swap pivota "Green" kolor ---- 
    if gb.time_tick >= czas_niema_anim:
        drawData(
            data=data,
            colorArray=[
                "green" if i in (pivot_index, tail) else
                "gray" if head <= i <= tail else "white"
                for i in range(len(data))
            ]
        )
    if not Pauza_Krok():
        return None
    if not gb.Czekaj():
        return None

    # przenosimy pivot na koniec (tail)
    data[pivot_index], data[tail] = data[tail], data[pivot_index]

    # -- Metryki --
    gb.zmiany += 1
    gb.zapisy += 3
    # ------------

    # pivot bedzie koncowym/ border poczatek
    pivot = data[tail]
    border = head
    


    drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=border) )
    if not Pauza_Krok():
        return None
    if not gb.Czekaj():
        return None

    for i in range(head, tail):

        # --- Pauza / krok ---
        if not Pauza_Krok():
            return None
        # ------------------

        # --- Aby widziec index kazdy raz ---
        drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex=i, isSwaping=False))
        if not gb.Czekaj():
            return None

        gb.porownanie += 1


        if data[i] < pivot:

            # -- Change Color in the swap -- 
            drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex= i, isSwaping= True) )
            if not Pauza_Krok():
                return None
            if not gb.Czekaj():
                return None

            data[border], data[i] = data[i], data[border]

            # -- Metryki --
            gb.zmiany += 1
            gb.zapisy += 3
            # ------------

            border += 1

            drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex= i) )
            if not Pauza_Krok():
                return None
            if not gb.Czekaj():
                return None

        # -- Aktualizacja metryk --
        czas = time.time() - gb.czas_startu
        update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
        # -- Aktualizacja metryk --

    # --- Swap pivot with border value ---
    drawData(data=data, colorArray=getColorArray(dataLen=len(data), head=head, tail=tail, border=border, currentIndex= tail, isSwaping= True) )
    if not Pauza_Krok():
        return None
    
    if not gb.Czekaj():
        return None
    data[border], data[tail] = data[tail], data[border]

    # -- Finalna Aktualizacja Metryk --
    gb.zmiany += 1
    gb.zapisy += 3
    czas = time.time() - gb.czas_startu
    update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)
    # -- Finalna Aktualizacja Metryk --

    return border


def quick_sort_median_of_three(*,data, head, tail, drawData, update_Matryki):

   # Pauza / krok   
    if not Pauza_Krok():
        return None

    if head < tail: # Stop candition

        partitionIndex = partition(data=data, head=head, tail=tail,drawData=drawData, update_Matryki=update_Matryki)

        # Pauza / krok
        if not Pauza_Krok():
            return None

        # --- Jesli zatrzymano przez reset stop ---
        if partitionIndex is None:
            return None

        # --- Left partition ---
        # Pauza / krok
        if not Pauza_Krok():
            return None
        quick_sort_median_of_three(data=data, head=head, tail=partitionIndex - 1, drawData=drawData, update_Matryki=update_Matryki)  # partitionIndex - 1 to not include border value

        # --- Right partition ---
        # Pauza / krok
        if not Pauza_Krok():
            return None
        quick_sort_median_of_three(data=data, head=partitionIndex + 1, tail=tail, drawData=drawData, update_Matryki=update_Matryki)

        if head == 0 and tail == len(data) -1 and not gb.stop_signal:
            drawData(data=data, colorArray=["green" for x in range(len(data))])
            czas = time.time() - gb.czas_startu
            update_Matryki(porownanie=gb.porownanie, zmiany=gb.zmiany, zapisy=gb.zapisy, czas=czas)



def getColorArray(dataLen, head, tail, border, currentIndex, isSwaping = False):
    collorArray = []
    for i in range(dataLen):
        #Base Coloring
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
            if i != currentIndex:     # -- currentIndex zostaje zolty --
                collorArray[i] = "green"

        #  -- Current index ma najwyższy priorytet --
        if i == currentIndex:
            collorArray[i] = "yellow"

    return collorArray
