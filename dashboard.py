import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import requests
import os

# Configuración de la URL de la API
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000/predecir")

app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>EduFuture</title>
    {%favicon%}
    {%css%}
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
            line-height: 1.5;
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
            max-width: 1400px;
            margin: 0 auto;
            padding: 80px 40px;
            position: relative;
            z-index: 1;
        }
        
        /* Header */
        .header {
            text-align: center;
            margin-bottom: 72px;
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
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
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
            border-radius: 18px;
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
            font-size: clamp(32px, 7vw, 56px);
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
            font-size: clamp(14px, 2.5vw, 17px);
            color: #9ca3af;
            font-weight: 500;
            letter-spacing: 0.01em;
            max-width: 600px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        /* Main Card */
        .main-card {
            background: rgba(31, 41, 55, 0.6);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 32px;
            padding: 56px;
            margin-bottom: 48px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            gap: 40px;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset,
                        0 1px 0 0 rgba(255, 255, 255, 0.05) inset;
            position: relative;
            overflow: hidden;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
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
        
        .main-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.6) 50%, transparent);
        }
        
        .main-card:hover {
            box-shadow: 0 32px 80px rgba(0, 0, 0, 0.6),
                        0 0 0 1px rgba(255, 255, 255, 0.15) inset,
                        0 1px 0 0 rgba(255, 255, 255, 0.08) inset;
            transform: translateY(-2px);
        }
        
        .progress-section {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        
        .progress-ring {
            position: relative;
            filter: drop-shadow(0 8px 24px rgba(16, 185, 129, 0.3));
            display: inline-block;
        }
        
        .percentage {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: clamp(32px, 5vw, 40px);
            font-weight: 900;
            background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.03em;
        }
        
        .score-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }
        
        .score-label {
            font-size: clamp(11px, 2vw, 13px);
            color: #9ca3af;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 16px;
        }
        
        .score-container {
            display: flex;
            align-items: baseline;
            justify-content: center;
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .score {
            font-size: clamp(56px, 10vw, 80px);
            font-weight: 900;
            background: linear-gradient(135deg, #ffffff 0%, #f3f4f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
            letter-spacing: -0.05em;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .score:hover {
            transform: scale(1.02);
        }
        
        .score-max {
            font-size: clamp(24px, 4vw, 32px);
            color: #6b7280;
            font-weight: 600;
        }
        
        .risk {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 12px 24px;
            border-radius: 14px;
            font-size: clamp(12px, 2vw, 14px);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .risk-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.6; transform: scale(1.2); }
        }
        
        .risk-low {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.15);
        }
        
        .risk-low .risk-indicator {
            background: #10b981;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.6);
        }
        
        .risk-medium {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
            color: #f59e0b;
            border: 1px solid rgba(245, 158, 11, 0.3);
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.15);
        }
        
        .risk-medium .risk-indicator {
            background: #f59e0b;
            box-shadow: 0 0 12px rgba(245, 158, 11, 0.6);
        }
        
        .risk-high {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
            box-shadow: 0 4px 16px rgba(239, 68, 68, 0.15);
        }
        
        .risk-high .risk-indicator {
            background: #ef4444;
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.6);
        }
        
        /* Error/Loading message */
        .message {
            padding: 16px 24px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            margin-top: 12px;
        }
        
        .message-error {
            background: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .message-loading {
            background: rgba(99, 102, 241, 0.1);
            color: #6366f1;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        
        /* Section Title */
        .section-title {
            font-size: clamp(22px, 4vw, 28px);
            font-weight: 800;
            color: #fff;
            margin-bottom: 32px;
            letter-spacing: -0.03em;
            text-align: center;
        }
        
        /* Cards Grid */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
            gap: 24px;
            margin-bottom: 48px;
        }
        
        .card {
            background: rgba(31, 41, 55, 0.6);
            backdrop-filter: blur(40px) saturate(180%);
            -webkit-backdrop-filter: blur(40px) saturate(180%);
            border-radius: 28px;
            padding: 32px;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
        
        .card:nth-child(1) { animation-delay: 0.2s; }
        .card:nth-child(2) { animation-delay: 0.3s; }
        .card:nth-child(3) { animation-delay: 0.4s; }
        
        .card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5),
                        0 0 0 1px rgba(255, 255, 255, 0.15) inset;
        }
        
        .card-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 32px;
        }
        
        .card-icon {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            flex-shrink: 0;
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .card:hover .card-icon {
            transform: scale(1.1) rotate(5deg);
        }
        
        .card-title {
            font-size: clamp(16px, 3vw, 19px);
            font-weight: 700;
            color: #fff;
            letter-spacing: -0.02em;
        }
        
        /* Stepper */
        .stepper {
            margin-bottom: 32px;
        }
        
        .stepper:last-child {
            margin-bottom: 0;
        }
        
        .label {
            font-size: clamp(11px, 2vw, 12px);
            color: #9ca3af;
            font-weight: 600;
            margin-bottom: 16px;
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        
        .stepper-controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: clamp(16px, 3vw, 24px);
        }
        
        .stepper-btn {
            width: clamp(40px, 8vw, 48px);
            height: clamp(40px, 8vw, 48px);
            border-radius: 14px;
            background: rgba(55, 65, 81, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #fff;
            font-size: clamp(20px, 4vw, 24px);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .stepper-btn:hover {
            background: rgba(75, 85, 99, 0.9);
            border-color: rgba(255, 255, 255, 0.15);
            transform: scale(1.08);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .stepper-btn:active {
            transform: scale(0.96);
        }
        
        .value {
            font-size: clamp(28px, 6vw, 36px);
            font-weight: 800;
            color: #fff;
            min-width: clamp(70px, 15vw, 90px);
            text-align: center;
            letter-spacing: -0.03em;
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .value:hover {
            transform: scale(1.05);
        }
        
        /* Toggle */
        .toggle {
            width: 100%;
            padding: 16px 20px;
            border-radius: 14px;
            background: rgba(55, 65, 81, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e5e7eb;
            font-size: clamp(13px, 2.5vw, 15px);
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 16px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            text-align: left;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .toggle:last-child {
            margin-bottom: 0;
        }
        
        .toggle:hover {
            background: rgba(75, 85, 99, 0.7);
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateX(4px) scale(1.01);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .toggle-active {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.3) 0%, rgba(16, 185, 129, 0.2) 100%);
            color: #fff;
            border-color: rgba(16, 185, 129, 0.4);
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.25),
                        0 0 0 1px rgba(16, 185, 129, 0.1) inset;
        }
        
        .toggle-active:hover {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.4) 0%, rgba(16, 185, 129, 0.3) 100%);
            border-color: rgba(16, 185, 129, 0.5);
            transform: translateX(4px) scale(1.02);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.35);
        }
        
        /* Chip */
        .chip {
            width: 100%;
            padding: 14px 20px;
            border-radius: 14px;
            background: rgba(55, 65, 81, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #9ca3af;
            font-size: clamp(13px, 2.5vw, 15px);
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 14px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .chip:last-child {
            margin-bottom: 0;
        }
        
        .chip:hover {
            background: rgba(75, 85, 99, 0.7);
            border-color: rgba(255, 255, 255, 0.15);
            color: #e5e7eb;
            transform: scale(1.02);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        }
        
        .chip-active {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(139, 92, 246, 0.2) 100%);
            color: #fff;
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 4px 16px rgba(99, 102, 241, 0.25),
                        0 0 0 1px rgba(99, 102, 241, 0.1) inset;
        }
        
        .chip-active:hover {
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.4) 0%, rgba(139, 92, 246, 0.3) 100%);
            border-color: rgba(99, 102, 241, 0.5);
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        }
        
        /* Action Button */
        .actions {
            text-align: center;
            animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.5s both;
        }
        
        .btn-primary {
            padding: clamp(14px, 3vw, 18px) clamp(32px, 8vw, 48px);
            border-radius: 16px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            border: none;
            color: #fff;
            font-size: clamp(14px, 2.5vw, 16px);
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4),
                        0 0 0 1px rgba(255, 255, 255, 0.1) inset;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            position: relative;
            overflow: hidden;
            width: 100%;
            max-width: 400px;
        }
        
        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        .btn-primary:hover::before {
            left: 100%;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 32px rgba(99, 102, 241, 0.5),
                        0 0 0 1px rgba(255, 255, 255, 0.15) inset;
        }
        
        .btn-primary:active {
            transform: translateY(0) scale(0.98);
        }
        
        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .container {
                padding: 60px 32px;
            }
            
            .main-card {
                padding: 40px 32px;
            }
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 48px 24px;
            }
            
            .header {
                margin-bottom: 48px;
            }
            
            .main-card {
                padding: 32px 24px;
                gap: 32px;
            }
            
            .card {
                padding: 28px 20px;
            }
            
            .grid {
                gap: 20px;
            }
            
            .logo {
                width: 48px;
                height: 48px;
                font-size: 24px;
            }
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 40px 16px;
            }
            
            .header {
                margin-bottom: 40px;
            }
            
            .main-card {
                padding: 28px 20px;
                border-radius: 24px;
                gap: 28px;
            }
            
            .card {
                padding: 24px 18px;
                border-radius: 20px;
            }
            
            .card-header {
                margin-bottom: 24px;
            }
            
            .stepper {
                margin-bottom: 24px;
            }
            
            .toggle, .chip {
                padding: 12px 16px;
            }
        }
        
        @media (max-width: 360px) {
            .stepper-controls {
                gap: 12px;
            }
            
            .value {
                min-width: 60px;
            }
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

def create_donut(percentage):
    """Crea el gráfico de dona para el porcentaje"""
    fig = go.Figure(data=[go.Pie(
        values=[percentage, 100-percentage],
        hole=0.78,
        marker=dict(
            colors=['#10b981', 'rgba(31, 41, 55, 0.4)'],
            line=dict(color='rgba(0,0,0,0)', width=0)
        ),
        textinfo='none',
        hoverinfo='skip',
        showlegend=False
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=200,
        width=200
    )
    
    return fig

def validate_inputs(hrs, aus, tut, ap, gen, dep, mus):
    """Valida que los inputs estén en rangos aceptables"""
    if not (0 <= hrs <= 60):
        return False, "Horas de estudio debe estar entre 0 y 60"
    if not (0 <= aus <= 50):
        return False, "Ausencias debe estar entre 0 y 50"
    if tut not in [0, 1]:
        return False, "Tutorías debe ser 0 o 1"
    if ap not in [0, 1]:
        return False, "Apoyo parental debe ser 0 o 1"
    if gen not in [0, 1]:
        return False, "Actividades generales debe ser 0 o 1"
    if dep not in [0, 1]:
        return False, "Deportes debe ser 0 o 1"
    if mus not in [0, 1]:
        return False, "Música debe ser 0 o 1"
    return True, "OK"

def call_prediction_api(study_time, absences, tutoring, parental_support, 
                        extracurricular, sports, music):
    """
    Llama a la API de predicción y retorna el resultado.
    
    Returns:
        tuple: (success, result_or_error_message)
    """
    try:
        # Construir el payload en el formato esperado
        payload = {
            "StudyTimeWeekly": float(study_time),
            "Absences": float(absences),
            "Tutoring": int(tutoring),
            "ParentalSupport": int(parental_support),
            "Extracurricular": int(extracurricular),
            "Sports": int(sports),
            "Music": int(music)
        }
        
        # Realizar el POST a la API
        response = requests.post(
            API_URL,
            json=payload,
            timeout=10  # Timeout de 10 segundos
        )
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            data = response.json()
            # Asumir que la API devuelve {'prediccion': valor} o similar
            if 'prediccion' in data:
                return True, float(data['prediccion'])
            elif 'prediction' in data:
                return True, float(data['prediction'])
            elif 'gpa' in data:
                return True, float(data['gpa'])
            else:
                # Si el formato es diferente, intentar obtener el primer valor numérico
                for key, value in data.items():
                    try:
                        return True, float(value)
                    except (ValueError, TypeError):
                        continue
                return False, "Formato de respuesta inesperado"
        else:
            return False, f"Error del servidor: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "Tiempo de espera agotado. El servidor no responde."
    except requests.exceptions.ConnectionError:
        return False, "No se pudo conectar con la API. Verifique que esté activa."
    except requests.exceptions.RequestException as e:
        return False, f"Error en la petición: {str(e)}"
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

app.layout = html.Div(className='container', children=[
    
    html.Div(className='header', children=[
        html.Div(className='logo-container', children=[
            html.Div('🎓', className='logo')
        ]),
        html.H1('EduFuture', className='title'),
        html.P('Sistema Inteligente de Predicción del Rendimiento Estudiantil', className='subtitle')
    ]),
    
    html.Div(className='main-card', children=[
        html.Div(className='progress-section', children=[
            html.Div(className='progress-ring', children=[
                dcc.Graph(id='donut', figure=create_donut(0), config={'displayModeBar': False}),
                html.Div(id='percentage', className='percentage', children='--')
            ])
        ]),
        html.Div(className='score-section', children=[
            html.Div('GPA Predicho', className='score-label'),
            html.Div(className='score-container', children=[
                html.Span(id='score', className='score', children='--'),
                html.Span('/4.0', className='score-max')
            ]),
            html.Div(id='risk', className='risk risk-medium', children=[
                html.Div(className='risk-indicator'),
                html.Span('Sin Predicción')
            ])
        ]),
        html.Div(id='message-container', children=[])
    ]),
    
    html.H2('Factores de Rendimiento', className='section-title'),
    
    html.Div(className='grid', children=[
        
        html.Div(className='card', children=[
            html.Div(className='card-header', children=[
                html.Div('📊', className='card-icon'),
                html.H3('Asistencia y Estudio', className='card-title')
            ]),
            html.Div(className='stepper', children=[
                html.Label('Ausencias (semestre)', className='label'),
                html.Div(className='stepper-controls', children=[
                    html.Button('−', id='aus-minus', className='stepper-btn'),
                    html.Div(id='aus-val', className='value', children='2'),
                    html.Button('+', id='aus-plus', className='stepper-btn')
                ])
            ]),
            html.Div(className='stepper', children=[
                html.Label('Horas de Estudio (semanal)', className='label'),
                html.Div(className='stepper-controls', children=[
                    html.Button('−', id='hrs-minus', className='stepper-btn'),
                    html.Div(id='hrs-val', className='value', children='15h'),
                    html.Button('+', id='hrs-plus', className='stepper-btn')
                ])
            ])
        ]),
        
        html.Div(className='card', children=[
            html.Div(className='card-header', children=[
                html.Div('🤝', className='card-icon'),
                html.H3('Apoyo Académico', className='card-title')
            ]),
            html.Button(id='apoyo', className='toggle toggle-active', children=[
                html.Span('👨‍👩‍👧'),
                html.Span('Apoyo Parental: Sí')
            ]),
            html.Button(id='tutoria', className='toggle toggle-active', children=[
                html.Span('📚'),
                html.Span('Recibe Tutorías: Sí')
            ])
        ]),
        
        html.Div(className='card', children=[
            html.Div(className='card-header', children=[
                html.Div('⭐', className='card-icon'),
                html.H3('Actividades Extra', className='card-title')
            ]),
            html.Button(id='general', className='chip chip-active', children=[
                html.Span('✨'),
                html.Span('Actividades Generales')
            ]),
            html.Button(id='deportes', className='chip chip-active', children=[
                html.Span('⚽'),
                html.Span('Deportes')
            ]),
            html.Button(id='musica', className='chip', children=[
                html.Span('🎵'),
                html.Span('Música')
            ])
        ])
    ]),
    
    html.Div(className='actions', children=[
        html.Button('Predecir GPA', id='update', className='btn-primary')
    ]),
    
    # Stores para mantener el estado
    dcc.Store(id='aus-state', data=2),
    dcc.Store(id='hrs-state', data=15),
    dcc.Store(id='apoyo-state', data=True),
    dcc.Store(id='tutoria-state', data=True),
    dcc.Store(id='general-state', data=True),
    dcc.Store(id='deportes-state', data=True),
    dcc.Store(id='musica-state', data=False)
])

# Callbacks para los steppers
@app.callback(
    [Output('aus-val', 'children'), Output('aus-state', 'data')],
    [Input('aus-minus', 'n_clicks'), Input('aus-plus', 'n_clicks')],
    [State('aus-state', 'data')]
)
def update_aus(minus, plus, val):
    ctx = dash.callback_context
    if not ctx.triggered: 
        return str(val), val
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn == 'aus-minus' and val > 0: 
        val -= 1
    elif btn == 'aus-plus' and val < 50: 
        val += 1
    return str(val), val

@app.callback(
    [Output('hrs-val', 'children'), Output('hrs-state', 'data')],
    [Input('hrs-minus', 'n_clicks'), Input('hrs-plus', 'n_clicks')],
    [State('hrs-state', 'data')]
)
def update_hrs(minus, plus, val):
    ctx = dash.callback_context
    if not ctx.triggered: 
        return f'{val}h', val
    btn = ctx.triggered[0]['prop_id'].split('.')[0]
    if btn == 'hrs-minus' and val > 0: 
        val -= 1
    elif btn == 'hrs-plus' and val < 60: 
        val += 1
    return f'{val}h', val

# Callbacks para los toggles
@app.callback(
    [Output('apoyo', 'className'), Output('apoyo', 'children'), Output('apoyo-state', 'data')],
    [Input('apoyo', 'n_clicks')],
    [State('apoyo-state', 'data')]
)
def toggle_apoyo(n, state):
    if n: 
        state = not state
    cls = 'toggle toggle-active' if state else 'toggle'
    txt = [html.Span('👨‍👩‍👧'), html.Span(f'Apoyo Parental: {"Sí" if state else "No"}')]
    return cls, txt, state

@app.callback(
    [Output('tutoria', 'className'), Output('tutoria', 'children'), Output('tutoria-state', 'data')],
    [Input('tutoria', 'n_clicks')],
    [State('tutoria-state', 'data')]
)
def toggle_tutoria(n, state):
    if n: 
        state = not state
    cls = 'toggle toggle-active' if state else 'toggle'
    txt = [html.Span('📚'), html.Span(f'Recibe Tutorías: {"Sí" if state else "No"}')]
    return cls, txt, state

# Callbacks para los chips
@app.callback(
    [Output('general', 'className'), Output('general-state', 'data')],
    [Input('general', 'n_clicks')],
    [State('general-state', 'data')]
)
def toggle_general(n, state):
    if n: 
        state = not state
    cls = 'chip chip-active' if state else 'chip'
    return cls, state

@app.callback(
    [Output('deportes', 'className'), Output('deportes-state', 'data')],
    [Input('deportes', 'n_clicks')],
    [State('deportes-state', 'data')]
)
def toggle_deportes(n, state):
    if n: 
        state = not state
    cls = 'chip chip-active' if state else 'chip'
    return cls, state

@app.callback(
    [Output('musica', 'className'), Output('musica-state', 'data')],
    [Input('musica', 'n_clicks')],
    [State('musica-state', 'data')]
)
def toggle_musica(n, state):
    if n: 
        state = not state
    cls = 'chip chip-active' if state else 'chip'
    return cls, state

# Callback principal para la predicción
@app.callback(
    [Output('donut', 'figure'),
     Output('score', 'children'),
     Output('percentage', 'children'),
     Output('risk', 'children'),
     Output('risk', 'className'),
     Output('message-container', 'children')],
    [Input('update', 'n_clicks')],
    [State('aus-state', 'data'),
     State('hrs-state', 'data'),
     State('apoyo-state', 'data'),
     State('tutoria-state', 'data'),
     State('general-state', 'data'),
     State('deportes-state', 'data'),
     State('musica-state', 'data')]
)
def predict_gpa(n, aus, hrs, ap, tut, gen, dep, mus):
    """Callback principal que llama a la API y actualiza la UI"""
    
    # Si no se ha hecho clic, mostrar estado inicial
    if not n:
        return (
            create_donut(0), 
            '--', 
            '--',
            [html.Div(className='risk-indicator'), html.Span('Sin Predicción')],
            'risk risk-medium',
            []
        )
    
    # Convertir booleanos a enteros
    tutoring = 1 if tut else 0
    parental = 1 if ap else 0
    extra = 1 if gen else 0
    sports = 1 if dep else 0
    music = 1 if mus else 0
    
    # Validar inputs
    valid, msg = validate_inputs(hrs, aus, tutoring, parental, extra, sports, music)
    if not valid:
        error_msg = html.Div(msg, className='message message-error')
        return (
            create_donut(0),
            '--',
            '--',
            [html.Div(className='risk-indicator'), html.Span('Error')],
            'risk risk-high',
            error_msg
        )
    
    # Llamar a la API
    success, result = call_prediction_api(
        study_time=hrs,
        absences=aus,
        tutoring=tutoring,
        parental_support=parental,
        extracurricular=extra,
        sports=sports,
        music=music
    )
    
    # Manejar la respuesta
    if not success:
        error_msg = html.Div(f"⚠️ {result}", className='message message-error')
        return (
            create_donut(0),
            '--',
            '--',
            [html.Div(className='risk-indicator'), html.Span('Error API')],
            'risk risk-high',
            error_msg
        )
    
    # Predicción exitosa
    gpa = result
    
    # Asegurar que el GPA esté en el rango 0-4
    gpa = max(0.0, min(4.0, gpa))
    
    # Calcular porcentaje (0-4 GPA -> 0-100%)
    percentage = int((gpa / 4.0) * 100)
    
    # Determinar nivel de riesgo
    if gpa >= 3.0:
        risk_txt = [html.Div(className='risk-indicator'), html.Span('Riesgo Bajo')]
        risk_cls = 'risk risk-low'
    elif gpa >= 2.0:
        risk_txt = [html.Div(className='risk-indicator'), html.Span('Riesgo Medio')]
        risk_cls = 'risk risk-medium'
    else:
        risk_txt = [html.Div(className='risk-indicator'), html.Span('Riesgo Alto')]
        risk_cls = 'risk risk-high'
    
    return (
        create_donut(percentage),
        f'{gpa:.2f}',
        f'{percentage}%',
        risk_txt,
        risk_cls,
        []
    )

if __name__ == '__main__':
    print(f"🚀 Conectando a la API en: {API_URL}")
    app.run(debug=True)