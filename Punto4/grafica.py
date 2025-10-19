import matplotlib.pyplot as plt
import numpy as np

# Tus datos
tokens = [1, 3, 5, 7]

# Tiempos CYK (en segundos)
tiempos_cyk =[0.0002722999779507518, 0.0002452000044286251, 0.00022310001077130437, 0.0006474999827332795]
# Tiempos LL(1) (aproximados según tus resultados anteriores - ajusta según tus datos reales)
tiempos_ll1 = [0.004070200026035309, 0.00016690004849806428, 0.00014840002404525876, 0.00012959999730810523]

# Crear figura con 3 subplots
fig, ax1 = plt.subplots(1, 1, figsize=(6, 5))

# ============ GRÁFICO 1: Comparación Directa ============
ax1.plot(tokens, tiempos_ll1, 'o-', label='LL(1)', linewidth=2, markersize=8, color='green')
ax1.plot(tokens, tiempos_cyk, 's-', label='CYK', linewidth=2, markersize=8, color='red')
ax1.set_xlabel('Número de Tokens', fontsize=12)
ax1.set_ylabel('Tiempo (segundos)', fontsize=12)
ax1.set_title('LL(1) vs CYK', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

