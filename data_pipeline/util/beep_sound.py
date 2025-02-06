from time import sleep,perf_counter

from winsound import Beep
def beep_sound():
    time_start = perf_counter()
    while perf_counter() - time_start < 5:
        Beep(2000,500)
        sleep(0.5)