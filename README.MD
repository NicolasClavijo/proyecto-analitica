# 📘 **DOCUMENTACIÓN DEL PROYECTO – EduFuture**

## **Sistema Inteligente de Predicción del Rendimiento Estudiantil (GPA)**

### **Universidad de La Sabana – Proyecto en Analítica**

### **Autores: Nicolás Clavijo, Christian Cruz, Cristian Rodríguez, Katerin García**

---

# ✨ **1. Introducción**

EduFuture es un sistema integral diseñado para predecir el **GPA (promedio académico)** de un estudiante utilizando técnicas de Machine Learning.
El proyecto fue desarrollado para la materia **Proyecto en Analítica**, de la Universidad de La Sabana, por:

* **Nicolás Clavijo**
* **Christian Cruz**
* **Cristian Rodríguez**
* **Katerin García**

El sistema combina:

* Una **API REST en Flask**
* Una **interfaz interactiva creada en Dash**
* Un **modelo predictivo entrenado en Python**
* Validación rigurosa de datos
* Manejo de errores y mensajes informativos
* Diseño moderno y experiencia de usuario mejorada

El sistema permite al usuario ingresar factores académicos y extracurriculares y recibir:

* Un **GPA predicho**
* Un **indicador de riesgo académico**
* Un **porcentaje visual en forma de dona**
* Un **panel de recomendaciones personalizadas** para mejorar el rendimiento

---

# 🏗️ **2. Arquitectura General del Sistema**

El proyecto está compuesto por tres componentes principales:

---

## **1️⃣ API Flask – “motor de predicción”**

* Expone la ruta: **POST /predecir**
* Recibe variables numéricas y binarias
* Procesa la información
* Ejecuta el modelo entrenado (`modelo_final.pkl`)
* Retorna un valor tipo GPA (0.0 a 4.0)

---

## **2️⃣ Interfaz Dash – “interacción del usuario”**

* Interfaz visual intuitiva
* Steppers para horas y ausencias
* Toggles para tutorías y apoyo parental
* Chips para actividades extracurriculares
* Gráfico dinámico estilo “dona”
* Sistema de riesgo (bajo, medio, alto)
* Sección de consejos generados automáticamente
* Manejo robusto de errores del API

---

## **3️⃣ Modelo de Machine Learning**

* Entrenado en Google Colab
* Exportado con `joblib`
* Recibe siete variables y predice el GPA
* Integrado de manera modular en Flask

---

# 🔌 **3. Documentación del API (Flask)**

## 📍 **Endpoint disponible**

```
POST /predecir
```

---

## 📩 **Estructura de entrada (JSON)**

El API recibe exactamente los siguientes parámetros:

```json
{
    "StudyTimeWeekly": 12,
    "Absences": 3,
    "Tutoring": 1,
    "ParentalSupport": 0,
    "Extracurricular": 1,
    "Sports": 1,
    "Music": 0
}
```

---

## 🧩 **Significado de los parámetros**

| Nombre          | Tipo  | Rango | Descripción                   |
| --------------- | ----- | ----- | ----------------------------- |
| StudyTimeWeekly | float | 0–60  | Horas de estudio semanal      |
| Absences        | float | 0–50  | Número de ausencias           |
| Tutoring        | int   | 0 o 1 | Recibe tutorías               |
| ParentalSupport | int   | 0 o 1 | Cuenta con apoyo parental     |
| Extracurricular | int   | 0 o 1 | Actividades extracurriculares |
| Sports          | int   | 0 o 1 | Participa en deportes         |
| Music           | int   | 0 o 1 | Participa en música           |

---

## 📤 **Respuesta del API**

Ejemplo:

```json
{
    "GPA_Predicho": 3.42
}
```

Siempre retorna un número **entre 0.0 y 4.0**.

---

## 🧱 **Flujo interno del endpoint**

```python
@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.get_json()

    entrada = np.array([[ 
        data["StudyTimeWeekly"],
        data["Absences"],
        data["Tutoring"],
        data["ParentalSupport"],
        data["Extracurricular"],
        data["Sports"],
        data["Music"]
    ]])

    prediccion = modelo.predict(entrada)[0]
    return jsonify({"GPA_Predicho": float(prediccion)})
```

---

## 🚨 **Manejo de errores**

La API puede retornar errores por:

