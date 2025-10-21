# medida_cache_mejorada.py  — ejecutar local y observar diferencias
import time
import random
import statistics

N = 6_000_000
a = bytearray(N)
indices = [0, N//4, N//2, 3*N//4, N-1]

# FUNC: realizar una sola lectura y devolver tiempo en ns
def timed_read(idx):
    t0 = time.perf_counter_ns()
    _ = a[idx]
    t1 = time.perf_counter_ns()
    return t1 - t0

# "calentar" una posición: leerla muchas veces
calentar = indices[2]   # la que queremos poner en cache
for _ in range(5000):
    _ = a[calentar]

# opción: "ensuciar" la cache para forzar que otras líneas no estén calientes
# leer un montón de memoria extensa (eviction)
tmp = bytearray(N//2)
for i in range(0, len(tmp), 4096):
    _ = tmp[i]

# medir cada índice muchas veces en orden aleatorio y tomar mediana
samples = {idx: [] for idx in indices}
for _ in range(200):
    order = indices[:] 
    random.shuffle(order)
    for idx in order:
        samples[idx].append(timed_read(idx))

# mostrar mediana y desviación
for idx in indices:
    med = statistics.median(samples[idx])
    mean = statistics.mean(samples[idx])
    stdev = statistics.pstdev(samples[idx])
    print(f"index {idx}: mediana {med} ns, media {mean:.1f} ns, stdev {stdev:.1f} ns")
