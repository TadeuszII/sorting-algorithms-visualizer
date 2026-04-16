import time
pauza = False      # Pause/resume
krok = False       # Single-step
stop_signal = False  # Rese t/stop sorting
sortowanie = False   # Is sorting running?

# Metrics
porownanie = 0
zmiany = 0
zapisy = 0
czas_startu = 0.0

time_tick = 0.0


def Pauza_Krok():
    global pauza, krok, stop_signal, sortowanie, czas_startu
    while pauza and not krok:
        start_pause = time.time() # Start Timera
        time.sleep(0.1)
        if stop_signal: return None
        
        # Za kazdym razym pozwala sprawdzac stop_signal
        while pauza and not krok:
             time.sleep(0.1)
             if stop_signal: return None
        
        # Oblicza wilie uzytkownik byl w pauzie aby ten czas wzrocic
        pause_duration = time.time() - start_pause
        czas_startu += pause_duration

    if krok:
        krok = False
    if stop_signal:
        return None
    return True
