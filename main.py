from tkinter import *
from tkinter import ttk
import random
import time
import threading
from tkinter import PhotoImage
import csv
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# ---- Import algorytmow ----
from Bubble_Sort import bubble_sort
from quicksort import quick_sort
from quick_sort_median_of_three import quick_sort_median_of_three
from cocktail_shaker_sort import cocktail_shaker_sort
from odd_even_sort import odd_even_sort
from gnome_sort import gnome_sort
from bitonic_sort import bitonic_sort
from shell_sort import shell_sort
from heap_sort import heap_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from intro_sort import intro_sort
from merge_sort import merge_sort
from bubble_sort_z_flaga import bubble_sort_z_flaga
import globalne_zmienne as gb

import os # ---- For .exe files ----
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ... (other code) ...

# Dla drugich komputerow


#Konstanty WIDTH I HEIGHT
WIDTH =  1600
HEIGHT = 900 
CANVAS_WIDTH = 1250
CANVAS_HEIGHT = 760
UIFRAME_WIDTH = 1500
UIFRAME_HEIGHT = 200
SEPERATOR = "-----------------"


# ---- Glowny ekran ----
root = Tk()
root.title("Wizualizacja Algorytmów Sortowania")
root.maxsize(WIDTH, HEIGHT)

try:
    root.state('zoomed') # Działa w systemie Windows
except TclError:
    pass # Na wypadek uruchomienia na innym systemie


# ---- Variabes ----
# --- Variables dla odbiernia nazw algortymu/nazw wybrany dane dla generacji ---
selected_alg = StringVar()
selected_genMenu = StringVar()

# --- Lista z danymi ---
data = []
kopia_daty = []
sort_locked_widgets = []
sort_locked_comboboxes = []
sort_run_id = 0


# --- Logo uniwersytetu ---
#logo_Uniweretetu = PhotoImage(file=r"C:\Users\taduk\Desktop\Save projektu\Mini Projekt II przedstawinie\Python kod\filia_wilno_logo_kolor.png").subsample(2)
#logo_Uniweretetu = PhotoImage(file=resource_path("filia_wilno_logo_kolor.png")).subsample(2)
logo_Uniweretetu = PhotoImage(file=resource_path("filia_wilno_logo_kolor.png")).subsample(2)




# ---- Funckji i funckji knopek pause/resume/step/reset ----


# --- Przycisk pauzy ---
def pauza_Button():
    
    gb.pauza = not gb.pauza # -- Switch --

    if gb.pauza:
        pass
    else:
        gb.time_tick = speedScale.get() # -- Odbiera danne predkosci s suwaka --


# --- Przycisk kroku ---
def krok_Button():
    gb.krok = True


# --- Przycisk reset ---
def resetuj_Sort_Button():
    global data, kopia_daty, sort_run_id

    # -- zatrzymanie działania algorytmu --
    gb.stop_signal = True
    gb.pauza = False
    gb.krok = False
    gb.sortowanie = False
    sort_run_id += 1

    # -- wyzerowanie metryk --
    gb.zapisy = 0
    gb.zmiany = 0
    gb.czas_startu = 0
    gb.porownanie = 0

    update_Matryki( porownanie=gb.porownanie, zapisy=gb.zapisy, zmiany=gb.zmiany, czas=gb.czas_startu)
    set_sort_controls_locked(False)

    # -- Sprawdzenie czy kopia_daty nie jest pusta --
    if kopia_daty:
        data = kopia_daty.copy()
        drawData(data=data,colorArray=["red" for _ in range(len(data))])


# --- Przycisk delete ---
def delete_Button():
    global data, kopia_daty, sort_run_id

    # -- zatrzymanie działania algorytmu --
    gb.stop_signal = True
    gb.pauza = False
    gb.krok = False
    gb.sortowanie = False
    sort_run_id += 1

    #  -- wyzerowanie metryk --
    gb.zapisy = 0
    gb.zmiany = 0
    gb.czas_startu = 0
    gb.porownanie = 0

    update_Matryki(porownanie=0, zmiany=0, zapisy=0, czas=0)
    set_sort_controls_locked(False)

    # -- CZYSZCZENIE CANVASA --
    canvas.delete("all")

    # -- CZYSZCZENIE DANYCH --
    data = []
    kopia_daty = []

    



