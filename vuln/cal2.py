# prueba_cache_corregida.py
import time, random, statistics

N = 6_000_000
a = bytearray(N)
indices = [0, N//4, N//2, 3*N//4, N-1]
TARGET = indices[2]   # índice que queremos calentar

def timed_read(idx):
    t0 = time.perf_counter_ns()
    _ = a[idx]
    t1 = time.perf_counter_ns()
    return t1 - t0

def evict_cache():
    # leer un buffer grande para "ensuciar" caches (evict)
    tmp = bytearray(N//2)
    for i in range(0, len(tmp), 4096):
        _ = tmp[i]

# repetimos muchas veces para obtener estadística
SAMPLES = 300
samples = {idx: [] for idx in indices}

for _ in range(SAMPLES):
    evict_cache()                      # 1) eviction primero
    # 2) calentar objetivo (varias lecturas seguidas)
    for i in range(2000):
        _ = a[TARGET]
    # 3) medir (en orden aleatorio para reducir prefetch bias)
    order = indices[:]
    random.shuffle(order)
    for idx in order:
        samples[idx].append(timed_read(idx))

# mostrar resultados: mediana y media
for idx in indices:
    med = statistics.median(samples[idx])
    mean = statistics.mean(samples[idx])
    stdev = statistics.pstdev(samples[idx])
    print(f"index {idx}: mediana {med} ns, media {mean:.1f} ns, stdev {stdev:.1f} ns")
