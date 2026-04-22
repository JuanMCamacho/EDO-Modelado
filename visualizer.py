# visualizer.py
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


PLOT_STYLE = {
    "figure_bg": "#252A31",
    "axes_bg": "#21262D",
    "text": "#E6EDF3",
    "grid": "#4B5563",
    "spine": "#6B7280",
    "numeric": "#4EA1FF",
    "analytic": "#66D19E",
    "ambient": "#FF7B72",
    "legend_bg": "#252A31",
    "legend_edge": "#4B5563",
}


def _ruta_salida(nombre_archivo, output_dir):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path / nombre_archivo


def _estilizar_ejes(fig, ax):
    fig.patch.set_facecolor(PLOT_STYLE["figure_bg"])
    ax.set_facecolor(PLOT_STYLE["axes_bg"])
    ax.tick_params(colors=PLOT_STYLE["text"])
    ax.xaxis.label.set_color(PLOT_STYLE["text"])
    ax.yaxis.label.set_color(PLOT_STYLE["text"])
    ax.title.set_color(PLOT_STYLE["text"])
    ax.grid(True, color=PLOT_STYLE["grid"], alpha=0.35, linewidth=0.8)
    for spine in ax.spines.values():
        spine.set_color(PLOT_STYLE["spine"])


def _estilizar_leyenda(legend):
    legend.get_frame().set_facecolor(PLOT_STYLE["legend_bg"])
    legend.get_frame().set_edgecolor(PLOT_STYLE["legend_edge"])
    for text in legend.get_texts():
        text.set_color(PLOT_STYLE["text"])


def graficar_estatico(
    t,
    T,
    Ta,
    nombre_archivo="grafica_enfriamiento.png",
    output_dir="resultados",
):
    """Genera y guarda la grafica estatica de la simulacion."""
    ruta_archivo = _ruta_salida(nombre_archivo, output_dir)

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=PLOT_STYLE["figure_bg"])
    ax.plot(t, T, label="Temperatura del objeto T(t)", color=PLOT_STYLE["numeric"], linewidth=2.2)
    ax.axhline(
        y=Ta,
        color=PLOT_STYLE["ambient"],
        linestyle="--",
        linewidth=1.8,
        label=f"Temperatura ambiente Ta={Ta:.2f}",
    )
    ax.set_title("Ley de Enfriamiento de Newton")
    ax.set_xlabel("Tiempo (min)")
    ax.set_ylabel("Temperatura (grados C)")
    _estilizar_ejes(fig, ax)
    legend = ax.legend()
    _estilizar_leyenda(legend)

    fig.tight_layout()
    fig.savefig(ruta_archivo, dpi=140, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"Grafica estatica guardada en: {ruta_archivo}")
    return str(ruta_archivo)


def generar_gif(
    t,
    T,
    Ta,
    nombre_archivo="animacion_enfriamiento.gif",
    output_dir="resultados",
):
    """Genera una animacion GIF dinamica del proceso de enfriamiento."""
    ruta_archivo = _ruta_salida(nombre_archivo, output_dir)

    y_min = min(float(np.min(T)), float(Ta)) - 5.0
    y_max = max(float(np.max(T)), float(Ta)) + 5.0
    cmap = plt.get_cmap("coolwarm")
    norm = plt.Normalize(vmin=y_min, vmax=y_max)

    fig, ax = plt.subplots(figsize=(8, 5), facecolor=PLOT_STYLE["figure_bg"])
    ax.set_xlim(0.0, float(np.max(t)))
    ax.set_ylim(y_min, y_max)
    ax.set_title("Animacion del Proceso de Enfriamiento")
    ax.set_xlabel("Tiempo (min)")
    ax.set_ylabel("Temperatura (grados C)")
    _estilizar_ejes(fig, ax)

    linea_temp, = ax.plot([], [], linewidth=2.2, color=PLOT_STYLE["numeric"], label="T(t)")
    ax.axhline(y=Ta, color=PLOT_STYLE["ambient"], linestyle="--", linewidth=1.8, label="Ta")
    punto, = ax.plot([], [], marker="o", markersize=7)
    legend = ax.legend(loc="best")
    _estilizar_leyenda(legend)

    def init():
        linea_temp.set_data([], [])
        punto.set_data([], [])
        punto.set_color(PLOT_STYLE["numeric"])
        return linea_temp, punto

    def update(frame_index):
        idx = int(frame_index)
        linea_temp.set_data(t[: idx + 1], T[: idx + 1])
        punto.set_data([t[idx]], [T[idx]])

        color_actual = cmap(norm(T[idx]))
        linea_temp.set_color(color_actual)
        punto.set_color(color_actual)
        return linea_temp, punto

    total_frames = min(120, len(t))
    frames_animacion = np.linspace(0, len(t) - 1, total_frames, dtype=int)
    ani = FuncAnimation(fig, update, frames=frames_animacion, init_func=init, blit=True)

    ani.save(ruta_archivo, writer=PillowWriter(fps=15))
    plt.close(fig)

    print(f"Animacion guardada en: {ruta_archivo}")
    return str(ruta_archivo)