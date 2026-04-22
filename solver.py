import numpy as np
from scipy.integrate import solve_ivp


def calcular_constante_k(T0, Ta, tiempo_prueba, temp_prueba):
    """Calcula k a partir de un punto medido usando la solucion analitica."""
    if tiempo_prueba <= 0:
        raise ValueError("El tiempo de medicion debe ser mayor a 0.")
    if np.isclose(T0, Ta):
        raise ValueError("T0 no puede ser igual a Ta para estimar k.")

    razon = (temp_prueba - Ta) / (T0 - Ta)
    if razon <= 0:
        raise ValueError(
            "Los datos no son fisicamente consistentes para calcular k (razon <= 0)."
        )

    return float(np.log(razon) / tiempo_prueba)


def solucion_analitica(t, T0, Ta, k):
    """Devuelve T(t) = Ta + (T0 - Ta) * exp(k*t)."""
    return Ta + (T0 - Ta) * np.exp(k * np.asarray(t))


def _modelo_enfriamiento(_t, temperatura, k, Ta):
    return k * (temperatura - Ta)


def simular_enfriamiento(T0, Ta, k, t_max, dt):
    """Resuelve numericamente la EDO dT/dt = k(T-Ta) con scipy.integrate."""
    if t_max <= 0:
        raise ValueError("El tiempo total de simulacion debe ser mayor a 0.")
    if dt <= 0:
        raise ValueError("El paso de tiempo dt debe ser mayor a 0.")

    num_pasos = int(t_max / dt) + 1
    t_eval = np.linspace(0.0, t_max, num_pasos)

    solucion = solve_ivp(
        _modelo_enfriamiento,
        (0.0, t_max),
        [float(T0)],
        t_eval=t_eval,
        args=(float(k), float(Ta)),
        method="RK45",
    )

    if not solucion.success:
        raise RuntimeError(f"No se pudo resolver la EDO: {solucion.message}")

    return solucion.t, solucion.y[0]