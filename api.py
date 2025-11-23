from flask import Flask, request, jsonify, render_template_string
import joblib
import numpy as np

app = Flask(__name__)

# Cargar modelo
modelo = joblib.load("modelo_final.pkl")

# Template HTML para la página principal
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduFuture API</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0f1e;
            color: #e5e7eb;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
            overflow-x: hidden;
        }
        
        /* Animated gradient background */
        body::before {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at 20% 50%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 40% 20%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
            animation: drift 30s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes drift {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(30px, -30px) rotate(5deg); }
            66% { transform: translate(-20px, 20px) rotate(-5deg); }
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 80px 40px;
            position: relative;
            z-index: 1;
        }
        
        /* Header */
        .header {
            text-align: center;
            margin-bottom: 64px;
            animation: fadeInDown 0.8s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo-container {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        .logo {
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            box-shadow: 0 8px 32px rgba(99, 102, 241, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            position: relative;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .logo::before {
            content: '';
            position: absolute;
            inset: -2px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            border-radius: 20px;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: -1;
            filter: blur(12px);
        }
        
        .logo:hover {
            transform: scale(1.05) translateY(-2px);
        }
        
        .logo:hover::before {
            opacity: 0.6;
        }
        
        .title {
            font-size: clamp(36px, 7vw, 56px);
            font-weight: 900;
            background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 50%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.04em;
            margin-bottom: 12px;
            line-height: 1.1;
        }
        
        .subtitle {
            font-size: clamp(15px, 2.5vw, 18px);
            color: #9ca3af;
            font-weight: 500;
            letter-spacing: 0.01em;
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* Status Badge */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 28px;
            border-radius: 50px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
            font-size: 14px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 48px;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.15);
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.2s both;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .status-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.2); }
        }
        
        /* API Card */
        .api-card {
            background: rgba(31, 41, 55, 0.6);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 32px;
            padding: 48px;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset,
                        0 1px 0 0 rgba(255, 255, 255, 0.05) inset;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
            margin-bottom: 32px;
        }
        
        .api-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.6) 50%, transparent);
        }
        
        .card-title {
            font-size: clamp(20px, 4vw, 24px);
            font-weight: 800;
            color: #fff;
            margin-bottom: 24px;
            letter-spacing: -0.03em;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .endpoint-section {
            margin-bottom: 32px;
        }
        
        .endpoint-section:last-child {
            margin-bottom: 0;
        }
        
        .endpoint-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .method-badge {
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.2) 100%);
            color: #a5b4fc;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        
        .endpoint-path {
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: clamp(14px, 2.5vw, 16px);
            color: #e5e7eb;
            font-weight: 600;
        }
        
        .endpoint-description {
            color: #9ca3af;
            font-size: 15px;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        /* Code Block */
        .code-block {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            margin-top: 16px;
            overflow-x: auto;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .code-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        
        .code-title {
            font-size: 12px;
            color: #9ca3af;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        
        pre {
            margin: 0;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.6;
            color: #e5e7eb;
        }
        
        .json-key {
            color: #8b5cf6;
        }
        
        .json-string {
            color: #10b981;
        }
        
        .json-number {
            color: #f59e0b;
        }
        
        .json-boolean {
            color: #ef4444;
        }
        
        /* Parameters Table */
        .params-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
        }
        
        .params-table th {
            text-align: left;
            padding: 12px 16px;
            background: rgba(17, 24, 39, 0.6);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            font-size: 12px;
            color: #9ca3af;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        
        .params-table td {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 14px;
        }
        
        .params-table tr:last-child td {
            border-bottom: none;
        }
        
        .param-name {
            font-family: 'Monaco', 'Courier New', monospace;
            color: #a5b4fc;
            font-weight: 600;
        }
        
        .param-type {
            color: #10b981;
            font-size: 12px;
            font-weight: 600;
        }
        
        .param-desc {
            color: #9ca3af;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 64px;
            padding-top: 32px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            color: #6b7280;
            font-size: 14px;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 48px 24px;
            }
            
            .api-card {
                padding: 32px 24px;
            }
            
            .code-block {
                padding: 20px 16px;
            }
            
            .params-table {
                font-size: 13px;
            }
            
            .params-table th,
            .params-table td {
                padding: 10px 12px;
            }
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 40px 16px;
            }
            
            .api-card {
                padding: 28px 20px;
                border-radius: 24px;
            }
            
            .endpoint-header {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-container">
                <div class="logo">🎓</div>
            </div>
            <h1 class="title">EduFuture API</h1>
            <p class="subtitle">Sistema de Predicción de Rendimiento Estudiantil</p>
        </div>
        
        <div style="text-align: center;">
            <div class="status-badge">
                <div class="status-indicator"></div>
                <span>API Operativa</span>
            </div>
        </div>
        
        <div class="api-card">
            <h2 class="card-title">📡 Endpoint Disponible</h2>
            
            <div class="endpoint-section">
                <div class="endpoint-header">
                    <span class="method-badge">POST</span>
                    <span class="endpoint-path">/predecir</span>
                </div>
                
                <p class="endpoint-description">
                    Predice la calificación (GPA) de un estudiante basándose en múltiples factores académicos y personales.
                </p>
                
                <h3 style="font-size: 16px; color: #e5e7eb; margin-top: 24px; margin-bottom: 12px; font-weight: 700;">Parámetros de Entrada</h3>
                
                <table class="params-table">
                    <thead>
                        <tr>
                            <th>Parámetro</th>
                            <th>Tipo</th>
                            <th>Descripción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="param-name">StudyTimeWeekly</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Horas de estudio semanales</td>
                        </tr>
                        <tr>
                            <td class="param-name">Absences</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Número de ausencias en el semestre</td>
                        </tr>
                        <tr>
                            <td class="param-name">Tutoring</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Recibe tutorías (0 = No, 1 = Sí)</td>
                        </tr>
                        <tr>
                            <td class="param-name">ParentalSupport</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Apoyo parental (0 = No, 1 = Sí)</td>
                        </tr>
                        <tr>
                            <td class="param-name">Extracurricular</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Actividades extracurriculares (0 = No, 1 = Sí)</td>
                        </tr>
                        <tr>
                            <td class="param-name">Sports</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Practica deportes (0 = No, 1 = Sí)</td>
                        </tr>
                        <tr>
                            <td class="param-name">Music</td>
                            <td class="param-type">number</td>
                            <td class="param-desc">Estudia música (0 = No, 1 = Sí)</td>
                        </tr>
                    </tbody>
                </table>
                
                <div class="code-block">
                    <div class="code-header">
                        <span class="code-title">Ejemplo de Request</span>
                    </div>
                    <pre><span class="json-key">{</span>
  <span class="json-key">"StudyTimeWeekly"</span>: <span class="json-number">15</span>,
  <span class="json-key">"Absences"</span>: <span class="json-number">2</span>,
  <span class="json-key">"Tutoring"</span>: <span class="json-number">1</span>,
  <span class="json-key">"ParentalSupport"</span>: <span class="json-number">1</span>,
  <span class="json-key">"Extracurricular"</span>: <span class="json-number">1</span>,
  <span class="json-key">"Sports"</span>: <span class="json-number">1</span>,
  <span class="json-key">"Music"</span>: <span class="json-number">0</span>
<span class="json-key">}</span></pre>
                </div>
                
                <div class="code-block">
                    <div class="code-header">
                        <span class="code-title">Ejemplo de Response</span>
                    </div>
                    <pre><span class="json-key">{</span>
  <span class="json-key">"GPA_Predicho"</span>: <span class="json-number">8.5</span>
<span class="json-key">}</span></pre>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>EduFuture API v1.0 • Desarrollado con Flask & Machine Learning</p>
        </div>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def home():
    """Página principal de la API"""
    return render_template_string(HOME_TEMPLATE)

@app.route("/predecir", methods=["POST"])
def predecir():
    """Endpoint de predicción"""
    try:
        data = request.get_json()
        
        # Validar que todos los campos estén presentes
        required_fields = ["StudyTimeWeekly", "Absences", "Tutoring", 
                          "ParentalSupport", "Extracurricular", "Sports", "Music"]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido: {field}"}), 400
        
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
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)