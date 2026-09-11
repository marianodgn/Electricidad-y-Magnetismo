import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de la página
st.set_page_config(page_title="Simulador Interactivo", page_icon="🔬", layout="wide")

st.title("🔬 Laboratorio Virtual de Simulaciones")
st.write("Seleccione la simulación visual en el panel para interactuar con los parámetros.")

st.markdown("---")

# 2. Tu código HTML / JavaScript (Aquí pegás tu simulación)
# Puse un ejemplo visual simple de un círculo como marcador de posición
codigo_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background-color: #0b0c10; color: #c5c6c7; font-family: Arial, sans-serif; text-align: center; }
        .pulsar {
            width: 50px; height: 50px; background: #66fcf1; border-radius: 50%; margin: 50px auto;
            animation: latido 1.5s infinite;
        }
        @keyframes latido {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 252, 241, 0.7); }
            70% { transform: scale(1.5); box-shadow: 0 0 0 15px rgba(102, 252, 241, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(102, 252, 241, 0); }
        }
    </style>
</head>
<body>
    <h3>Simulación en ejecución...</h3>
    <div class="pulsar"></div>
</body>
</html>
"""

# 3. El "Motor" que renderiza tu HTML dentro de Streamlit
# El height ajusta el alto de la ventana de la simulación
components.html(codigo_html, height=400, scrolling=True)
