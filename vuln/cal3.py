# spectre_simulation_safe.py
# Simulación didáctica de la estructura lógica de un ataque Spectre.
# NO explota sistemas, NO intenta leer memoria ajena. Solo usa datos locales.
#
# Ejecuta localmente para ver la idea: "entrenar -> provocar -> medir".
# Esta versión *simula* la acción especulativa de forma explícita
# (no usa mecanismos reales de speculative execution).

import time
import statistics

# ------------------------------
# Configuración / "memoria"
# ------------------------------
PAGE = 4096
PROBE_PAGES = 256
PROBE_SIZE = PROBE_PAGES * PAGE
probe_array = bytearray(PROBE_SIZE)          # array de sondeo (inocuo)
secret_data = b"password123"                 # datos secretos *locales* (tu control)
secret_bytes = list(secret_data)             # lista de bytes del secreto

# ------------------------------
# Función "vulnerable" (simulada)
# ------------------------------
def vulnerable_function(index):
    """
    Simulación segura: en la realidad la CPU podría especular y ejecutar el
    acceso incluso si 'index' fuera inválido. Aquí, para mostrar la idea,
    hacemos lo siguiente *solo dentro del proceso*:
      - si index es válido, leemos secret_bytes[index] y accedemos a probe_array
      - si index es inválido, NO intentamos leer mem. ajena; en la simulación
        podemos opcionalmente simular un acceso especulativo forzado para demostrar
        el mecanismo de huella (pero solo sobre secret_bytes locales).
    """
    # Lectura "legal"
    if 0 <= index < len(secret_bytes):
        sv = secret_bytes[index]
        # acceder a la posición del probe para "dejar huella"
        _ = probe_array[sv * PAGE]
    else:
        # Simulación didáctica de lo que pasaría "speculativamente":
        # NO hacemos lecturas fuera de rango reales; simulamos la huella
        # escogiendo un valor con criterio controlado (p. ej. 0).
        # Esta rama *no* lee memoria de otros procesos ni del kernel.
        sv = 0
        _ = probe_array[sv * PAGE]

# ------------------------------
# Entrenamiento del predictor (simulado)
# ------------------------------
def train_branch_predictor(rounds=100):
    # Llamamos la función con índices válidos muchas veces
    for _ in range(rounds):
        vulnerable_function(0)  # índice válido repetido

# ------------------------------
# Medición de tiempos (simple)
# ------------------------------
def measure_probe_time(page_index):
    """Mide acceso al comienzo de la página page_index (en ns)."""
    idx = page_index * PAGE
    t0 = time.perf_counter_ns()
    _ = probe_array[idx]
    t1 = time.perf_counter_ns()
    return t1 - t0

# ------------------------------
# Proceso completo de la "simulación de ataque"
# ------------------------------
def spectre_simulation_demo():
    print("=== SIMULACIÓN DIDÁCTICA (SEGURA) DE SPECTRE ===")
    print("Secret (local):", secret_data.decode())
    print("---- Entrenando predictor (simulado) ----")
    train_branch_predictor(200)

    # Limpiar "probe_array" (poner ceros) — no es flush de cache real, solo conceptual
    for i in range(PROBE_PAGES):
        probe_array[i * PAGE] = 0

    # Provocar la "ejecución especulativa" simulada para byte 0 del secreto
    # En la vida real esto intentaría acceder fuera de límites en tiempo especulativo.
    # Aquí llamamos a vulnerable_function con el índice que queremos "leer".
    vulnerable_function(0)  # intentamos leer el primer byte del secreto

    # Medimos tiempos de acceso a todas las páginas "probe"
    timings = []
    for i in range(PROBE_PAGES):
        t = measure_probe_time(i)
        timings.append((i, t))

    # Ordenar por tiempo (rápido primero)
    timings.sort(key=lambda x: x[1])

    print("\nTop 6 páginas más rápidas (posibles huellas):")
    for i, (page, t) in enumerate(timings[:6]):
        char = chr(page) if 32 <= page < 127 else f"0x{page:02x}"
        print(f"{i+1:2d}. page {page:3d}  char: {char:>4}  time: {t} ns")

    print("\nNota: la página correspondiente al primer byte del secreto "
          f"es {secret_bytes[0]} ('{chr(secret_bytes[0])}').\n")

if __name__ == "__main__":
    spectre_simulation_demo()
