# solver.py
import numpy as np

def simular_enfriamiento(T0, Ta, k, t_max, dt=0.5):
    """
    Resuelve numéricamente la EDO usando el Método de Euler.
    Convención del profesor: dT/dt = k(T - Ta) donde 'k' es negativo.
    """
    num_pasos = int(t_max / dt) + 1
    
    t = np.zeros(num_pasos)
    T = np.zeros(num_pasos)
    
    t[0] = 0
    T[0] = T0
    
    # Bucle iterativo aplicando el Método de Euler
    for i in range(1, num_pasos):
        t[i] = t[i-1] + dt
        
        # Pendiente térmica (k es negativo, por lo que el resultado se ajusta solo)
        dT_dt = k * (T[i-1] - Ta)
        
        # Nueva temperatura
        T[i] = T[i-1] + (dt * dT_dt)
        
    return t, T