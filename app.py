import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Configuración de la página
# ==========================================
st.set_page_config(page_title="Laboratorio de Física", page_icon="⚛️", layout="wide")

# ==========================================
# 2. Menú de Navegación Lateral
# ==========================================
st.sidebar.title("🎛️ Panel de Control")
st.sidebar.markdown("Seleccione el entorno virtual a ejecutar:")

# Aquí agregas los nombres y los iconos (emojis) de tus simulaciones
modulo_elegido = st.sidebar.radio(
    "Módulos disponibles:",
    [
        "⚡ Campo Electromagnético",
        "🌊 Tubo de Kundt (Ondas)",
        "☀️ Efecto Fotoeléctrico",
        "⚙️ Próximamente..."
    ]
)

# ==========================================
# 3. Lógica de renderizado principal
# ==========================================
st.title(f"Laboratorio Virtual: {modulo_elegido}")
st.markdown("---")

# --- SIMULACIÓN 1 ---
if modulo_elegido == "⚡ Campo Electromagnético":
    st.write("Simulación interactiva de líneas de campo, flujo eléctrico y cargas puntuales.")
    
    html_electro = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: #0b0c10; color: #66fcf1; font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .caja { border: 2px dashed #45a29e; padding: 40px; border-radius: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="caja">
            <h2>⚡ Entorno de Electromagnetismo</h2>
            <p>(Aquí pegarás tu código HTML/JS con el canvas interactivo)</p>
        </div>
    </body>
    </html>
    """
    components.html(html_electro, height=400, scrolling=True)

# --- SIMULACIÓN 2 ---
elif modulo_elegido == "🌊 Tubo de Kundt (Ondas)":
    st.write("Interfaz para visualización de ondas estacionarias y medición de nodos acústicos.")
    
    html_ondas = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: #0b0c10; color: #66fcf1; font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
            .onda { width: 80%; height: 50px; background: repeating-linear-gradient(90deg, #0b0c10, #45a29e 20px, #0b0c10 40px); margin: 0 auto; border-radius: 25px;}
        </style>
    </head>
    <body>
        <h2>🌊 Entorno de Acústica</h2>
        <div class="onda"></div>
        <p>(Aquí incrustarás los controles del actuador y el micrófono)</p>
    </body>
    </html>
    """
    components.html(html_ondas, height=400, scrolling=True)

# --- SIMULACIÓN 3 ---
elif modulo_elegido == "☀️ Efecto Fotoeléctrico":
    st.write("Análisis de emisión de electrones mediante excitación por fotones.")
    
    html_foto = """
    <div style="background-color:#0b0c10; color:#c5c6c7; text-align:center; padding: 50px; border: 1px solid #66fcf1;">
        <h3>☀️ Entorno Cuántico</h3>
        <p>Espacio reservado para la simulación del efecto fotoeléctrico.</p>
    </div>
    """
    components.html(html_foto, height=400, scrolling=True)

# --- SIMULACIÓN VACÍA ---
else:
    st.info("Este módulo se encuentra actualmente en desarrollo. Vuelva pronto.")
