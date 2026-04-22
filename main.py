# main.py
import numpy as np
from solver import simular_enfriamiento
from visualizer import graficar_estatico, generar_gif

def calcular_constante_k(T0, Ta, tiempo_prueba, temp_prueba):
    """
    Calcula la constante k asumiendo la fórmula: T(t) = Ta + (T0 - Ta) * e^(kt)
    Al despejar k, el resultado será naturalmente negativo.
    """
    if T0 == Ta or temp_prueba == Ta:
        return 0.0
        
    # Despeje: k = ln((T(t) - Ta) / (T0 - Ta)) / t
    razon = (temp_prueba - Ta) / (T0 - Ta)
    k = np.log(razon) / tiempo_prueba
    return k

def main():
    # 1. Datos del Problema (Basado en la diapositiva del profesor)
    T_inicial = 20.0       # T(0) = 20°C (Procesador frío)
    T_ambiente = 80.0      # Tm = 80°C (Banco de pruebas)
    tiempo_eval = 3.0      # t = 3 minutos
    temp_eval = 50.0       # T(3) = 50°C
    
    tiempo_total_simulacion = 25 # Minutos para ver cómo se estabiliza
    
    print("Resolviendo problema analítico...")
    
    # El programa calcula 'k' automáticamente respetando la ley de los signos
    k_constante = calcular_constante_k(T_inicial, T_ambiente, tiempo_eval, temp_eval)
    
    print(f"La constante k calculada es: {k_constante:.4f}") 
    # Esto imprimirá exactamente -0.2310
    
    print("Iniciando cálculo numérico por Método de Euler...")
    
    # 2. Simulación Numérica
    tiempos, temperaturas = simular_enfriamiento(
        T0=T_inicial, 
        Ta=T_ambiente, 
        k=k_constante, 
        t_max=tiempo_total_simulacion
    )
    
    print("Cálculo completado. Generando recursos visuales...")
    
    # 3. Visualización y Exportación
    # El archivo visualizer.py no necesita cambios, funcionará perfectamente con estos datos
    graficar_estatico(tiempos, temperaturas, T_ambiente)
    generar_gif(tiempos, temperaturas, T_ambiente)
    
    print("¡Ejecución finalizada con éxito!")

if __name__ == "__main__":
    main()