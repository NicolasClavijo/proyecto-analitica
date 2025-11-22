from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Cargar modelo
modelo = joblib.load("modelo_final.pkl")

@app.route("/predecir", methods=["POST"])
def predecir():
    data = request.get_json()

    # Obtener los valores en el orden correcto
    entrada = np.array([[
        data["StudyTimeWeekly"],
        data["Absences"],
        data["Tutoring"],
        data["ParentalSupport"],
        data["Extracurricular"],
        data["Sports"],
        data["Music"]
    ]])

    # Hacer predicción
    prediccion = modelo.predict(entrada)[0]

    return jsonify({"GPA_Predicho": float(prediccion)})

if __name__ == "__main__":
    app.run(debug=True)