❌ Falta de campos
❌ Tipo de dato incorrecto
❌ Daño en el modelo
❌ Peticiones mal formadas

La interfaz Dash maneja todos estos errores correctamente.

---

# 🖥️ **4. Documentación de la Interfaz Dash**

La interfaz fue diseñada para cumplir los criterios de:

✔ Accesibilidad
✔ Interactividad
✔ Claridad visual
✔ Experiencia del usuario
✔ Retroalimentación inmediata

Incluye:

* Tarjetas animadas
* Controles interactivos
* Gráficos dinámicos
* Sistema de colores por riesgo
* Mensajes de error y carga
* Módulo de consejos personalizados

---

# ➕ **4.1 Controles principales**

## 🔢 Steppers (Ausencias / Horas de estudio)

Permiten aumentar o disminuir valores:

```python
@app.callback(
    [Output('aus-val', 'children'), Output('aus-state', 'data')],
```

Límites:

* Ausencias: 0–50
* Horas de estudio: 0–60

---

## 🎛 Toggles (Apoyo parental / Tutorías)

Cambian entre ON/OFF:

* Apoyo Parental
* Recibe Tutorías

Actualizan automáticamente el estado interno.

---

## ⭐ Chips de actividades extracurriculares

Incluye:

* Actividades generales
* Deportes
* Música

Se pueden activar/desactivar individualmente.

---

# 📊 **4.2 Gráfico de dona**

Representa el porcentaje del GPA:

```python
def create_donut(percentage):
```

La dona refleja visualmente el rendimiento.

---

# 🚦 **4.3 Sistema de riesgo**

Dependiendo del GPA:

| GPA      | Nivel        | Color    |
| -------- | ------------ | -------- |
| ≥ 3.0    | Riesgo Bajo  | Verde    |
| 2.0–2.99 | Riesgo Medio | Amarillo |
| < 2.0    | Riesgo Alto  | Rojo     |

---

# 💬 **4.4 Sistema de Consejos Personalizados**

Incluye una sección generada por la función:

```python
get_advice_content(gpa, ...)
```

Genera recomendaciones basadas en:

* Ausencias
* Horas de estudio
* Tutorías
* Actividades
* Deporte/Música

---

# 🔄 **4.5 Callback principal (núcleo de la app)**

Este callback:

1. Recoge todos los inputs
2. Valida datos
3. Llama a la API
4. Procesa la respuesta
5. Actualiza gráfico, riesgo, GPA y consejos

---

# 🛡️ **5. Validación y Manejo de Errores**

La función:

```python
validate_inputs()
```

Garantiza:

* Límites correctos
* Tipos válidos
* Valores coherentes

Errores se muestran con:

* Caja roja
* Mensaje descriptivo
* Riesgo marcado como “Error”
* Se evita llamar al API para protegerlo

---

# 🧪 **6. Ejemplo de uso**

1. Ajustar horas de estudio
2. Ajustar ausencias
3. Activar/desactivar tutorías
4. Activar actividades adicionales
5. Click en “Predecir GPA”

La interfaz muestra:

* GPA
* Porcentaje
* Riesgo
* Consejos personalizados
* Sincronización con la API

---

# 🛠️ **7. Cómo ejecutar el sistema**

## **1. Iniciar API Flask**

```bash
python api.py
```

Debe mostrar:

```
Running on http://127.0.0.1:5000
```

---

## **2. Iniciar la interfaz Dash**

```bash
python dashboard.py
```

Abrir:

```
http://127.0.0.1:8050
```

---

# 📦 **8. Requisitos**

```txt
Flask
numpy
joblib
dash
plotly
requests
```

Instalar con:

```bash
pip install flask dash plotly numpy joblib requests
```

---

# 🧾 **9. Conclusión**

El sistema **EduFuture** cumple completamente con los criterios de evaluación y la rúbrica:

### ✔ Funcionalidad

La aplicación predice correctamente, muestra resultados y maneja errores.

### ✔ Interacción con el modelo

Conexión API–Dash funcionando de forma estable y robusta.

### ✔ Diseño y UX

Interfaz moderna, clara, accesible, responsiva y estéticamente sobresaliente.

### ✔ Validación y errores

Control total de entradas + mensajes claros + sistema seguro contra fallos.

### ✔ Documentación

Este documento describe todo el flujo, arquitectura y uso.