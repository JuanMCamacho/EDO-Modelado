# Simulador de la Ley de Enfriamiento de Newton

Este proyecto desarrolla un sistema de modelado y simulación para analizar el proceso de enfriamiento (o calentamiento) de un objeto utilizando la **Ley de Enfriamiento de Newton**. Integra una solución numérica mediante el método de Euler / Runge-Kutta y una interfaz gráfica profesional.

## Requisitos del Sistema
* **Python 3.8 o superior**
* Bibliotecas necesarias: `numpy`, `matplotlib`, `scipy`, `customtkinter`, `pillow`.

## Instalación y Configuración

Para ejecutar el proyecto localmente, sigue estos pasos desde tu terminal de PowerShell o CMD:

1. **Crear un entorno virtual (Recomendado):**
   ```powershell
   python -m venv venv
   ```

2. **Activar el entorno:**
   * En Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
   * En macOS/Linux: `source venv/bin/activate`

3. **Instalar dependencias:**
   ```powershell
   pip install numpy matplotlib scipy customtkinter pillow
   ```

## Estructura de Ejecución

El proyecto se divide en dos módulos principales para cubrir la totalidad de la rúbrica de evaluación:

### 1. Calculadora e Interfaz Interactiva (`main.py`)
Es el punto de entrada principal. Permite al usuario ingresar parámetros en tiempo real para:
* Calcular la constante de enfriamiento **k** automáticamente a partir de una medición previa.
* Simular numéricamente la evolución de la temperatura.
* Generar una gráfica estática y una **animación GIF** del proceso.

**Ejecución:** ```powershell
python main.py
```

### 2. Análisis de Escenarios Comparativos (`escenarios.py`)
Este script fue desarrollado específicamente para cumplir con el punto de **"Modelo Predictivo"** de la rúbrica. Genera una comparativa automática entre:
* **Escenario Base:** Entorno predeterminado (ej. Procesador en banco de pruebas a 80°C).
* **Mejor Disipación:** Variación de la constante de enfriamiento `k` para simular distintos materiales.
* **Ambiente Controlado:** Variación de la temperatura ambiente `Ta`.

**Ejecución:** ```powershell
python escenarios.py
```
*Nota: La gráfica resultante se guarda automáticamente en la carpeta `/resultados/comparativa_escenarios.png`.*

## Nota:
Siguiendo las instrucciones impartidas en clase, el modelo matemático y el código utilizan la convención de una **constante k negativa** ($k < 0$) para representar la razón de cambio en la Ecuación Diferencial Ordinaria:

$$ \frac{dT}{dt} = k(T - T_a) $$

---
**Proyecto desarrollado para la materia de Ecuaciones Diferenciales.**