# --- Funckja Metryk ---
def update_Matryki(*,porownanie, zmiany, zapisy, czas):
    # -- Odnawia metryki w aplikaci --
    label_porownan.config(text=f"Porownania: {porownanie}")
    label_zamian_i_zapisow.config(text=f"Zamiany/Zapisy: {zmiany+zapisy}")
    label_czasu.config(text=f"Czas: {czas:.3f} s")


def set_sort_controls_locked(locked: bool):
    state = DISABLED if locked else NORMAL
    combo_state = "disabled" if locked else "readonly"

    for widget in sort_locked_widgets:
        widget.config(state=state)

    for widget in sort_locked_comboboxes:
        widget.config(state=combo_state)


def start_sort_thread(target, **extra_kwargs):
    global sort_run_id

    sort_run_id += 1
    current_run_id = sort_run_id

    gb.stop_signal = False
    gb.sortowanie = True
    gb.pauza = False
    gb.krok = False

    gb.porownanie = 0
    gb.zmiany = 0
    gb.zapisy = 0
    gb.czas_startu = time.time()

    set_sort_controls_locked(True)

    kwargs = {
        "data": data,
        "drawData": drawData,
        "update_Matryki": update_Matryki,
        **extra_kwargs
    }

    def sort_runner():
        try:
            target(**kwargs)
        finally:
            def finish_sort():
                if current_run_id != sort_run_id:
                    return

                gb.sortowanie = False
                if not gb.stop_signal:
                    set_sort_controls_locked(False)

            root.after(0, finish_sort)

    threading.Thread(target=sort_runner, daemon=True).start()

# --- Funckja Rysowania ---
def drawData(*, data, colorArray):

    # -- Rysowanie na canvase --
    def draw_tink():
        canvas.delete("all")
        c_height = canvas.winfo_height()
        c_width = canvas.winfo_width()
        x_width = c_width / len(data)
        offset = 0
        spacing = 0
        
        znomrmalizowanaData = [ i / max(data) for i in data] # -- Potrzebne jest aby slupki byli prawidlowo rysowane --

        for i, height in enumerate(znomrmalizowanaData):
            # -- Gorny lewy kat --
            x0 = int(i * x_width + offset + spacing)
            y0 = c_height - height * (c_height - 20)
            # -- Dolny prawy kat --
            x1 = int((i + 1 ) * x_width + offset)
            y1 = c_height

            # -- Sprawdzenie jezeli ilosc dannych jest wieksze niz 50, nie beda wypisywane cyferki z wierchu slopkow
            if len(data) <= 50:  
                canvas.create_text(x0+2, y0, anchor=SW, text=str(data[i]), fill="black") # - SW = South-West -
                canvas.create_rectangle(x0, y0, x1, y1, fill=colorArray[i], outline="black")
            else:
                canvas.create_rectangle(x0, y0, x1, y1,  fill=colorArray[i], outline="")

        # -- Animacji --
        root.update_idletasks() # - Natychmiast narysuje zmiany odnawia tylko rysowanie GUI -
    
    root.after(0, draw_tink)  # - bez tej funckji GUI by zawiesil sie wrzuca NOWE narysowanie slupkow do glownego watku GUI

