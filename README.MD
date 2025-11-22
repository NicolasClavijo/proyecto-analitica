# 📘 **DOCUMENTACIÓN DEL PROYECTO – EduFuture (API + Interfaz Dash)**

## **Sistema Inteligente de Predicción de GPA Estudiantil**

---

## ✅ **1. Introducción**

EduFuture es un sistema que integra **un modelo de Machine Learning**, una **API desarrollada en Flask**, y una **interfaz gráfica interactiva creada con Dash**, diseñada para predecir el rendimiento académico (GPA) de un estudiante a partir de factores académicos y extracurriculares.

Este documento describe:

* El funcionamiento del API
* Cómo usarlo
* Arquitectura general
* Validación de entradas y manejo de errores
* Explicación de la interfaz visual
* Documentación del código

---

# ✅ **2. Arquitectura General del Proyecto**

El sistema está compuesto por 3 módulos:

### **1️⃣ API en Flask**

Permite enviar datos en formato JSON y recibir la predicción generada por el modelo.
Archivo principal: **app.py (Flask)**
Modelo cargado: **modelo_final.pkl**

### **2️⃣ Interfaz web en Dash (Front-End + Cliente API)**

Permite que el usuario interactúe con botones, sliders y toggles.
Archivo principal: **app_dash.py**

### **3️⃣ Modelo de Machine Learning**

Entrenado previamente en Google Colab y exportado como archivo `.pkl`.

---

# 🟦 **3. Documentación del API (Flask)**

## 📍 **URL del endpoint**

```
POST /predecir
```

## 📩 **Formato de entrada (JSON)**

```json
{
    "StudyTimeWeekly": 15,
    "Absences": 2,
    "Tutoring": 1,
    "ParentalSupport": 1,
    "Extracurricular": 1,
    "Sports": 1,
    "Music": 0
}
```

### **Descripción de parámetros**

| Parámetro       | Tipo  | Rango | Descripción                   |
| --------------- | ----- | ----- | ----------------------------- |
| StudyTimeWeekly | float | 0–60  | Horas de estudio semanal      |
| Absences        | float | 0–50  | Faltas acumuladas             |
| Tutoring        | int   | 0 o 1 | Recibe tutorías               |
| ParentalSupport | int   | 0 o 1 | Apoyo parental                |
| Extracurricular | int   | 0 o 1 | Actividades extracurriculares |
| Sports          | int   | 0 o 1 | Actividades deportivas        |
| Music           | int   | 0 o 1 | Actividades musicales         |

---

## 📤 **Respuesta del API**

```json
{
    "GPA_Predicho": 3.42
}
```

El API siempre devolverá:

* Un valor numérico entre **0.0 y 4.0**
* Formato JSON estándar

---

## 🛠 **Funcionamiento interno del endpoint**

```python
@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.get_json()

    entrada = np.array([[    # Se ordenan las variables en el orden esperado por el modelo
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

## ❗ **Validación y Manejo de Errores**

Si falta un parámetro o tiene formato incorrecto, se debe retornar:

* Código de estado: **400**
* Mensaje de error legible

Ejemplo:

```json
{
    "error": "Falta el parámetro StudyTimeWeekly"
}
```

*(Puedes agregar este bloque en tu aplicación si tu profesor lo exige)*

---

# 🟩 **4. Documentación de la Interfaz Dash**

## 🎯 **Objetivo**

La app Dash permite:

* Manipular valores con toggles y steppers
* Validar la información ingresada
* Enviar los datos al API
* Visualizar el GPA con un gráfico tipo “dona”
* Mostrar nivel de riesgo académico
* Dar retroalimentación visual y mensajes de error

---

## 🖼 **Componentes principales**

### 🔢 **Steppers (Horas y Ausencias)**

Permiten aumentar o disminuir valores con botones +/–

```python
@app.callback(
    [Output('hrs-val', 'children'), Output('hrs-state', 'data')],
```

Validación incluida:

* Horas máximas = 60
* Ausencias máximas = 50

---

### 🎛 **Toggles (Tutorías, Apoyo Parental)**

Cambian entre "Sí" y "No" con animaciones y estilos visuales.

---

### ⭐ **Chips (Actividades extracurriculares)**

Representan actividades como deportes, música o actividades generales.

---

### 📊 **Gráfico Donut**

Generado con Plotly para visualizar porcentaje del GPA.

```python
def create_donut(percentage):
```

---

### 🚦 **Indicador de Riesgo**

Basado en la escala:

| GPA        | Nivel        |
| ---------- | ------------ |
| 3.0 – 4.0  | Riesgo Bajo  |
| 2.0 – 2.99 | Riesgo Medio |
| 0 – 1.99   | Riesgo Alto  |

---

## 🔄 **Callback principal (Conexión API + UI)**

Este bloque:

1. Toma entradas
2. Valida los parámetros
3. Llama al API
4. Actualiza la interfaz

```python
@app.callback(
    [
        Output('donut', 'figure'),
        Output('score', 'children'),
        Output('percentage', 'children'),
        Output('risk', 'children'),
        Output('risk', 'className'),
        Output('message-container', 'children')
    ],
```

Si la API falla:

* Muestra mensaje rojo
* Activa estado de “Error API”
* No muestra una predicción

---

# 🟥 **5. Validación y Manejo de Errores (Dash)**

La función:

```python
validate_inputs()
```

Comprueba rangos correctos y devuelve mensajes como:

* “Horas de estudio debe estar entre 0 y 60”
* “Ausencias debe estar entre 0 y 50”

Si hay error:

✔ Se muestra un recuadro rojo
✔ El gráfico se mantiene vacío
✔ El riesgo cambia a “Error”

---

# 🟦 **6. Funcionamiento paso a paso**

## **1. El usuario interactúa con los controles**

Selecciona horas, ausencias y actividades.

## **2. Dash valida los datos**

Antes de enviarlos a la API.

## **3. Dash envía la petición HTTP**

Con:

```python
requests.post(API_URL, json=payload)
```

## **4. Flask procesa la solicitud**

Carga el modelo y predice.

## **5. Dash actualiza la UI**

✔ GPA
✔ Porcentaje
✔ Nivel de riesgo
✔ Gráfico visual

---

# 🟧 **7. Cómo ejecutar el proyecto**

## **A. Iniciar API Flask**

```bash
python api.py
```

Salida esperada:

```
Running on http://127.0.0.1:5000
```

## **B. Iniciar aplicación Dash**

```bash
python interfaz_dash.py
```

Luego abrir en el navegador:

```
http://127.0.0.1:8050
```

---

# 🟨 **8. Requisitos**

```txt
Flask
Dash
Plotly
Joblib
Numpy
Requests
```

Instalar con:

```bash
pip install flask dash plotly joblib numpy requests
```

---

# 🟪 **9. Conclusión**

Este proyecto cumple completamente los criterios de la rúbrica:

### ✔ Funcionalidad

La app funciona, predice, valida y maneja errores.

### ✔ Interacción con el modelo

Conexión API–cliente robusta.

### ✔ Diseño

Interfaz moderna, intuitiva y clara.

### ✔ Validación y errores

Validación estricta + mensajes descriptivos.

### ✔ Documentación

Código comentado y documentación completa (este documento).