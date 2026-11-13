import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. Configuración de la página
# ==========================================
st.set_page_config(
    page_title="Laboratorio de Física",
    page_icon="⚛️",
    layout="wide"
)

# ==========================================
# 2. SISTEMA DE AUTENTICACIÓN (La Puerta)
# ==========================================
def check_password():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.markdown(
            "<h2 style='text-align: center; color: #66fcf1; margin-top: 50px;'>"
            "🔒 Acceso Restringido - Laboratorio Virtual</h2>",
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.markdown(
                "<div style='background: rgba(31, 40, 51, 0.8); padding: 20px; "
                "border-radius: 10px; border: 1px solid #45a29e;'>",
                unsafe_allow_html=True
            )

            usuario = st.text_input("Usuario:")
            clave = st.text_input("Contraseña:", type="password")

            if st.button("INGRESAR AL LABORATORIO"):
                if usuario == "EYMUNGS" and clave == "2026GUILLERMO":
                    st.session_state["autenticado"] = True
                    st.rerun()
                else:
                    st.error(
                        "🚫 Credenciales incorrectas. Verifique mayúsculas "
                        "y vuelva a intentar."
                    )

            st.markdown("</div>", unsafe_allow_html=True)

        return False

    return True


if not check_password():
    st.stop()

# ==========================================
# 3. Menú de Navegación Lateral
# ==========================================
st.sidebar.title("🎛️ Panel de Control")

if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state["autenticado"] = False
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("Seleccione el entorno virtual a ejecutar:")

modulo_elegido = st.sidebar.radio(
    "Módulos disponibles:",
    [
        "🧲 Inducción Electromagnética"
    ]
)

# ==========================================
# 4. Renderizado principal
# ==========================================
st.title(f"Laboratorio Virtual: {modulo_elegido}")
st.markdown("---")

# ==========================================================
# MÓDULO ÚNICO: INDUCCIÓN ELECTROMAGNÉTICA
# ==========================================================
if modulo_elegido == "🧲 Inducción Electromagnética":

    st.markdown(
        """
        Análisis interactivo de ingreso y salida de espiras cuadradas en un campo magnético.
        La simulación permite visualizar la Ley de Faraday, la Ley de Lenz y la Fuerza de Lorentz en tiempo real.
        """
    )

    html_induccion = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --bg-color: #f0f2f5;
            --panel-bg: #ffffff;
            --text-color: #333333;
            --primary: #1a5276;
            --secondary: #2980b9;
            --accent: #e67e22;
            --danger: #c0392b;
            --success: #27ae60;
            --border-radius: 10px;
        }

        body {
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Pestañas */
        .tab-container { width: 100%; max-width: 1250px; margin-bottom: 20px; }
        .tabs { display: flex; gap: 5px; border-bottom: 2px solid var(--secondary); }
        .tab-btn {
            background-color: #e1e8ed; color: var(--text-color);
            border: none; padding: 12px 24px; font-size: 16px; font-weight: bold;
            cursor: pointer; border-radius: 8px 8px 0 0;
            transition: all 0.3s;
        }
        .tab-btn:hover { background-color: #d1d8dd; }
        .tab-btn.active { background-color: var(--secondary); color: white; }
        
        .tab-content { display: none; padding: 20px 0; }
        .tab-content.active { display: flex; }

        /* Contenedor principal de la Simulación */
        .sim-layout {
            display: flex; flex-direction: row; gap: 20px; width: 100%;
            justify-content: center; flex-wrap: wrap;
        }

        .left-col { display: flex; flex-direction: column; gap: 15px; flex: 1; max-width: 800px; }
        .right-col { display: flex; flex-direction: column; gap: 15px; width: 400px; }

        canvas {
            background-color: #fff; border-radius: var(--border-radius);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #ddd; width: 100%;
        }

        .panel {
            background: var(--panel-bg); padding: 20px; border-radius: var(--border-radius);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 12px;
        }

        .panel h2 { margin-top: 0; color: var(--primary); border-bottom: 2px solid var(--secondary); padding-bottom: 5px; font-size: 1.2em; }

        .control-group { display: flex; flex-direction: column; gap: 5px; margin-bottom: 8px; }
        .control-group label { font-weight: bold; font-size: 0.9em; display: flex; justify-content: space-between;}
        .control-group select, .control-group input { padding: 5px; border-radius: 5px; border: 1px solid #ccc; }
        .control-row { display: flex; gap: 15px; }
        .control-row > div { flex: 1; }

        .btn-row { display: flex; gap: 10px; margin-top: 10px; }
        button.action-btn {
            background-color: var(--secondary); color: white; border: none;
            padding: 10px; border-radius: 5px; cursor: pointer; font-weight: bold; flex: 1;
        }
        button.action-btn:hover { background-color: var(--primary); }
        button#btnReset { background-color: #95a5a6; }
        button#btnReset:hover { background-color: #7f8c8d; }

        .status-badge {
            display: inline-block; padding: 5px 10px; border-radius: 4px;
            color: white; font-weight: bold; text-transform: uppercase; font-size: 0.85em;
            background-color: var(--primary); text-align: center;
        }

        .math-block {
            background: #f8f9fa; padding: 15px; border-left: 4px solid var(--secondary);
            border-radius: 4px; font-family: "Courier New", Courier, monospace; font-size: 0.9em; line-height: 1.6;
        }

        .highlight { font-weight: bold; color: var(--danger); }
        .force-highlight { font-weight: bold; color: var(--success); }

        /* Estilos Teoría */
        .theory-content { background: white; padding: 30px; border-radius: var(--border-radius); box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; line-height: 1.6; font-size: 1.05em; }
        .theory-content h3 { color: var(--secondary); border-bottom: 1px solid #eee; padding-bottom: 5px; }
        .theory-content ul { padding-left: 20px; }
    </style>
</head>
<body>

    <div class="tab-container">
        <div class="tabs">
            <button class="tab-btn active" onclick="openTab(event, 'simulacion')">Simulación Interactiva</button>
            <button class="tab-btn" onclick="openTab(event, 'teoria')">Resumen Teórico</button>
        </div>

        <!-- PESTAÑA: SIMULACIÓN -->
        <div id="simulacion" class="tab-content active sim-layout">
            <div class="left-col">
                <canvas id="simCanvas" width="800" height="350"></canvas>
                
                <div class="panel">
                    <h2>Controles del Sistema</h2>
                    <div class="control-row">
                        <div class="control-group">
                            <label>Lado de la espira (L): <span id="sizeVal">0.10 m</span></label>
                            <input type="range" id="sizeSlider" min="0.05" max="0.15" step="0.01" value="0.10">
                        </div>
                        <div class="control-group">
                            <label>Nº Vueltas (N): <span id="nVal">10</span></label>
                            <input type="range" id="nSlider" min="1" max="50" step="1" value="10">
                        </div>
                        <div class="control-group">
                            <label>Velocidad (v): <span id="vVal">5 m/s</span></label>
                            <input type="range" id="vSlider" min="1" max="20" step="1" value="5">
                        </div>
                    </div>
                    <div class="control-row">
                        <div class="control-group">
                            <label>Intensidad del Campo (B): <span id="bVal">0.1 T</span></label>
                            <input type="range" id="bSlider" min="0" max="2" step="0.05" value="0.1">
                        </div>
                        <div class="control-group">
                            <label>Dirección del Campo (B):</label>
                            <select id="dirSelect">
                                <option value="z_out">+Z (Saliente ⊙)</option>
                                <option value="z_in">-Z (Entrante ⊗)</option>
                                <option value="x">+X (Derecha →)</option>
                                <option value="y">+Y (Arriba ↑)</option>
                            </select>
                        </div>
                    </div>
                    <div class="btn-row">
                        <button id="btnPlay" class="action-btn">Pausar</button>
                        <button id="btnReset" class="action-btn">Reiniciar Cruce</button>
                    </div>
                </div>
            </div>

            <div class="right-col">
                <div class="panel" style="flex-grow: 1;">
                    <h2>Análisis Matemático Físico</h2>
                    <div style="display:flex; justify-content: space-between; align-items: center;">
                        <span>Estado:</span>
                        <span id="faseActual" class="status-badge">AFUERA</span>
                    </div>
                    <div class="math-block" id="mathDetails">
                        <!-- Generado por JS -->
                    </div>
                    <div id="explanationText" style="font-size: 0.9em; color: #555; margin-top: 10px; background: #fdf2e9; padding: 10px; border-radius: 5px; border-left: 4px solid var(--accent);">
                        <!-- Explicación conceptual -->
                    </div>
                </div>
            </div>
        </div>

        <!-- PESTAÑA: TEORÍA -->
        <div id="teoria" class="tab-content">
            <div class="theory-content">
                <h2>Resumen Teórico: Inducción y Fuerzas Magnéticas</h2>
                
                <h3>1. Flujo Magnético (Φ)</h3>
                <p>El flujo magnético mide la cantidad de líneas de campo que atraviesan el área de la espira. Se calcula como el producto escalar entre el vector Campo Magnético (B) y el vector Área (A, que es perpendicular a la superficie de la espira).</p>
                <p><b>Φ = B · A · cos(θ)</b></p>
                <p><i>Nota clave:</i> Si el campo magnético apunta en el eje X (derecha) o Y (arriba), es paralelo a la superficie del monitor (θ = 90° con la normal). El flujo es 0 y no habrá inducción. El campo <b>debe</b> tener componente Z (entrante o saliente) para generar flujo.</p>

                <h3>2. Ley de Faraday</h3>
                <p>Establece que la fuerza electromotriz (fem, ε) inducida en un circuito es directamente proporcional a la rapidez con que cambia el flujo magnético en el tiempo.</p>
                <p><b>ε<sub>ind</sub> = - N · (dΦ / dt)</b> (donde N es el número de espiras)</p>
                <ul>
                    <li>Si la espira <b>ingresa</b> al campo, el área dentro del campo aumenta, el flujo aumenta.</li>
                    <li>Si la espira <b>sale</b> del campo, el área dentro del campo disminuye, el flujo disminuye.</li>
                    <li>Si está totalmente adentro o afuera, el flujo es constante y <b>ε<sub>ind</sub> = 0</b>.</li>
                </ul>

                <h3>3. Ley de Lenz</h3>
                <p>El signo negativo en la Ley de Faraday es la Ley de Lenz. Nos dice que la corriente inducida tendrá un sentido tal que generará un campo magnético propio que se <b>opondrá</b> al cambio de flujo original.</p>
                <ul>
                    <li><i>Ejemplo:</i> Si entras a un campo Saliente, el flujo saliente aumenta. La espira crea un campo Entrante para compensar, induciendo corriente Horaria.</li>
                </ul>

                <h3>4. Fuerza de Lorentz (Fuerza Magnética)</h3>
                <p>Un cable con corriente (I) dentro de un campo magnético (B) experimenta una fuerza. Al cruzar la frontera del campo, solo un segmento transversal sufre esta fuerza (los segmentos superior e inferior sufren fuerzas que se cancelan verticalmente).</p>
                <p><b>F<sub>m</sub> = N · I · L<sub>efectivo</sub> · B</b> (dirección por regla de la mano derecha)</p>
                <p>Esta fuerza magnética <b>siempre se opone al movimiento</b> actuando como un freno magnético. Por ello, para mantener velocidad constante, una <b>Fuerza Externa (F<sub>ext</sub>)</b> debe ser aplicada de igual magnitud pero en sentido opuesto (F<sub>ext</sub> = -F<sub>m</sub>).</p>
            </div>
        </div>
    </div>

    <script>
        // --- GESTIÓN DE PESTAÑAS ---
        function openTab(evt, tabName) {
            let i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) tabcontent[i].style.display = "none";
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) tablinks[i].className = tablinks[i].className.replace(" active", "");
            document.getElementById(tabName).style.display = "flex";
            evt.currentTarget.className += " active";
        }

        // --- SISTEMA FÍSICO Y VARIABLES ---
        const canvas = document.getElementById('simCanvas');
        const ctx = canvas.getContext('2d');
        const pixelsPerMeter = 1000; 
        
        // Zonas de Campo (en metros)
        const B_startX = 0.3;
        const B_endX = 0.6;
        const Epila = 1;  // V (Impulsa corriente Horaria)
        const R_res = 10; // Ohms

        // Estados controlados por usuario
        let params = {
            size: 0.10, // Lado del cuadrado
            N: 10,
            v: 5,
            B: 0.1,
            dir: 'z_out'
        };

        // Estado Dinámico
        let cx = 0.1; 
        let isPlaying = true;
        let lastTime = 0;

        // --- ELEMENTOS DEL DOM ---
        const ui = {
            sizeSlider: document.getElementById('sizeSlider'),
            sizeVal: document.getElementById('sizeVal'),
            nSlider: document.getElementById('nSlider'),
            nVal: document.getElementById('nVal'),
            vSlider: document.getElementById('vSlider'),
            vVal: document.getElementById('vVal'),
            bSlider: document.getElementById('bSlider'),
            bVal: document.getElementById('bVal'),
            dirSelect: document.getElementById('dirSelect'),
            btnPlay: document.getElementById('btnPlay'),
            btnReset: document.getElementById('btnReset'),
            faseActual: document.getElementById('faseActual'),
            mathDetails: document.getElementById('mathDetails'),
            explanationText: document.getElementById('explanationText')
        };

        // --- EVENT LISTENER ---
        function updateParams() {
            params.size = parseFloat(ui.sizeSlider.value);
            params.N = parseInt(ui.nSlider.value);
            params.v = parseFloat(ui.vSlider.value);
            params.B = parseFloat(ui.bSlider.value);
            params.dir = ui.dirSelect.value;
            
            ui.sizeVal.innerText = params.size.toFixed(2) + " m";
            ui.nVal.innerText = params.N;
            ui.vVal.innerText = params.v + " m/s";
            ui.bVal.innerText = params.B.toFixed(2) + " T";
            
            updatePhysics();
            draw();
        }

        ui.sizeSlider.addEventListener('input', updateParams);
        ui.nSlider.addEventListener('input', updateParams);
        ui.vSlider.addEventListener('input', updateParams);
        ui.bSlider.addEventListener('input', updateParams);
        ui.dirSelect.addEventListener('change', updateParams);

        ui.btnPlay.addEventListener('click', () => {
            isPlaying = !isPlaying;
            ui.btnPlay.innerText = isPlaying ? "Pausar" : "Reanudar";
        });

        ui.btnReset.addEventListener('click', () => {
            cx = 0.05; 
            updatePhysics();
            draw();
        });

        // --- MOTOR FÍSICO ---
        function calculatePhysics() {
            let state = '';
            let ext = params.size / 2; 
            let leftEdge = cx - ext;
            let rightEdge = cx + ext;

            let Leff = params.size; 
            let dAdt = 0;           

            if (rightEdge < B_startX) {
                state = 'afuera_pre';
            } else if (leftEdge > B_endX) {
                state = 'afuera_post';
            } else if (rightEdge >= B_startX && leftEdge <= B_startX) {
                state = 'ingresando';
                dAdt = Leff * params.v; 
            } else if (rightEdge >= B_endX && leftEdge <= B_endX) {
                state = 'saliendo';
                dAdt = -Leff * params.v; 
            } else if (leftEdge >= B_startX && rightEdge <= B_endX) {
                state = 'adentro';
            }

            let Eind_cw = 0; 
            let isZFlux = (params.dir === 'z_out' || params.dir === 'z_in');
            let Bz = 0;
            if (params.dir === 'z_out') Bz = params.B;
            if (params.dir === 'z_in') Bz = -params.B;

            if (isZFlux && (state === 'ingresando' || state === 'saliendo')) {
                Eind_cw = params.N * Bz * dAdt;
            }

            let I = (Epila + Eind_cw) / R_res; 
            let Fx = 0; 
            
            if (isZFlux && Leff > 0) {
                if (state === 'ingresando') {
                    Fx = - I * Leff * Bz * params.N; 
                } 
                else if (state === 'saliendo') {
                    Fx = I * Leff * Bz * params.N;
                }
            }

            let Fext = -Fx;

            return { state, dAdt, Leff, Eind: Eind_cw, I, Fm: Fx, Fext };
        }

        // --- DIBUJO Y ACTUALIZACIÓN ---
        function update(time) {
            if (!lastTime) lastTime = time;
            const dt = (time - lastTime) / 1000;
            lastTime = time;

            if (isPlaying) {
                cx += params.v * dt * 0.005; 
                if (cx > 0.85) cx = 0.05; 
                updatePhysics();
            }
            draw();
            requestAnimationFrame(update);
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const cy = 175;
            
            const pxStartX = B_startX * pixelsPerMeter;
            const pxWidth = (B_endX - B_startX) * pixelsPerMeter;
            ctx.fillStyle = params.B > 0 ? '#e8f4f8' : '#fff';
            if (params.B > 0) ctx.fillRect(pxStartX, 20, pxWidth, 310);
            
            ctx.fillStyle = '#2980b9'; ctx.strokeStyle = '#2980b9'; ctx.lineWidth = 2;
            let spacing = 40;
            
            if (params.B > 0) {
                for (let x = pxStartX + 20; x < pxStartX + pxWidth; x += spacing) {
                    for (let y = 50; y < 300; y += spacing) {
                        ctx.beginPath();
                        if (params.dir === 'z_out') {
                            ctx.arc(x, y, 2, 0, Math.PI * 2); ctx.fill();
                            ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2); ctx.stroke();
                        } else if (params.dir === 'z_in') {
                            ctx.moveTo(x-5, y-5); ctx.lineTo(x+5, y+5);
                            ctx.moveTo(x+5, y-5); ctx.lineTo(x-5, y+5);
                            ctx.stroke();
                        } else if (params.dir === 'x') {
                            drawArrowDir(ctx, x-10, y, x+10, y);
                        } else if (params.dir === 'y') {
                            drawArrowDir(ctx, x, y+10, x, y-10);
                        }
                    }
                }
            }

            ctx.font = 'bold 16px Arial';
            let dirText = params.dir === 'z_out' ? '⊙ Saliente (+Z)' : params.dir === 'z_in' ? '⊗ Entrante (-Z)' : params.dir === 'x' ? '→ Derecha (+X)' : '↑ Arriba (+Y)';
            ctx.fillText(`B = ${params.B}T ${dirText}`, pxStartX + 10, 40);

            const p = calculatePhysics();
            const pxCx = cx * pixelsPerMeter;
            const pxSize = params.size * pixelsPerMeter;
            
            ctx.strokeStyle = '#c0392b'; ctx.lineWidth = 4;
            
            const left = pxCx - pxSize/2; 
            const right = pxCx + pxSize/2;
            const top = cy - pxSize/2; 
            const bot = cy + pxSize/2;
            
            ctx.beginPath();
            ctx.moveTo(left, top); ctx.lineTo(right, top); 
            ctx.lineTo(right, bot); 
            ctx.lineTo(left, bot); 
            ctx.lineTo(left, cy + 15); 
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(left, cy - 15); ctx.lineTo(left, top); 
            ctx.stroke();
            
            drawBattery(left, cy);
            drawCurrentArrows(pxCx, cy, pxSize, p.I);

            if ((p.state === 'ingresando' || p.state === 'saliendo') && Math.abs(p.Fm) > 0.001) {
                let fxX = p.state === 'ingresando' ? pxCx + pxSize/2 : pxCx - pxSize/2;
                
                ctx.strokeStyle = '#2980b9'; ctx.fillStyle = '#2980b9';
                let fmPx = p.Fm > 0 ? 50 : -50;
                drawArrowDir(ctx, fxX, cy, fxX + fmPx, cy);
                ctx.fillText('Fm', fxX + fmPx, cy - 10);

                ctx.strokeStyle = '#27ae60'; ctx.fillStyle = '#27ae60';
                let fextPx = p.Fext > 0 ? 50 : -50;
                let extPoint = p.state === 'ingresando' ? pxCx - pxSize : pxCx + pxSize; 
                drawArrowDir(ctx, extPoint, cy, extPoint + fextPx, cy);
                ctx.fillText('Fext', extPoint + fextPx, cy - 10);
            }
        }

        function drawBattery(x, y) {
            ctx.strokeStyle = '#000'; ctx.lineWidth = 3;
            ctx.beginPath(); ctx.moveTo(x - 12, y - 10); ctx.lineTo(x + 12, y - 10); ctx.stroke();
            ctx.lineWidth = 5;
            ctx.beginPath(); ctx.moveTo(x - 7, y + 10); ctx.lineTo(x + 7, y + 10); ctx.stroke();
            ctx.fillStyle = '#000'; ctx.font = '12px Arial'; ctx.fillText('1V', x - 25, y + 4);
        }

        function drawCurrentArrows(x, y, size, I) {
            if (Math.abs(I) < 0.001) return;
            ctx.fillStyle = '#e67e22'; ctx.font = 'bold 14px Arial';
            let off = size/2;
            if (I > 0) { 
                ctx.fillText('I →', x - 10, y - off - 10);
                ctx.fillText('↓ I', x + off + 10, y + 5);
            } else { 
                ctx.fillText('← I', x - 10, y - off - 10);
                ctx.fillText('I ↑', x + off + 10, y + 5);
            }
        }

        function drawArrowDir(context, fromx, fromy, tox, toy) {
            const headlen = 8;
            const dx = tox - fromx; const dy = toy - fromy;
            const angle = Math.atan2(dy, dx);
            context.beginPath(); context.moveTo(fromx, fromy); context.lineTo(tox, toy);
            context.lineTo(tox - headlen * Math.cos(angle - Math.PI/6), toy - headlen * Math.sin(angle - Math.PI/6));
            context.moveTo(tox, toy);
            context.lineTo(tox - headlen * Math.cos(angle + Math.PI/6), toy - headlen * Math.sin(angle + Math.PI/6));
            context.stroke();
        }

        // --- ACTUALIZACIÓN DE TEXTO MATEMÁTICO ---
        function updatePhysics() {
            const p = calculatePhysics();
            
            ui.faseActual.innerText = p.state.replace('_pre', '').replace('_post', '').toUpperCase();
            ui.faseActual.style.backgroundColor = (p.state === 'adentro') ? '#1a5276' : 
                                                  (p.state === 'ingresando' || p.state === 'saliendo') ? '#e67e22' : '#7f8c8d';

            let isZFlux = (params.dir === 'z_out' || params.dir === 'z_in');
            let dirI = p.I > 0 ? "(Horario)" : (p.I < 0 ? "(Anti-horario)" : "");
            
            let mathHTML = ``;
            let expText = ``;

            if (!isZFlux) {
                mathHTML = `
                    Campo B paralelo al área.<br>
                    Ángulo θ = 90° -> cos(90°) = 0<br>
                    Flujo (Φ) = <span class="highlight">0 Wb</span><br>
                    ε<sub>inducida</sub> = 0 V<br>
                    I = 1V / ${R_res}Ω = <b>${p.I.toFixed(2)} A</b> ${dirI}<br>
                    F<sub>magX</sub> = 0 N (No hay fuerza opositora horizontal)<br>
                `;
                expText = `Al estar el campo B alineado en X o Y, no hay líneas de campo atravesando la superficie de la espira. No existe flujo, y por tanto, no hay inducción electromagnética. La corriente es solo la de la batería.`;
            } 
            else if (p.state === 'afuera_pre' || p.state === 'afuera_post' || p.state === 'adentro') {
                mathHTML = `
                    Flujo (Φ): Constante<br>
                    Variación dΦ/dt = 0<br>
                    ε<sub>inducida</sub> = 0 V<br>
                    I = ε<sub>pila</sub> / R = 1 / 10 = <span class="highlight">${Math.abs(p.I).toFixed(3)} A</span> ${dirI}<br>
                    F<sub>mag</sub> = 0 N<br>
                    F<sub>ext</sub> = <span class="force-highlight">0 N</span>
                `;
                expText = p.state === 'adentro' ? `Estando totalmente adentro, el flujo es máximo pero no cambia (dΦ/dt = 0). Sin variación de flujo, no hay corriente inducida. La fuerza externa necesaria es nula.` : `La espira está fuera del campo. No hay flujo magnético.`;
            } 
            else {
                let faseTxt = p.state === 'ingresando' ? 'aumenta' : 'disminuye';
                mathHTML = `
                    Lado cortando líneas (L) = ${p.Leff.toFixed(3)} m<br>
                    El flujo (Φ) <b>${faseTxt}</b>.<br>
                    ε<sub>ind</sub> = N·B·L·v = ${params.N}·${params.B}·${p.Leff.toFixed(3)}·${params.v} = <b>${Math.abs(p.Eind).toFixed(2)} V</b><br>
                    I = (1V ${p.Eind > 0 ? '+' : '-'} ${Math.abs(p.Eind).toFixed(2)}) / 10 = <span class="highlight">${Math.abs(p.I).toFixed(3)} A</span> ${dirI}<br>
                    F<sub>mag</sub> = N·I·L·B = <b>${Math.abs(p.Fm).toFixed(4)} N</b> ${p.Fm > 0 ? '→' : '←'}<br>
                    F<sub>ext</sub> = <span class="force-highlight">${Math.abs(p.Fext).toFixed(4)} N</span> ${p.Fext > 0 ? '→' : (p.Fext < 0 ? '←' : '0 N')}
                `;
                
                let dirExt = p.Fext > 0 ? "la DERECHA" : "la IZQUIERDA";
                if (Math.abs(p.Fext) < 0.0001) dirExt = "ningún lado (F=0)";
                
                expText = `Al ${p.state}, el flujo magnético ${faseTxt}. Por la Ley de Lenz, se induce una fem de ${Math.abs(p.Eind).toFixed(2)}V. La fuerza magnética de frenado es ${Math.abs(p.Fm).toFixed(4)}N. Para mantener la velocidad, debes aplicar la misma fuerza hacia ${dirExt}.`;
            }
            
            ui.mathDetails.innerHTML = mathHTML;
            ui.explanationText.innerHTML = `<strong>Concepto:</strong> ${expText}`;
        }

        // --- INIT ---
        updateParams();
        requestAnimationFrame(update);

    </script>
</body>
</html>
"""

    # Se ajusta la altura para asegurar que la pestaña teórica y la app entren bien sin scroll interno molesto
    components.html(
        html_induccion,
        height=1100,
        scrolling=True
    )
