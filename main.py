import tkinter.messagebox as messagebox

import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from solver import calcular_constante_k, simular_enfriamiento, solucion_analitica
from visualizer import generar_gif, graficar_estatico


class NewtonCoolingCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculadora - Ley de Enfriamiento de Newton")
        self.geometry("1200x760")
        self.minsize(980, 640)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.entries = {}
        self.canvas = None

        self._build_ui()

    def _build_ui(self):
        form_panel = ctk.CTkFrame(self, corner_radius=12)
        form_panel.grid(row=0, column=0, padx=16, pady=16, sticky="ns")

        content_panel = ctk.CTkFrame(self, corner_radius=12)
        content_panel.grid(row=0, column=1, padx=(0, 16), pady=16, sticky="nsew")
        content_panel.columnconfigure(0, weight=1)
        content_panel.rowconfigure(1, weight=1)

        ctk.CTkLabel(
            form_panel,
            text="Datos del modelo",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w", padx=18, pady=(18, 10))

        self._create_field(form_panel, "T0", "Temperatura inicial (grados C)")
        self._create_field(form_panel, "Ta", "Temperatura ambiente (grados C)")
        self._create_field(form_panel, "t_med", "Tiempo de medicion t (min)")
        self._create_field(form_panel, "T_med", "Temperatura medida T(t) (grados C)")
        self._create_field(form_panel, "t_max", "Tiempo total de simulacion (min)")
        self._create_field(form_panel, "dt", "Paso de tiempo dt (min)")

        btn_calcular = ctk.CTkButton(
            form_panel,
            text="Calcular y simular",
            height=40,
            command=self.calcular,
        )
        btn_calcular.pack(fill="x", padx=18, pady=(16, 8))

        btn_limpiar = ctk.CTkButton(
            form_panel,
            text="Limpiar",
            height=40,
            fg_color="#4A4A4A",
            hover_color="#3A3A3A",
            command=self.limpiar,
        )
        btn_limpiar.pack(fill="x", padx=18, pady=(0, 18))

        

        ctk.CTkLabel(
            content_panel,
            text="Resultados",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8))

        panel_bg = content_panel.cget("fg_color")
        self.plot_frame = ctk.CTkFrame(
            content_panel,
            fg_color=panel_bg,
            corner_radius=0,
            border_width=0,
        )
        self.plot_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 10))
        self.plot_frame.rowconfigure(0, weight=1)
        self.plot_frame.columnconfigure(0, weight=1)

        self.output_box = ctk.CTkTextbox(content_panel, height=180, wrap="word")
        self.output_box.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        self.output_box.insert("1.0", "Ingresa los datos y presiona 'Calcular y simular'.")
        self.output_box.configure(state="disabled")

        self._sync_output_box_style()

    def _create_field(self, parent, key, label):
        ctk.CTkLabel(parent, text=label).pack(anchor="w", padx=18, pady=(6, 3))
        entry = ctk.CTkEntry(parent, width=300)
        entry.pack(fill="x", padx=18, pady=(0, 4))
        self.entries[key] = entry

    def _get_float(self, key, label):
        value_raw = self.entries[key].get().strip().replace(",", ".")
        if not value_raw:
            raise ValueError(f"Completa el campo: {label}.")
        try:
            return float(value_raw)
        except ValueError as exc:
            raise ValueError(f"Valor invalido en {label}: '{value_raw}'.") from exc

    def _set_output_text(self, text):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(state="disabled")

    def _to_hex_color(self, color_value, fallback="#2B2B2B"):
        try:
            r16, g16, b16 = self.winfo_rgb(color_value)
            r, g, b = r16 // 257, g16 // 257, b16 // 257
            return f"#{r:02X}{g:02X}{b:02X}"
        except Exception:
            return fallback

    def _lighten_hex(self, hex_color, amount=0.1):
        amount = max(0.0, min(1.0, amount))
        if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) != 7:
            return hex_color

        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        r = int(r + (255 - r) * amount)
        g = int(g + (255 - g) * amount)
        b = int(b + (255 - b) * amount)
        return f"#{r:02X}{g:02X}{b:02X}"

    def _darken_hex(self, hex_color, amount=0.1):
        amount = max(0.0, min(1.0, amount))
        if not isinstance(hex_color, str) or not hex_color.startswith("#") or len(hex_color) != 7:
            return hex_color

        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        r = int(r * (1 - amount))
        g = int(g * (1 - amount))
        b = int(b * (1 - amount))
        return f"#{r:02X}{g:02X}{b:02X}"

    def _resolve_ctk_color(self, color_value, fallback="#2B2B2B"):
        appearance = ctk.get_appearance_mode().lower()
        if isinstance(color_value, (tuple, list)) and color_value:
            index = 1 if appearance == "dark" and len(color_value) > 1 else 0
            return self._to_hex_color(color_value[index], fallback)
        if isinstance(color_value, str) and color_value and color_value != "transparent":
            return self._to_hex_color(color_value, fallback)
        return self._to_hex_color(fallback, fallback)

    def _build_plot_palette(self):
        frame_bg = self._resolve_ctk_color(self.plot_frame.cget("fg_color"))
        appearance = ctk.get_appearance_mode().lower()
        if appearance == "dark":
            base_bg = self._darken_hex(frame_bg, 0.1)
            return {
                "figure_bg": base_bg,
                "axes_bg": base_bg,
                "text": "#E6EDF3",
                "grid": "#4B5563",
                "spine": "#6B7280",
                "numeric": "#4EA1FF",
                "analytic": "#66D19E",
                "ambient": "#FF7B72",
                "legend_bg": base_bg,
                "legend_edge": "#4B5563",
            }
        return {
            "figure_bg": frame_bg,
            "axes_bg": frame_bg,
            "text": "#111827",
            "grid": "#D1D5DB",
            "spine": "#9CA3AF",
            "numeric": "#0057B8",
            "analytic": "#2E8B57",
            "ambient": "#D22B2B",
            "legend_bg": frame_bg,
            "legend_edge": "#D1D5DB",
        }

    def _sync_output_box_style(self):
        palette = self._build_plot_palette()
        self.output_box.configure(
            fg_color=palette["figure_bg"],
            text_color=palette["text"],
        )

    def _render_plot(self, t, T_num, T_ana, Ta):
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        palette = self._build_plot_palette()
        self._sync_output_box_style()

        fig = Figure(figsize=(7.5, 4.6), dpi=100, facecolor=palette["figure_bg"])
        ax = fig.add_subplot(111, facecolor=palette["axes_bg"])
        ax.plot(t, T_num, color=palette["numeric"], linewidth=2.2, label="Solucion numerica")
        ax.plot(
            t,
            T_ana,
            color=palette["analytic"],
            linewidth=1.8,
            linestyle="--",
            label="Solucion analitica",
        )
        ax.axhline(
            y=Ta,
            color=palette["ambient"],
            linestyle=":",
            linewidth=1.8,
            label="Temperatura ambiente",
        )
        ax.set_title("Ley de Enfriamiento de Newton", color=palette["text"])
        ax.set_xlabel("Tiempo (min)", color=palette["text"])
        ax.set_ylabel("Temperatura (grados C)", color=palette["text"])
        ax.tick_params(colors=palette["text"])
        ax.grid(True, color=palette["grid"], alpha=0.35, linewidth=0.8)

        for spine in ax.spines.values():
            spine.set_color(palette["spine"])

        legend = ax.legend(loc="best", frameon=True)
        legend.get_frame().set_facecolor(palette["legend_bg"])
        legend.get_frame().set_edgecolor(palette["legend_edge"])
        for text in legend.get_texts():
            text.set_color(palette["text"])

        fig.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        plot_widget = self.canvas.get_tk_widget()
        plot_widget.configure(bg=palette["figure_bg"], highlightthickness=0)
        plot_widget.grid(row=0, column=0, sticky="nsew")

    def calcular(self):
        try:
            T0 = self._get_float("T0", "Temperatura inicial")
            Ta = self._get_float("Ta", "Temperatura ambiente")
            tiempo_med = self._get_float("t_med", "Tiempo de medicion")
            temp_med = self._get_float("T_med", "Temperatura medida")
            t_max = self._get_float("t_max", "Tiempo total")

            dt = self._get_float("dt", "Paso de tiempo dt")

            if t_max <= 0 or tiempo_med <= 0 or dt <= 0:
                raise ValueError("t, t_max y dt deben ser mayores que 0.")

            k = calcular_constante_k(T0, Ta, tiempo_med, temp_med)
            t_num, T_num = simular_enfriamiento(T0, Ta, k, t_max=t_max, dt=dt)
            T_ana = solucion_analitica(t_num, T0, Ta, k)

            ruta_grafica = graficar_estatico(t_num, T_num, Ta)
            ruta_gif = generar_gif(t_num, T_num, Ta)

            self._render_plot(t_num, T_num, T_ana, Ta)

            error_final = abs(T_num[-1] - T_ana[-1])
            resumen = (
                "Modelo matematico:\n"
                "dT/dt = k(T - Ta)\n\n"
                f"Constante calculada k = {k:.6f} 1/min\n"
                f"T({t_max:.2f}) numerica = {T_num[-1]:.4f} grados C\n"
                f"T({t_max:.2f}) analitica = {T_ana[-1]:.4f} grados C\n"
                f"Error absoluto final = {error_final:.6f}\n\n"
                f"Grafica exportada: {ruta_grafica}\n"
                f"GIF exportado: {ruta_gif}\n"
            )
            self._set_output_text(resumen)
        except Exception as exc:
            messagebox.showerror("Error en el calculo", str(exc))
            self._set_output_text(f"Error: {exc}")

    def limpiar(self):
        for entry in self.entries.values():
            entry.delete(0, "end")

        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        self._set_output_text("Ingresa los datos y presiona 'Calcular y simular'.")


def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = NewtonCoolingCalculator()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()