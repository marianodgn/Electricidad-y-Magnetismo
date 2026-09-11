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
    st.write("Visualización del apantallamiento electrostático de un cascarón conductor esférico.")
    
    html_electro = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { background-color: #0b0c10; color: #c5c6c7; font-family: Arial, sans-serif; text-align: center; }
            canvas { background-color: #1f2833; border: 1px solid #45a29e; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.5); margin-top: 10px;}
        </style>
    </head>
    <body>
        <canvas id="simCanvas" width="600" height="400"></canvas>
        <script>
            const canvas = document.getElementById('simCanvas');
            const ctx = canvas.getContext('2d');
            
            // Parámetros del sistema
            const cx = 300, cy = 200; // Centro geométrico
            const R = 100; // Radio del cascarón
            const qx = cx + R/2, qy = cy; // Posición de la carga (+q) a R/2
            
            // 1. Dibujar líneas de campo exteriores (Uniformemente distribuidas)
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'rgba(102, 252, 241, 0.7)'; // Cyan neón
            for(let i=0; i<16; i++) {
                let ang = i * (Math.PI / 8);
                ctx.beginPath();
                // Arrancan en la pared externa y van hacia el infinito (radiales al centro)
                ctx.moveTo(cx + R * Math.cos(ang), cy + R * Math.sin(ang));
                ctx.lineTo(cx + (R + 150) * Math.cos(ang), cy + (R + 150) * Math.sin(ang));
                ctx.stroke();
            }

            // 2. Dibujar líneas de campo interiores (Asimétricas pero ortogonales)
            ctx.strokeStyle = 'rgba(255, 70, 85, 0.7)'; // Rojo suave
            for(let i=0; i<16; i++) {
                let ang = i * (Math.PI / 8);
                
                // Punto final en la pared interna
                let endX = cx + R * Math.cos(ang);
                let endY = cy + R * Math.sin(ang);
                
                // Truco físico/gráfico: Punto de control alineado al radio del círculo.
                // Esto fuerza matemáticamente a que la curva golpee la pared a 90 grados exactos.
                let cpX = cx + (R * 0.4) * Math.cos(ang);
                let cpY = cy + (R * 0.4) * Math.sin(ang);

                ctx.beginPath();
                ctx.moveTo(qx, qy); // Salen de la carga descentrada
                ctx.quadraticCurveTo(cpX, cpY, endX, endY);
                ctx.stroke();
            }

            // 3. Dibujar el cascarón conductor delgado
            ctx.beginPath();
            ctx.arc(cx, cy, R, 0, 2 * Math.PI);
            ctx.lineWidth = 6;
            ctx.strokeStyle = '#c5c6c7'; // Gris metalizado
            ctx.stroke();

            // 4. Dibujar la carga puntual positiva (+q)
            ctx.beginPath();
            ctx.arc(qx, qy, 10, 0, 2 * Math.PI);
            ctx.fillStyle = '#ff4655'; // Rojo vivo
            ctx.fill();
            
            // Signo positivo
            ctx.fillStyle = 'white';
            ctx.font = '16px Arial bold';
            ctx.fillText('+', qx - 5, qy + 5);
        </script>
    </body>
    </html>
    """
    components.html(html_electro, height=450, scrolling=False)

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
