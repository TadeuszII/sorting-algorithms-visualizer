import time
pauza = False      # Pause/resume
krok = False       # Single-step
tryb_krokowy = False  # Step mode
stop_signal = False  # Rese t/stop sorting
sortowanie = False   # Is sorting running?

# Metrics
porownanie = 0
zmiany = 0
zapisy = 0
czas_startu = 0.0

time_tick = 0.0


def Pauza_Krok():
    global pauza, krok, tryb_krokowy, stop_signal, sortowanie, czas_startu
    if stop_signal:
        return None

    if pauza or tryb_krokowy:
        start_pause = time.time() # Start Timera
        while (pauza or tryb_krokowy) and not krok:
            time.sleep(0.05)
            if stop_signal:
                return None

        pause_duration = time.time() - start_pause
        czas_startu += pause_duration

    if krok:
        krok = False
    if stop_signal:
        return None
    return True


def Czekaj():
    global czas_startu
    if stop_signal:
        return False
    if tryb_krokowy:
        return True

    koniec = time.time() + time_tick
    while time.time() < koniec:
        if stop_signal:
            return False
        if pauza or tryb_krokowy:
            return Pauza_Krok() is not None
        time.sleep(min(0.05, max(0, koniec - time.time())))

    return True
