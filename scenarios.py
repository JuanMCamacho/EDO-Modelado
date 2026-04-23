# escenarios.py
from pathlib import Path
import matplotlib.pyplot as plt
from solver import simular_enfriamiento

# Usamos la misma paleta oscura de su visualizer.py para mantener coherencia
PLOT_STYLE = {
    "figure_bg": "#252A31",
    "axes_bg": "#21262D",
    "text": "#E6EDF3",
    "grid": "#4B5563",
}

def generar_comparativa():
    print("Generando análisis de escenarios comparativos...")
    
    # Parámetros base del procesador (Problema original)
    T0 = 20.0
    t_max = 25.0
    dt = 0.5
    
    # ESCENARIO 1: Base (Banco de pruebas a 80°C)
    Ta_1 = 80.0
    k_1 = -0.2310  # Constante negativa como pidió tu profesor
    t1, T1 = simular_enfriamiento(T0, Ta_1, k_1, t_max, dt)

    # ESCENARIO 2: Diferente constante de enfriamiento/calentamiento
    # Simulamos un procesador con un disipador de mejor calidad (k más grande)
    Ta_2 = 80.0
    k_2 = -0.5000 
    t2, T2 = simular_enfriamiento(T0, Ta_2, k_2, t_max, dt)

    # ESCENARIO 3: Diferente temperatura ambiente
    # Simulamos el procesador original, pero en un cuarto con aire acondicionado
    Ta_3 = 25.0
    k_3 = -0.2310
    t3, T3 = simular_enfriamiento(T0, Ta_3, k_3, t_max, dt)

    # --- Configuración de la Gráfica ---
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=PLOT_STYLE["figure_bg"])
    ax.set_facecolor(PLOT_STYLE["axes_bg"])
    
    # Trazar las 3 curvas
    ax.plot(t1, T1, label=f"Escenario Base ($T_a={Ta_1}^\circ C$, $k={k_1}$)", color="#FF7B72", linewidth=2.5)
    ax.plot(t2, T2, label=f"Mejor Disipación ($T_a={Ta_2}^\circ C$, $k={k_2}$)", color="#66D19E", linewidth=2.5)
    ax.plot(t3, T3, label=f"Ambiente Controlado ($T_a={Ta_3}^\circ C$, $k={k_3}$)", color="#4EA1FF", linewidth=2.5)

    # Estilos
    ax.set_title("Análisis Predictivo: Comparativa de Escenarios", color=PLOT_STYLE["text"], fontsize=14, pad=15)
    ax.set_xlabel("Tiempo (min)", color=PLOT_STYLE["text"])
    ax.set_ylabel("Temperatura (°C)", color=PLOT_STYLE["text"])
    ax.tick_params(colors=PLOT_STYLE["text"])
    ax.grid(True, color=PLOT_STYLE["grid"], alpha=0.5, linewidth=0.8)
    
    for spine in ax.spines.values():
        spine.set_color(PLOT_STYLE["grid"])

    legend = ax.legend(loc="best", facecolor=PLOT_STYLE["axes_bg"], edgecolor=PLOT_STYLE["grid"])
    for text in legend.get_texts():
        text.set_color(PLOT_STYLE["text"])

    # Guardar archivo
    output_dir = Path("resultados")
    output_dir.mkdir(parents=True, exist_ok=True)
    ruta_archivo = output_dir / "comparativa_escenarios.png"
    
    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)
    
    print(f"Gráfica comparativa guardada en: {ruta_archivo}")

if __name__ == "__main__":
    generar_comparativa()