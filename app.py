import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Configuración de la página
# ==========================================
st.set_page_config(page_title="Laboratorio de Física", page_icon="⚛️", layout="wide")

# ==========================================
# 2. SISTEMA DE AUTENTICACIÓN (La Puerta)
# ==========================================
def check_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown("<h2 style='text-align: center; color: #66fcf1; margin-top: 50px;'>🔒 Acceso Restringido - Laboratorio Virtual</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("<div style='background: rgba(31, 40, 51, 0.8); padding: 20px; border-radius: 10px; border: 1px solid #45a29e;'>", unsafe_allow_html=True)
            usuario = st.text_input("Usuario:")
            clave = st.text_input("Contraseña:", type="password")
            if st.button("INGRESAR AL LABORATORIO"):
                if usuario == "EYMUNGS" and clave == "2026GUILLERMO":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error("🚫 Credenciales incorrectas. Verifique mayúsculas y vuelva a intentar.")
            st.markdown("</div>", unsafe_allow_html=True)
        return False
    return True

# Si la persona no está validada, el código se frena acá y no lee lo de abajo
if not check_password():
    st.stop()

# ==========================================
# 3. Menú de Navegación Lateral
# ==========================================
st.sidebar.title("🎛️ Panel de Control")

# Botón para cerrar sesión por seguridad
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state["autenticado"] = False
    st.rerun()
    
st.sidebar.markdown("---")
st.sidebar.markdown("Seleccione el entorno virtual a ejecutar:")

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
# 4. Lógica de renderizado principal
# ==========================================
st.title(f"Laboratorio Virtual: {modulo_elegido}")
st.markdown("---")

# --- SIMULACIÓN 1 ---
if modulo_elegido == "⚡ Campo Electromagnético":
    st.write("Mueva el control deslizante para desplazar la carga $+q$ en el interior del cascarón. Observe cómo las líneas de campo exterior (en cyan) permanecen invariantes debido al apantallamiento electrostático, independientemente de la distribución asimétrica de la carga inducida en la pared interna.")
    
    html_electro_interactivo = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: #0b0c10; color: #c5c6c7; font-family: 'Segoe UI', sans-serif; text-align: center; margin-top: 10px; }
            canvas { background-color: #1f2833; border: 1px solid #45a29e; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            .controles { margin-top: 20px; padding: 15px; background: rgba(31, 40, 51, 0.8); border-radius: 8px; display: inline-block; border: 1px solid #45a29e;}
            input[type=range] { width: 300px; cursor: pointer; accent-color: #ff4655; }
            label { font-size: 16px; font-weight: bold; color: #66fcf1; }
        </style>
    </head>
    <body>
        <canvas id="simCanvas" width="600" height="400"></canvas>
        
        <div class="controles">
            <label for="posSlider">Posición de la Carga (+q): <span id="valorPos">R/2</span></label><br><br>
            <input type="range" id="posSlider" min="-80" max="80" value="50" step="1">
        </div>

        <script>
            const canvas = document.getElementById('simCanvas');
            const ctx = canvas.getContext('2d');
            const slider = document.getElementById('posSlider');
            const valorPos = document.getElementById('valorPos');
            
            const cx = 300, cy = 200; 
            const R = 100; 
            
            function dibujarEscena() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                let offset = parseFloat(slider.value);
                let qx = cx + offset;
                let qy = cy;
                
                let proporcion = (offset / R).toFixed(2);
                valorPos.innerText = (proporcion >= 0 ? "+" : "") + proporcion + " R";

                // Líneas exteriores
                ctx.lineWidth = 2;
                ctx.strokeStyle = 'rgba(102, 252, 241, 0.7)'; 
                for(let i=0; i<16; i++) {
                    let ang = i * (Math.PI / 8);
                    ctx.beginPath();
                    ctx.moveTo(cx + R * Math.cos(ang), cy + R * Math.sin(ang));
                    ctx.lineTo(cx + (R + 150) * Math.cos(ang), cy + (R + 150) * Math.sin(ang));
                    ctx.stroke();
                }

                // Líneas interiores
                ctx.strokeStyle = 'rgba(255, 70, 85, 0.8)';
                for(let i=0; i<16; i++) {
                    let ang = i * (Math.PI / 8);
                    let endX = cx + R * Math.cos(ang);
                    let endY = cy + R * Math.sin(ang);
                    
                    let tension = 0.4 + (Math.abs(offset) / R) * 0.2;
                    let cpX = cx + (R * tension) * Math.cos(ang);
                    let cpY = cy + (R * tension) * Math.sin(ang);

                    ctx.beginPath();
                    ctx.moveTo(qx, qy); 
                    ctx.quadraticCurveTo(cpX, cpY, endX, endY);
                    ctx.stroke();
                }

                // Cascarón
                ctx.beginPath();
                ctx.arc(cx, cy, R, 0, 2 * Math.PI);
                ctx.lineWidth = 6;
                ctx.strokeStyle = '#c5c6c7'; 
                ctx.stroke();

                // Carga +q
                ctx.beginPath();
                ctx.arc(qx, qy, 10, 0, 2 * Math.PI);
                ctx.fillStyle = '#ff4655';
                ctx.fill();
                
                ctx.fillStyle = 'white';
                ctx.font = '16px Arial bold';
                ctx.fillText('+', qx - 5, qy + 5);
            }

            slider.addEventListener('input', dibujarEscena);
            dibujarEscena();
        </script>
    </body>
    </html>
    """
    components.html(html_electro_interactivo, height=550, scrolling=False)

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
