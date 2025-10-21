# ejemplo_inocuo.py — demuestra efecto cache vs RAM (ejecuta localmente)
import time
import random

N = 5_000_000
a = bytearray(N)
indices = [0, N//4, N//2, 3*N//4, N-1]

def access(i):
    # una lectura simple
    return a[i]

# "calentamos" (ponemos en cache) un índice concreto:
calentar = indices[2]
# Leer muchas veces para asegurar que la línea está en cache
for _ in range(1000):
    _ = access(calentar)

# luego medimos tiempo de acceso a cada índice (100 iteraciones)
for idx in indices:
    t0 = time.perf_counter()
    for _ in range(100):
        _ = access(idx)
    t1 = time.perf_counter()
    print(f"index {idx}: {(t1-t0)/100:.9f} s por acceso (media)")

# Observa: el índice que "calentaste" suele tener menor tiempo por acceso.
