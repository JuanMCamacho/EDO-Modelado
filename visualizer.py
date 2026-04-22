# visualizer.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

def graficar_estatico(t, T, Ta):
    """Genera y guarda la gráfica estática de la simulación."""
    plt.figure(figsize=(8, 5))
    plt.plot(t, T, label='Temperatura del objeto $T(t)$', color='blue', linewidth=2)
    plt.axhline(y=Ta, color='red', linestyle='--', label=f'Temperatura ambiente ($T_a = {Ta}$)')
    
    plt.title('Simulación: Enfriamiento de Newton')
    plt.xlabel('Tiempo')
    plt.ylabel('Temperatura')
    plt.legend()
    plt.grid(True)
    plt.savefig('grafica_enfriamiento.png')
    plt.close()
    print("Gráfica estática guardada como 'grafica_enfriamiento.png'")

def generar_gif(t, T, Ta, nombre_archivo='animacion_enfriamiento.gif'):
    """Genera una animación GIF del proceso de enfriamiento."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    ax.set_xlim(0, max(t))
    ax.set_ylim(min(Ta) - 5 if isinstance(Ta, np.ndarray) else Ta - 5, max(T) + 5)
    ax.set_title('Animación: Proceso de Enfriamiento')
    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Temperatura')
    ax.grid(True)
    
    # Elementos de la gráfica que se actualizarán
    linea_temp, = ax.plot([], [], color='blue', linewidth=2, label='$T(t)$')
    linea_amb = ax.axhline(y=Ta, color='red', linestyle='--', label='$T_a$')
    punto, = ax.plot([], [], 'bo') # Un punto azul que sigue la curva
    
    ax.legend()

    def init():
        linea_temp.set_data([], [])
        punto.set_data([], [])
        return linea_temp, punto

    def update(frame):
        # Tomamos los datos hasta el frame actual para animar el trazo
        linea_temp.set_data(t[:frame], T[:frame])
        # Actualizamos la posición del punto guía
        punto.set_data([t[frame]], [T[frame]])
        return linea_temp, punto

    # Reducimos los frames para que el GIF no sea demasiado pesado
    frames_animacion = np.linspace(0, len(t)-1, 100, dtype=int)
    
    ani = FuncAnimation(fig, update, frames=frames_animacion, init_func=init, blit=True)
    
    # Guardar usando Pillow
    writer = PillowWriter(fps=15)
    ani.save(nombre_archivo, writer=writer)
    plt.close()
    print(f"Animación guardada como '{nombre_archivo}'")