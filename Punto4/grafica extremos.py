import matplotlib.pyplot as plt
import numpy as np

# Tus datos
tokens = [1, 3, 5, 11, 21, 41, 61, 81, 101, 151, 201, 301, 401]

# Tiempos CYK (en segundos)
tiempos_cyk = [0.0001278999843634665, 5.030003376305103e-05, 7.830001413822174e-05, 0.0005504000000655651, 0.00227419997099787, 0.017640499980188906, 0.05172260000836104, 0.12070249998942018, 0.2395618999726139, 0.7878162999986671, 1.8483030999777839, 6.188974999997299, 14.499899899994489]
# Tiempos LL(1) (aproximados según tus resultados anteriores - ajusta según tus datos reales)
tiempos_ll1 = [0.0036429999745450914, 0.00025209999876096845, 0.0002025999710895121, 0.0001601999974809587, 0.00014259997988119721, 0.00023909995798021555, 0.00021949998335912824, 0.00023769994731992483, 0.00025370001094415784, 0.00033569999504834414, 0.0004290000069886446, 0.0005299999611452222, 0.0006976000149734318]
# Crear figura con 3 subplots
fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))

# ============ GRÁFICO 1: Comparación Directa ============
ax1.plot(tokens, tiempos_ll1, 'o-', label='LL(1)', linewidth=2, markersize=8, color='green')
ax1.plot(tokens, tiempos_cyk, 's-', label='CYK', linewidth=2, markersize=8, color='red')
ax1.set_xlabel('Número de Tokens', fontsize=12)
ax1.set_ylabel('Tiempo (segundos)', fontsize=12)
ax1.set_title('Rendimiento: LL(1) vs CYK', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