# --- Funckja generacja/ Przycisk generacji ---
def Generate(): 
    global data
    global kopia_daty
    
    canvas.delete("all")

    minZnaczenie = int(min_Entry.get())
    maxZnaczenie = int(max_Entry.get())
    rozmiar = int(rozmiar_Entry.get())

    typDanych = genMenu.get()

    data = []
    

    # ["Losowe", "Rosnace", "Malejace", "Prawie posortowane"

    # -- Losowe danne --

    match typDanych:
        case "Losowe":
            for _ in range(rozmiar):
                data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
        
        case "Rosnace":
            for _ in range(rozmiar):
                data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
            data = sorted(data)
        
        case "Malejace":
            for _ in range(rozmiar):
                data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
            data = sorted(data, reverse=True)

        case "Prawie posortowane":
            # -- Zapelnia lista random dannymi --
            for _ in range(rozmiar):
                data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
            data = sorted(data) # -- Sortuje danne --
            swaps = max(1, rozmiar // 5) # -- Wilie bedzie swapow --
                
            for _ in range(swaps): # -- Swapuje danne bierzac randomne indexy i meniajac ich miejscami --
                i, j = random.sample(range(rozmiar), 2)
                data[i], data[j] = data[j], data[i]
        
        case "Bez duplikatów":
            if (maxZnaczenie - minZnaczenie + 1) < rozmiar:
                # Calculate new Max needed to fit unique numbers starting from Min
                new_max = minZnaczenie + rozmiar - 1
                
                # Update the variable and the slider UI
                maxZnaczenie = new_max
                max_Entry.set(new_max) # Force update the slider

                # Show info to the user
                showinfo(title="Uwaga", 
                        message=f"Aby wygenerować {rozmiar} unikalnych liczb (bez duplikatów),\n"
                                f"zakres wartości musi być co najmniej równy liczbie elementów.\n\n"
                                f"Automatycznie ustawiono Max wartość na: {new_max}.")
                
                data = random.sample(range(minZnaczenie, maxZnaczenie + 1), rozmiar)

            data = random.sample(range(minZnaczenie, maxZnaczenie + 1), rozmiar)

    # if typDanych == "Losowe":
    #     for _ in range(rozmiar):
    #         data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))

    # # -- Rosnace posortowane --
    # elif typDanych == "Rosnace":
    #     for _ in range(rozmiar):
    #         data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
    #     data = sorted(data)

    # # -- Malejace posortowane --
    # elif typDanych == "Malejace":
    #     for _ in range(rozmiar):
    #         data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
    #     data = sorted(data, reverse=True)

    # # -- Prawie posortowane --
    # elif typDanych == "Prawie posortowane":

    #     # -- Zapelnia lista random dannymi --
    #     for _ in range(rozmiar):
    #         data.append(random.randrange(minZnaczenie, maxZnaczenie + 1))
    #     data = sorted(data) # -- Sortuje danne --
    #     swaps = max(1, rozmiar // 5) # -- Wilie bedzie swapow --

    #     for _ in range(swaps): # -- Swapuje danne bierzac randomne indexy i meniajac ich miejscami --
    #         i, j = random.sample(range(rozmiar), 2)
    #         data[i], data[j] = data[j], data[i]

    # elif typDanych == "Bez duplikatów":
    #     if (maxZnaczenie - minZnaczenie + 1) < rozmiar:
    #         # Calculate new Max needed to fit unique numbers starting from Min
    #         new_max = minZnaczenie + rozmiar - 1
            
    #         # Update the variable and the slider UI
    #         maxZnaczenie = new_max
    #         max_Entry.set(new_max) # Force update the slider

    #         # Show info to the user
    #         showinfo(title="Uwaga", 
    #                  message=f"Aby wygenerować {rozmiar} unikalnych liczb (bez duplikatów),\n"
    #                          f"zakres wartości musi być co najmniej równy liczbie elementów.\n\n"
    #                          f"Automatycznie ustawiono Max wartość na: {new_max}.")
            
    #         data = random.sample(range(minZnaczenie, maxZnaczenie + 1), rozmiar)

    #     data = random.sample(range(minZnaczenie, maxZnaczenie + 1), rozmiar)

    kopia_daty = data.copy() # -- Tworze lista kopia dannych dla przycisku reset --

    drawData(data=data, colorArray=["red" for x in range(len(data))]) # -- Koloruje slupki na czerwone --

# --- Przycisk Open ---
def Open_button():
    global data, kopia_daty


    fileName = fd.askopenfilename(title="Wybierz plik CSV", initialdir="/", filetypes=[("Pliki CSV", "*.csv")]) # -- askopenfilename prosi nazwa file dla odkrycia --
    if not fileName:
        return

    nowa_data = []
    puste_wiersze = 0
    niepoprawne_wiersze = 0
    ujemne_liczby = 0

    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row or not row[0].strip():
                puste_wiersze += 1
                continue

            try:
                liczba = int(row[0])
            except ValueError:
                niepoprawne_wiersze += 1
                continue

            if liczba < 0:
                ujemne_liczby += 1
                continue

            nowa_data.append(liczba)
                
    if puste_wiersze or niepoprawne_wiersze or ujemne_liczby:
        showinfo(title="W wybranym pliku",
                 message=f"Pominięto wiersze:\n"
                         f"Puste: {puste_wiersze}\n"
                         f"Niepoprawne: {niepoprawne_wiersze}\n"
                         f"Liczby ujemne: {ujemne_liczby}")

    if len(nowa_data) < 5: # -- Jezeli dannych jest za malo wyszli komunikat i nic nie zrobi --
        showinfo(title="Wybrany plik", message="Musi być 5 lub więcej elementów!" )
    else: # -- jezeli wszystjo jest dobrze to dane wstawia dane --
        data = nowa_data
        kopia_daty = data.copy()
        drawData(data=data, colorArray=["red" for _ in range(len(data))])

# --- Przycisk Export ---
def Export_button():
    global data
    
    if data: # -- jezeli list data nie jest puste to zapisze do pliku --
        fileName = fd.asksaveasfilename(title="Zapisz plik CSV", initialdir="/", defaultextension=".csv", filetypes=[("Pliki CSV", "*.csv")]) # -- asksaveasfilename prosi nazwa file dla zapisu --
        if not fileName:
            return

        with open(fileName, "w", newline='') as csvfile:
            write = csv.writer(csvfile)

            for liczba in data: # -- zapisuje dane do pliku --
                write.writerow([liczba])
            showinfo(title="Dane", message=f"Dane zostale zapisane do pliku {fileName}" )

    else: # -- jezeli data jest pusta wyswtietli komunikat
        showinfo(title="Dane", message="Niema dannych ktorych mozna zapisac!" )


# --- Funckja Startu algortymu ---
def StartAlgorithm():
    global data

    gb.time_tick = speedScale.get() # -- biora aktualny czas --

    if gb.sortowanie:
        return

    if not data: return # -- jezeli nie zostalo nic sgenerowano nic nie robi --

    match algMenu.get():
        case "Median of three":
            start_sort_thread(quick_sort_median_of_three, head=0, tail=len(data) - 1)

        case "Quick Sort":
            start_sort_thread(quick_sort, head=0, tail=len(data) - 1)
        
        case "Bubble Sort":
            start_sort_thread(bubble_sort)
        
        case "Cocktail Shaker Sort":
            start_sort_thread(cocktail_shaker_sort)

        case "Odd Even Sort":
            start_sort_thread(odd_even_sort)
        
        case "Gnome Sort":
            start_sort_thread(gnome_sort)
        
        case "Bitonic Sort":
            rozmiar = len(data)
            isPowerOfTwo = True
            # -- Jezeli user wybral bitonic sort ale dlugosc daty nie potega 2 --
            if not ( (rozmiar & (rozmiar - 1)) == 0 ):
                isPowerOfTwo = False
                showinfo(title="Ostrzeżenie: Bitonic Sort", message=f"Wybrano rozmiar: {rozmiar}, ale Bitonic Sort\nwymaga, aby liczba elementów była potęgą 2\n (np. 8, 16, 32, 64, 128).\n Próbka zostanie nie poprawnie posortowana" )
            
            start_sort_thread(bitonic_sort, isPowerOfTwo=isPowerOfTwo)

        case "Shell Sort":
            start_sort_thread(shell_sort)
        
        case "Heap Sort":
            start_sort_thread(heap_sort)

        case "Selection Sort":
            start_sort_thread(selection_sort)

        case "Insertion Sort":
            start_sort_thread(insertion_sort)
        
        case "Intro Sort":
            start_sort_thread(intro_sort)

        case "Merge Sort":
            start_sort_thread(merge_sort)

        case "Bubble Sort Flag":
            start_sort_thread(bubble_sort_z_flaga)

        case SEPERATOR:
            showinfo(title="Uwaga", message=f"Nie można wybrać seperator jako algortym do sortowania")
            
root.grid_columnconfigure(1, weight=1) # ---- Canvas ma sie rozciagnac gdy okno zostanie zmienione ----
root.grid_rowconfigure(0, weight=1)  # ---- Sidebar ma sie rozciagnac gdy okno zostanie zmienione ----

# ----- Design UI -----

root.config(bg="white") # ---- Kolor backgroundu  ----

# ---- Lewy bar gdzie beda buttons/metryki/wybor algorytmu ----
sidebar = Frame(root, width=200, bg="white", padx=10, pady=10)
sidebar.grid(row=0, column=0, rowspan=2, sticky="nsw")

# ---- LOGO Uniwerstyteta ----
logo_label = Label(sidebar, image=logo_Uniweretetu, bg="white")
logo_label.grid(row=0, column=0, columnspan=2, pady=(0,15))

# ---- Menu Algorytmow ----

Label(sidebar, text="Algorytm:", bg="white", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
algMenu = ttk.Combobox(sidebar, state="readonly", textvariable=selected_alg, values=["Intro Sort", "Bitonic Sort", "Merge Sort", "Heap Sort", "Quick Sort", "Median of three", "Shell Sort", SEPERATOR, "Insertion Sort", "Selection Sort", "Gnome Sort", "Bubble Sort", "Bubble Sort Flag", "Cocktail Shaker Sort", "Odd Even Sort"], width=18)
algMenu.grid(row=2, column=0, columnspan=2, pady=4)
algMenu.current(0)

# ---- Menu Generacji
genMenu = ttk.Combobox(sidebar, state="readonly", textvariable=selected_genMenu, values=["Losowe", "Rosnace", "Malejace", "Prawie posortowane", "Bez duplikatów"], width=18)
genMenu.grid(row=16, column=0, columnspan=1, pady=10)
genMenu.current(0)



# ---- Przyciski/Buttons ---- 
# --- Styl przyciskow ---
styl_przycisku = {
    "width": 14,
    "height": 1,
    "font": ("Arial", 9, "bold"),
    "bg": "white",
    "bd": 1,
    "relief": "solid"
}

styl_przycisku2 = {
    "width": 5,
    "height": 1,
    "font": ("Arial", 9, "bold"),
    "bg": "white",
    "bd": 1,
    "relief": "solid"
}

# -- Przyciski/Buttons--
start_button = Button(sidebar, text="Start", command=StartAlgorithm, **styl_przycisku)
start_button.grid(row=5, column=0, columnspan=2, pady=(10,4)) # - Start -
pause_button = Button(sidebar, text="Stop / Wznow", command=pauza_Button, **styl_przycisku)
pause_button.grid(row=6, column=0, columnspan=2, pady=4) # - Pauza/wznow -
step_button = Button(sidebar, text="Krok", command=krok_Button, **styl_przycisku)
step_button.grid(row=7, column=0, columnspan=2, pady=4) # - Krok -
reset_button = Button(sidebar, text="Reset", command=resetuj_Sort_Button, **styl_przycisku)
reset_button.grid(row=8, column=0, columnspan=2, pady=4, padx=4) # - Reset -
delete_button = Button(sidebar, text="Delete", command=delete_Button, **styl_przycisku2)
delete_button.grid(row=8, column=1, columnspan=2, pady=4, padx=4) # - Delete -
generate_button = Button(sidebar, text="Generuj", command=Generate, **styl_przycisku)
generate_button.grid(row=15, column=0, columnspan=1, pady=5) # - Generuj -
open_button = Button(sidebar, text="Open", command=Open_button, **styl_przycisku2)
open_button.grid(row=15, column=1, columnspan=1, pady=5) # - Open -
export_button = Button(sidebar, text="Export", command=Export_button, **styl_przycisku2)
export_button.grid(row=16, column=1, columnspan=1, pady=10) # - Open -
# ---- /Przyciski ---- 

# ---- Suwaki dla Predskoc/Liczb Elementow[n]/Min wartosc elementa/Min wartosc elementa ----

# --- Styl Suwakow
font_teksta_suwaka = { "font": ("Arial", 9, "bold"), "bg": "white", }

# -- Predkosc --
Label(sidebar, text="Prędkość [s]:", **font_teksta_suwaka).grid(row=3, column=0, sticky="w", pady=(10,0))
speedScale = Scale(sidebar, from_=0.01, to=5.0, length=170, digits=2, resolution=0.01, orient=HORIZONTAL, bg="white")
speedScale.grid(row=4, column=0, columnspan=2, pady=4)

# -- Rozmiar Elementow[n] --
Label(sidebar, text="Liczba elementów [n]:", **font_teksta_suwaka).grid(row=9, column=0, sticky="w", pady=(10,0))
rozmiar_Entry = Scale(sidebar, from_=5, to=1000, length=170, resolution=1,orient=HORIZONTAL, bg="white")
rozmiar_Entry.grid(row=10, column=0, columnspan=2, pady=3)

# -- Minimalna wartosc Elementow --
Label(sidebar, text="Min wartość:", **font_teksta_suwaka).grid(row=11, column=0, sticky="w")
min_Entry = Scale(sidebar, from_=0, to=10, length=170, resolution=1,orient=HORIZONTAL, bg="white")
min_Entry.grid(row=12, column=0, columnspan=2, pady=3)

# -- Maksymalna wartosc Elementow --
Label(sidebar, text="Max wartość:", **font_teksta_suwaka).grid(row=13, column=0, sticky="w")
max_Entry = Scale(sidebar, from_=10, to=1000, length=170, resolution=1, orient=HORIZONTAL, bg="white")
max_Entry.grid(row=14, column=0, columnspan=2, pady=3)
sort_locked_widgets = [start_button, generate_button, open_button, export_button, rozmiar_Entry, min_Entry, max_Entry]
sort_locked_comboboxes = [algMenu, genMenu]
# --- /Suwaki dla Liczb Elementow[n]/Min wartosc elementa/Min wartosc elementa ---



# ----METRYKI----

font_teksta_metryk = { "font": ("Arial", 9, "bold"), "bg": "white", }

Label(sidebar, text="METRYKI:", **font_teksta_metryk).grid(row=17, column=0, columnspan=2, pady=(15,5)) # - Tekst "Metryki" -
label_porownan = Label(sidebar, text="Porównania: 0", **font_teksta_metryk) # - Porownanie -
label_zamian_i_zapisow = Label(sidebar, text="Zamiany/zapisy: 0", **font_teksta_metryk) # - zmian/zapisow -
label_czasu = Label(sidebar, text="Czas: 0.00 s", **font_teksta_metryk) # - Czas -

label_porownan.grid(row=18, column=0, sticky="w")
label_zamian_i_zapisow.grid(row=19, column=0, sticky="w")
label_czasu.grid(row=20, column=0, sticky="w")
# ---- /METRYKI ----

# --- Canvas ---

canvas = Canvas(root, bg="#B9B9B9", highlightthickness=0)
canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# --- /Canvas ---

root.mainloop()
