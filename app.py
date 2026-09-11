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
        "⚡ Campo Electromagnético",
        "🌊 Tubo de Kundt (Ondas)",
        "☀️ Efecto Fotoeléctrico",
        "⚙️ Próximamente..."
    ]
)

# ==========================================
# 4. Renderizado principal
# ==========================================
st.title(f"Laboratorio Virtual: {modulo_elegido}")
st.markdown("---")

# ==========================================================
# MÓDULO 1: CAMPO ELECTROMAGNÉTICO
# Tres experiencias:
#   A) Superposición y punto donde E = 0
#   B) Mapa de potencial, campo y equipotenciales
#   C) Ley de Gauss
# ==========================================================
if modulo_elegido == "⚡ Campo Electromagnético":

    st.markdown(
        """
        Este entorno reúne tres experiencias de electrostática basadas en las
        **prácticas 1, 2 y 3** de la guía: superposición del campo eléctrico,
        relación entre potencial y campo, y Ley de Gauss.

        Las magnitudes mostradas son calculadas directamente en el navegador
        a partir de las expresiones físicas utilizadas en la guía.
        """
    )

    html_electro = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
    * { box-sizing: border-box; }

    body {
        margin: 0;
        padding: 10px;
        background: #0b0c10;
        color: #c5c6c7;
        font-family: "Segoe UI", Arial, sans-serif;
    }

    h2, h3 {
        color: #66fcf1;
        margin-top: 4px;
    }

    .intro {
        color: #c5c6c7;
        line-height: 1.5;
        max-width: 1100px;
        margin: 0 auto 16px auto;
    }

    .tabs {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin: 12px auto;
        max-width: 1100px;
    }

    .tab {
        flex: 1;
        min-width: 180px;
        padding: 12px 14px;
        background: #1f2833;
        color: #c5c6c7;
        border: 1px solid #45a29e;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 700;
    }

    .tab.active {
        background: #16212c;
        color: #66fcf1;
        box-shadow: 0 0 0 1px #66fcf1 inset;
    }

    .panel {
        display: none;
        max-width: 1100px;
        margin: 0 auto;
    }

    .panel.active {
        display: block;
    }

    .card {
        background: rgba(31, 40, 51, 0.88);
        border: 1px solid #45a29e;
        border-radius: 10px;
        padding: 14px;
        margin: 12px 0;
    }

    .controls {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 12px;
        align-items: end;
    }

    .control {
        background: rgba(11, 12, 16, 0.35);
        border: 1px solid #33434c;
        border-radius: 8px;
        padding: 10px;
    }

    label {
        display: block;
        color: #66fcf1;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 5px;
    }

    input[type="range"], select, button.small {
        width: 100%;
    }

    input[type="range"] {
        cursor: pointer;
        accent-color: #ff4655;
    }

    select, button.small {
        background: #0b0c10;
        color: #c5c6c7;
        border: 1px solid #45a29e;
        border-radius: 6px;
        padding: 8px;
    }

    button.small {
        cursor: pointer;
        font-weight: 700;
    }

    button.small:hover {
        color: #66fcf1;
        border-color: #66fcf1;
    }

    .value {
        color: #ffffff;
        font-weight: 700;
    }

    .physics {
        line-height: 1.55;
        font-size: 14px;
        color: #d4d8db;
    }

    .equation {
        font-family: "Cambria Math", "Times New Roman", serif;
        font-size: 18px;
        text-align: center;
        color: #ffffff;
        padding: 8px 0;
    }

    .canvas-wrap {
        text-align: center;
        overflow-x: auto;
    }

    canvas {
        background: #10151b;
        border: 1px solid #45a29e;
        border-radius: 8px;
        max-width: 100%;
        height: auto;
    }

    .readout-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-top: 12px;
    }

    .readout {
        padding: 10px;
        border-left: 3px solid #45a29e;
        background: rgba(11, 12, 16, 0.38);
        border-radius: 5px;
        min-height: 64px;
    }

    .readout-title {
        font-size: 12px;
        color: #9da5ab;
    }

    .readout-value {
        font-size: 16px;
        color: #ffffff;
        font-weight: 700;
        margin-top: 3px;
    }

    .good {
        color: #66fcf1;
        font-weight: 700;
    }

    .warning {
        color: #ffd166;
        font-weight: 700;
    }

    .legend {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        font-size: 13px;
        margin: 7px 0;
    }

    .legend span::before {
        content: "";
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 5px;
        vertical-align: -1px;
    }

    .legend .plus::before { background: #ff4655; }
    .legend .minus::before { background: #4aa8ff; }
    .legend .zero::before { background: #66fcf1; }

    .twocol {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }

    @media (max-width: 800px) {
        .twocol { grid-template-columns: 1fr; }
    }

    .table-wrap {
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }

    th, td {
        border-bottom: 1px solid #33434c;
        padding: 7px;
        text-align: right;
    }

    th {
        color: #66fcf1;
    }

    .note {
        font-size: 12px;
        color: #9da5ab;
        line-height: 1.5;
    }

    .status {
        padding: 9px 10px;
        background: rgba(102, 252, 241, 0.06);
        border: 1px solid rgba(102, 252, 241, 0.25);
        border-radius: 6px;
        line-height: 1.5;
    }
</style>
</head>

<body>

<div class="intro">
    <h2>⚡ Laboratorio de Electrostática</h2>
    <div class="physics">
        Seleccione una experiencia. En todas ellas se distingue entre el
        <b>modelo físico</b> y su representación gráfica. Las magnitudes se
        calculan con SI y se muestran también en unidades cómodas para la
        interpretación.
    </div>
</div>

<div class="tabs">
    <button class="tab active" data-tab="exp1">1 · Campo nulo</button>
    <button class="tab" data-tab="exp2">2 · Potencial y campo</button>
    <button class="tab" data-tab="exp3">3 · Ley de Gauss</button>
</div>

<!-- =======================================================
     EXPERIENCIA 1
======================================================= -->
<section id="exp1" class="panel active">

    <div class="card">
        <h3>1. Superposición: ¿dónde se anula el campo?</h3>

        <div class="physics">
            Se colocan dos cargas puntuales sobre el eje <i>x</i>. Para cada
            posición de una carga de prueba se calcula:
        </div>

        <div class="equation">
            E(x) = E<sub>1</sub>(x) + E<sub>2</sub>(x)
        </div>

        <div class="physics">
            y, para una carga de prueba <i>q</i><sub>0</sub>:
        </div>

        <div class="equation">
            F(x) = q<sub>0</sub>E(x)
        </div>

        <div class="controls">
            <div class="control">
                <label>q₁ (µC)</label>
                <input id="q1" type="range" min="-10" max="10" step="0.1" value="2">
                <div class="value" id="q1v"></div>
            </div>

            <div class="control">
                <label>q₂ (µC)</label>
                <input id="q2" type="range" min="-10" max="10" step="0.1" value="4">
                <div class="value" id="q2v"></div>
            </div>

            <div class="control">
                <label>x₁ (cm)</label>
                <input id="x1" type="range" min="-8" max="2" step="0.1" value="-2">
                <div class="value" id="x1v"></div>
            </div>

            <div class="control">
                <label>x₂ (cm)</label>
                <input id="x2" type="range" min="-2" max="8" step="0.1" value="2">
                <div class="value" id="x2v"></div>
            </div>

            <div class="control">
                <label>Carga de prueba q₀ (µC)</label>
                <input id="q0" type="range" min="-5" max="5" step="0.1" value="1">
                <div class="value" id="q0v"></div>
            </div>
        </div>

        <div class="canvas-wrap">
            <canvas id="axisCanvas" width="1000" height="430"></canvas>
        </div>

        <div class="legend">
            <span class="plus">Carga positiva</span>
            <span class="minus">Carga negativa</span>
            <span class="zero">Punto E = 0</span>
        </div>

        <div class="readout-grid">
            <div class="readout">
                <div class="readout-title">Punto de campo nulo</div>
                <div class="readout-value" id="zeroPoint">—</div>
            </div>

            <div class="readout">
                <div class="readout-title">Campo máximo del gráfico</div>
                <div class="readout-value" id="maxField">—</div>
            </div>

            <div class="readout">
                <div class="readout-title">Interpretación</div>
                <div class="readout-value" id="zeroMeaning">—</div>
            </div>
        </div>

        <div class="status" id="exp1Status"></div>

        <div class="card">
            <h3>Lectura física</h3>
            <div class="physics">
                El campo total se obtiene por <b>superposición vectorial</b>.
                El lugar donde <i>E = 0</i> no es necesariamente el punto medio:
                depende de los signos, magnitudes y posiciones de las cargas.
                En las zonas cercanas a una carga puntual el campo crece mucho,
                por eso el gráfico evita representar exactamente los puntos de
                singularidad.
            </div>
        </div>
    </div>
</section>

<!-- =======================================================
     EXPERIENCIA 2
======================================================= -->
<section id="exp2" class="panel">

    <div class="card">
        <h3>2. Mapa de potencial, equipotenciales y campo eléctrico</h3>

        <div class="physics">
            Esta experiencia conecta tres representaciones del mismo sistema:
            <b>potencial escalar V</b>, <b>líneas equipotenciales</b> y
            <b>campo eléctrico vectorial E</b>.
        </div>

        <div class="equation">
            V = Σ k q<sub>i</sub>/r<sub>i</sub>
            &nbsp;&nbsp;&nbsp; y &nbsp;&nbsp;&nbsp;
            <span>𝐄 = −∇V</span>
        </div>

        <div class="controls">
            <div class="control">
                <label>q₁ (µC)</label>
                <input id="mQ1" type="range" min="-5" max="5" step="0.1" value="2">
                <div class="value" id="mQ1v"></div>
            </div>

            <div class="control">
                <label>q₂ (µC)</label>
                <input id="mQ2" type="range" min="-5" max="5" step="0.1" value="-2">
                <div class="value" id="mQ2v"></div>
            </div>

            <div class="control">
                <label>Distancia horizontal (cm)</label>
                <input id="sep" type="range" min="2" max="12" step="0.1" value="6">
                <div class="value" id="sepv"></div>
            </div>

            <div class="control">
                <label>Escala de campo</label>
                <input id="fieldScale" type="range" min="0.2" max="2.5" step="0.1" value="1">
                <div class="value" id="fieldScalev"></div>
            </div>

            <div class="control">
                <label>Equipotenciales</label>
                <select id="levels">
                    <option value="10">10 niveles</option>
                    <option value="14" selected>14 niveles</option>
                    <option value="18">18 niveles</option>
                </select>
            </div>
        </div>

        <div class="canvas-wrap">
            <canvas id="mapCanvas" width="1000" height="650"></canvas>
        </div>

        <div class="legend">
            <span class="plus">Carga positiva</span>
            <span class="minus">Carga negativa</span>
            <span class="zero">Equipotenciales</span>
        </div>

        <div class="readout-grid">
            <div class="readout">
                <div class="readout-title">Regla de lectura</div>
                <div class="readout-value">E ⟂ equipotenciales</div>
            </div>

            <div class="readout">
                <div class="readout-title">Dirección hacia V creciente</div>
                <div class="readout-value">E apunta hacia V decreciente</div>
            </div>

            <div class="readout">
                <div class="readout-title">Potencial</div>
                <div class="readout-value" id="mapPotentialRange">—</div>
            </div>
        </div>

        <div class="status">
            <b>Observación:</b> el potencial es escalar y se suma algebraicamente;
            el campo es vectorial y se obtiene a partir del gradiente del potencial.
            Las líneas equipotenciales se dibujan como curvas de igual V.
        </div>
    </div>
</section>

<!-- =======================================================
     EXPERIENCIA 3
======================================================= -->
<section id="exp3" class="panel">

    <div class="card">
        <h3>3. Ley de Gauss: flujo y carga encerrada</h3>

        <div class="physics">
            La Ley de Gauss establece:
        </div>

        <div class="equation">
            Φ<sub>E</sub> = ∮ 𝐄 · d𝐀 = Q<sub>enc</sub>/ε₀
        </div>

        <div class="physics">
            La superficie gaussiana puede cambiar de tamaño o posición.
            Lo que determina el <b>flujo neto</b> es la carga encerrada.
            La magnitud del campo sobre una superficie puede, en cambio,
            dejar de ser uniforme.
        </div>

        <div class="controls">
            <div class="control">
                <label>Configuración</label>
                <select id="gaussMode">
                    <option value="centered" selected>Esfera: carga centrada</option>
                    <option value="offcenter">Esfera: carga desplazada</option>
                </select>
            </div>

            <div class="control">
                <label>Q (µC)</label>
                <input id="gQ" type="range" min="-10" max="10" step="0.1" value="3">
                <div class="value" id="gQv"></div>
            </div>

            <div class="control">
                <label>Radio gaussiano (cm)</label>
                <input id="gR" type="range" min="3" max="12" step="0.1" value="7">
                <div class="value" id="gRv"></div>
            </div>

            <div class="control">
                <label>Desplazamiento de la carga (cm)</label>
                <input id="gOffset" type="range" min="0" max="5" step="0.1" value="3">
                <div class="value" id="gOffsetv"></div>
            </div>
        </div>

        <div class="twocol">
            <div class="canvas-wrap">
                <canvas id="gaussCanvas" width="640" height="500"></canvas>
            </div>

            <div>
                <div class="readout-grid">
                    <div class="readout">
                        <div class="readout-title">Carga encerrada</div>
                        <div class="readout-value" id="qEnc">—</div>
                    </div>

                    <div class="readout">
                        <div class="readout-title">Flujo de Gauss</div>
                        <div class="readout-value" id="flux">—</div>
                    </div>

                    <div class="readout">
                        <div class="readout-title">E si la carga está centrada</div>
                        <div class="readout-value" id="eCentered">—</div>
                    </div>

                    <div class="readout">
                        <div class="readout-title">¿Campo uniforme sobre S?</div>
                        <div class="readout-value" id="uniformField">—</div>
                    </div>
                </div>

                <div class="card">
                    <h3>Comprobación conceptual</h3>
                    <div class="physics" id="gaussExplanation"></div>
                </div>

                <div class="card">
                    <h3>Valores de E sobre la superficie</h3>
                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>Ángulo</th>
                                    <th>|E| (N/C)</th>
                                </tr>
                            </thead>
                            <tbody id="gaussTable"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="note">
            Nota didáctica: el dibujo es una sección 2D de una esfera gaussiana
            3D. El flujo mostrado corresponde a la superficie cerrada esférica
            completa, para mantener consistente la Ley de Gauss.
        </div>
    </div>
</section>

<script>
(function () {
    const k = 8.9875517923e9;
    const eps0 = 8.8541878128e-12;

    // -----------------------------------------------------
    // Utilidades
    // -----------------------------------------------------
    function fmt(value, digits = 2) {
        if (!Number.isFinite(value)) return "—";
        return Number(value).toFixed(digits);
    }

    function signed(value, digits = 2) {
        if (!Number.isFinite(value)) return "—";
        const n = Number(value);
        return (n >= 0 ? "+" : "") + n.toFixed(digits);
    }

    function setText(id, value) {
        const el = document.getElementById(id);
        if (el) el.textContent = value;
    }

    function clamp(v, a, b) {
        return Math.max(a, Math.min(b, v));
    }

    // -----------------------------------------------------
    // Tabs
    // -----------------------------------------------------
    document.querySelectorAll(".tab").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            document.getElementById(btn.dataset.tab).classList.add("active");

            if (btn.dataset.tab === "exp2") drawMap();
            if (btn.dataset.tab === "exp3") drawGauss();
        });
    });

    // =====================================================
    // EXPERIENCIA 1: E = 0
    // =====================================================
    const axisCanvas = document.getElementById("axisCanvas");
    const ax = axisCanvas.getContext("2d");

    const exp1Inputs = ["q1", "q2", "x1", "x2", "q0"];

    function axisData() {
        const q1 = parseFloat(document.getElementById("q1").value) * 1e-6;
        const q2 = parseFloat(document.getElementById("q2").value) * 1e-6;
        const x1 = parseFloat(document.getElementById("x1").value) / 100;
        const x2 = parseFloat(document.getElementById("x2").value) / 100;
        const q0 = parseFloat(document.getElementById("q0").value) * 1e-6;

        return { q1, q2, x1, x2, q0 };
    }

    function field1D(x, q1, q2, x1, x2) {
        let E = 0;

        const r1 = x - x1;
        const r2 = x - x2;

        if (Math.abs(r1) > 1e-5) {
            E += k * q1 * Math.sign(r1) / (r1 * r1);
        }

        if (Math.abs(r2) > 1e-5) {
            E += k * q2 * Math.sign(r2) / (r2 * r2);
        }

        return E;
    }

    function findRoots(q1, q2, x1, x2) {
        const roots = [];
        const minX = -0.16;
        const maxX = 0.16;
        const N = 3000;

        let prevX = minX;
        let prev = field1D(prevX, q1, q2, x1, x2);

        for (let i = 1; i <= N; i++) {
            const x = minX + (maxX - minX) * i / N;

            if (
                Math.abs(x - x1) < 0.0003 ||
                Math.abs(x - x2) < 0.0003
            ) {
                prevX = x;
                prev = field1D(x + 0.0004, q1, q2, x1, x2);
                continue;
            }

            const current = field1D(x, q1, q2, x1, x2);

            if (
                Number.isFinite(prev) &&
                Number.isFinite(current) &&
                prev * current < 0
            ) {
                let a = prevX;
                let b = x;

                for (let j = 0; j < 45; j++) {
                    const m = (a + b) / 2;
                    const fm = field1D(m, q1, q2, x1, x2);

                    if (prev * fm <= 0) {
                        b = m;
                    } else {
                        a = m;
                        prev = fm;
                    }
                }

                const root = (a + b) / 2;

                if (
                    Math.abs(root - x1) > 0.0007 &&
                    Math.abs(root - x2) > 0.0007 &&
                    !roots.some(r => Math.abs(r - root) < 0.0008)
                ) {
                    roots.push(root);
                }
            }

            prevX = x;
            prev = current;
        }

        return roots;
    }

    function drawArrow(ctx, x1, y1, x2, y2, color, width=2) {
        const angle = Math.atan2(y2-y1, x2-x1);
        const head = 8;

        ctx.strokeStyle = color;
        ctx.fillStyle = color;
        ctx.lineWidth = width;

        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(x2, y2);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(x2, y2);
        ctx.lineTo(
            x2 - head * Math.cos(angle - Math.PI / 6),
            y2 - head * Math.sin(angle - Math.PI / 6)
        );
        ctx.lineTo(
            x2 - head * Math.cos(angle + Math.PI / 6),
            y2 - head * Math.sin(angle + Math.PI / 6)
        );
        ctx.closePath();
        ctx.fill();
    }

    function drawAxis() {
        const {q1, q2, x1, x2, q0} = axisData();
        const W = axisCanvas.width;
        const H = axisCanvas.height;

        ax.clearRect(0, 0, W, H);

        ax.fillStyle = "#10151b";
        ax.fillRect(0, 0, W, H);

        const minX = -0.16;
        const maxX = 0.16;

        const px = x =>
            80 + (x - minX) / (maxX - minX) * (W - 160);

        const axisY = 275;

        ax.strokeStyle = "#9da5ab";
        ax.lineWidth = 2;

        ax.beginPath();
        ax.moveTo(50, axisY);
        ax.lineTo(W-50, axisY);
        ax.stroke();

        drawArrow(
            ax,
            W-90,
            axisY,
            W-55,
            axisY,
            "#9da5ab",
            2
        );

        ax.fillStyle = "#9da5ab";
        ax.font = "12px Segoe UI";

        for (let cm = -15; cm <= 15; cm += 5) {
            const x = cm / 100;
            const xp = px(x);

            ax.beginPath();
            ax.moveTo(xp, axisY - 6);
            ax.lineTo(xp, axisY + 6);
            ax.stroke();

            ax.fillText(
                cm + " cm",
                xp - 17,
                axisY + 25
            );
        }

        function drawCharge(q, xMeters) {
            const xp = px(xMeters);
            const radius = 17;

            ax.beginPath();
            ax.arc(xp, axisY, radius, 0, Math.PI*2);
            ax.fillStyle = q >= 0 ? "#ff4655" : "#4aa8ff";
            ax.fill();

            ax.fillStyle = "#ffffff";
            ax.font = "bold 17px Segoe UI";
            ax.textAlign = "center";

            ax.fillText(
                q >= 0 ? "+" : "−",
                xp,
                axisY + 6
            );

            ax.font = "12px Segoe UI";
            ax.fillText(
                (q / 1e-6).toFixed(1) + " µC",
                xp,
                axisY - 29
            );
        }

        drawCharge(q1, x1);
        drawCharge(q2, x2);

        const sampleXs = [];

        for (let cm = -14; cm <= 14; cm += 1.2) {
            sampleXs.push(cm / 100);
        }

        let maxAbsE = 0;

        sampleXs.forEach(x => {
            const e = field1D(x, q1, q2, x1, x2);

            if (Number.isFinite(e)) {
                maxAbsE = Math.max(maxAbsE, Math.abs(e));
            }
        });

        const displayScale = 70 / Math.max(maxAbsE, 1);

        sampleXs.forEach(x => {
            if (
                Math.abs(x-x1) < 0.009 ||
                Math.abs(x-x2) < 0.009
            ) {
                return;
            }

            const e = field1D(x, q1, q2, x1, x2);

            if (!Number.isFinite(e)) {
                return;
            }

            const xp = px(x);
            const dir = Math.sign(e);
            const len = clamp(
                Math.abs(e) * displayScale,
                10,
                44
            );

            drawArrow(
                ax,
                xp - dir*len*0.5,
                165,
                xp + dir*len*0.5,
                165,
                "#66fcf1",
                2
            );
        });

        const plotTop = 70;

        ax.strokeStyle = "#33434c";
        ax.lineWidth = 1;

        ax.beginPath();
        ax.moveTo(60, 108);
        ax.lineTo(W-60, 108);
        ax.stroke();

        ax.strokeStyle = "#66fcf1";
        ax.lineWidth = 2;
        ax.beginPath();

        let started = false;

        for (let i = 0; i <= 900; i++) {
            const x =
                minX +
                (maxX-minX)*i/900;

            if (
                Math.abs(x-x1) < 0.0013 ||
                Math.abs(x-x2) < 0.0013
            ) {
                started = false;
                continue;
            }

            const E = field1D(
                x,
                q1,
                q2,
                x1,
                x2
            );

            if (!Number.isFinite(E)) {
                started = false;
                continue;
            }

            const normalized =
                Math.tanh(
                    E / Math.max(maxAbsE, 1)
                );

            const xp = px(x);
            const yp =
                108 -
                normalized * 34;

            if (!started) {
                ax.moveTo(xp, yp);
                started = true;
            } else {
                ax.lineTo(xp, yp);
            }
        }

        ax.stroke();

        ax.fillStyle = "#9da5ab";
        ax.font = "12px Segoe UI";
        ax.textAlign = "left";

        ax.fillText(
            "E(x) — signo y comportamiento relativo",
            65,
            plotTop + 5
        );

        const roots =
            findRoots(q1, q2, x1, x2);

        roots.forEach(r => {
            const xp = px(r);

            ax.beginPath();
            ax.arc(
                xp,
                axisY,
                7,
                0,
                Math.PI*2
            );

            ax.fillStyle = "#66fcf1";
            ax.fill();

            ax.strokeStyle = "#ffffff";
            ax.lineWidth = 1;
            ax.stroke();

            ax.fillStyle = "#66fcf1";
            ax.font = "bold 12px Segoe UI";
            ax.textAlign = "center";

            ax.fillText(
                "E = 0",
                xp,
                axisY + 50
            );

            ax.fillText(
                (r*100).toFixed(2) + " cm",
                xp,
                axisY + 66
            );
        });

        const q0x = 0.115;
        const E0 = field1D(
            q0x,
            q1,
            q2,
            x1,
            x2
        );

        const F0 = q0 * E0;

        ax.fillStyle = "#ffffff";
        ax.font = "13px Segoe UI";
        ax.textAlign = "left";

        ax.fillText(
            "Carga de prueba en x = 11,5 cm: " +
            (E0/1e5).toFixed(3) +
            " ×10⁵ N/C",
            65,
            385
        );

        ax.fillText(
            "F = " +
            (F0/1e-6).toFixed(3) +
            " µN",
            65,
            405
        );

        setText(
            "q1v",
            (q1/1e-6).toFixed(1) +
            " µC"
        );

        setText(
            "q2v",
            (q2/1e-6).toFixed(1) +
            " µC"
        );

        setText(
            "x1v",
            (x1*100).toFixed(1) +
            " cm"
        );

        setText(
            "x2v",
            (x2*100).toFixed(1) +
            " cm"
        );

        setText(
            "q0v",
            (q0/1e-6).toFixed(1) +
            " µC"
        );

        if (roots.length > 0) {
            setText(
                "zeroPoint",
                roots
                    .map(r =>
                        (r*100).toFixed(2) +
                        " cm"
                    )
                    .join("  |  ")
            );
        } else {
            setText(
                "zeroPoint",
                "No aparece un cero finito en el intervalo"
            );
        }

        setText(
            "maxField",
            (maxAbsE/1e5).toFixed(2) +
            " ×10⁵ N/C"
        );

        const sameSign = q1*q2 > 0;
        const oppositeSign = q1*q2 < 0;

        let meaning =
            "Depende de las cargas";

        if (sameSign) {
            meaning =
                "Para cargas del mismo signo, el cero queda entre ellas.";
        } else if (oppositeSign) {
            meaning =
                "Para signos opuestos, el comportamiento depende de |q₁|/|q₂|.";
        } else {
            meaning =
                "Una carga es nula: el sistema se reduce a una sola carga.";
        }

        setText(
            "zeroMeaning",
            meaning
        );

        let status = "";

        if (q1 === 0 || q2 === 0) {
            status =
                "Con una sola carga no existe un punto finito donde su campo se anule.";
        } else if (roots.length > 0) {
            status =
                "Se encontró al menos un punto donde las contribuciones de campo se cancelan vectorialmente.";
        } else {
            status =
                "En el intervalo mostrado no aparece un punto finito de campo nulo.";
        }

        document.getElementById(
            "exp1Status"
        ).innerHTML = status;
    }

    exp1Inputs.forEach(id => {
        document.getElementById(id)
            .addEventListener(
                "input",
                drawAxis
            );
    });

    // =====================================================
    // EXPERIENCIA 2: V, E y equipotenciales
    // =====================================================
    const mapCanvas =
        document.getElementById("mapCanvas");

    const mc =
        mapCanvas.getContext("2d");

    function potentialAt(
        x,
        y,
        q1,
        q2,
        x1,
        x2
    ) {
        const r1 =
            Math.hypot(
                x-x1,
                y
            );

        const r2 =
            Math.hypot(
                x-x2,
                y
            );

        let V = 0;

        if (r1 > 0.001) {
            V += k*q1/r1;
        }

        if (r2 > 0.001) {
            V += k*q2/r2;
        }

        return V;
    }

    function fieldAt(
        x,
        y,
        q1,
        q2,
        x1,
        x2
    ) {
        let Ex = 0;
        let Ey = 0;

        const dx1 = x-x1;
        const dy1 = y;
        const r1 =
            Math.hypot(
                dx1,
                dy1
            );

        const dx2 = x-x2;
        const dy2 = y;
        const r2 =
            Math.hypot(
                dx2,
                dy2
            );

        if (r1 > 0.001) {
            const f =
                k*q1 /
                (r1*r1*r1);

            Ex += f*dx1;
            Ey += f*dy1;
        }

        if (r2 > 0.001) {
            const f =
                k*q2 /
                (r2*r2*r2);

            Ex += f*dx2;
            Ey += f*dy2;
        }

        return {
            Ex,
            Ey
        };
    }

    function potentialColor(
        v,
        vMax
    ) {
        const t =
            clamp(
                v / vMax,
                -1,
                1
            );

        let r, g, b;

        if (t >= 0) {
            const a = t;

            r =
                120 +
                135*a;

            g =
                150 -
                115*a;

            b =
                210 -
                170*a;
        } else {
            const a = -t;

            r =
                120 -
                80*a;

            g =
                150 -
                55*a;

            b =
                210 +
                45*a;
        }

        return (
            `rgb(${r|0},${g|0},${b|0})`
        );
    }

    function mapPointToCanvas(
        x,
        y,
        W,
        H,
        span
    ) {
        const x0 = W/2;
        const y0 = H/2;

        const scale =
            Math.min(W, H) /
            (2*span);

        return {
            px: x0 + x*scale,
            py: y0 - y*scale,
            scale
        };
    }

    function drawChargeMap(
        ctx,
        x,
        y,
        q,
        W,
        H,
        span
    ) {
        const p =
            mapPointToCanvas(
                x,
                y,
                W,
                H,
                span
            );

        ctx.beginPath();

        ctx.arc(
            p.px,
            p.py,
            15,
            0,
            Math.PI*2
        );

        ctx.fillStyle =
            q >= 0
                ? "#ff4655"
                : "#4aa8ff";

        ctx.fill();

        ctx.fillStyle = "#ffffff";
        ctx.font =
            "bold 16px Segoe UI";

        ctx.textAlign = "center";

        ctx.fillText(
            q >= 0 ? "+" : "−",
            p.px,
            p.py + 5
        );

        ctx.font = "12px Segoe UI";

        ctx.fillText(
            (q/1e-6).toFixed(1) +
            " µC",
            p.px,
            p.py - 22
        );
    }

    function drawEquipotentialSegment(
        ctx,
        x1,
        y1,
        x2,
        y2,
        v1,
        v2,
        level,
        W,
        H,
        span
    ) {
        if (
            !Number.isFinite(v1) ||
            !Number.isFinite(v2)
        ) {
            return;
        }

        if (
            (v1 < level && v2 > level) ||
            (v1 > level && v2 < level)
        ) {
            const t =
                (level-v1) /
                (v2-v1);

            const x =
                x1 + t*(x2-x1);

            const y =
                y1 + t*(y2-y1);

            const p =
                mapPointToCanvas(
                    x,
                    y,
                    W,
                    H,
                    span
                );

            return {
                x,
                y,
                px: p.px,
                py: p.py
            };
        }

        return null;
    }

    function drawMap() {

        const q1 =
            parseFloat(
                document.getElementById("mQ1").value
            )*1e-6;

        const q2 =
            parseFloat(
                document.getElementById("mQ2").value
            )*1e-6;

        const separation =
            parseFloat(
                document.getElementById("sep").value
            )/100;

        const fieldScale =
            parseFloat(
                document.getElementById("fieldScale").value
            );

        const levelCount =
            parseInt(
                document.getElementById("levels").value
            );

        const W =
            mapCanvas.width;

        const H =
            mapCanvas.height;

        const span = 0.14;
        const grid = 42;

        const x1 =
            -separation/2;

        const x2 =
            separation/2;

        mc.clearRect(
            0,
            0,
            W,
            H
        );

        mc.fillStyle = "#10151b";

        mc.fillRect(
            0,
            0,
            W,
            H
        );

        const vals = [];

        let maxAbsV = 1;

        for (let j = 0; j < grid; j++) {

            vals[j] = [];

            const y =
                span -
                (2*span)*j /
                (grid-1);

            for (let i = 0; i < grid; i++) {

                const x =
                    -span +
                    (2*span)*i /
                    (grid-1);

                const V =
                    potentialAt(
                        x,
                        y,
                        q1,
                        q2,
                        x1,
                        x2
                    );

                vals[j][i] =
                    V;

                if (
                    Number.isFinite(V) &&
                    Math.abs(V) < 5e7
                ) {
                    maxAbsV =
                        Math.max(
                            maxAbsV,
                            Math.abs(V)
                        );
                }
            }
        }

        const cellW =
            W/grid;

        const cellH =
            H/grid;

        for (let j = 0; j < grid-1; j++) {

            const y =
                span -
                2*span*j /
                (grid-1);

            for (let i = 0; i < grid-1; i++) {

                const x =
                    -span +
                    2*span*i /
                    (grid-1);

                const V =
                    vals[j][i];

                if (
                    Math.abs(V) > 5e7
                ) {
                    continue;
                }

                mc.fillStyle =
                    potentialColor(
                        V,
                        maxAbsV
                    );

                mc.fillRect(
                    i*cellW,
                    j*cellH,
                    cellW+1,
                    cellH+1
                );
            }
        }

        // Equipotenciales
        let levels = [];

        const levelBase =
            Math.max(
                1000,
                maxAbsV*0.12
            );

        for (
            let n = 1;
            n <= levelCount/2;
            n++
        ) {
            const lv =
                levelBase +
                (maxAbsV-levelBase) *
                n /
                (levelCount/2);

            levels.push(lv);
            levels.push(-lv);
        }

        levels.push(0);

        levels.forEach(level => {

            mc.strokeStyle =
                level === 0
                    ? "#ffffff"
                    : "rgba(102,252,241,0.60)";

            mc.lineWidth =
                level === 0
                    ? 2
                    : 1;

            for (
                let j = 0;
                j < grid-1;
                j++
            ) {

                for (
                    let i = 0;
                    i < grid-1;
                    i++
                ) {

                    const xA =
                        -span +
                        2*span*i /
                        (grid-1);

                    const xB =
                        -span +
                        2*span*(i+1) /
                        (grid-1);

                    const yA =
                        span -
                        2*span*j /
                        (grid-1);

                    const yB =
                        span -
                        2*span*(j+1) /
                        (grid-1);

                    const vTL =
                        vals[j][i];

                    const vTR =
                        vals[j][i+1];

                    const vBR =
                        vals[j+1][i+1];

                    const vBL =
                        vals[j+1][i];

                    const pts = [];

                    const e1 =
                        drawEquipotentialSegment(
                            mc,
                            xA,
                            yA,
                            xB,
                            yA,
                            vTL,
                            vTR,
                            level,
                            W,
                            H,
                            span
                        );

                    const e2 =
                        drawEquipotentialSegment(
                            mc,
                            xB,
                            yA,
                            xB,
                            yB,
                            vTR,
                            vBR,
                            level,
                            W,
                            H,
                            span
                        );

                    const e3 =
                        drawEquipotentialSegment(
                            mc,
                            xA,
                            yB,
                            xB,
                            yB,
                            vBL,
                            vBR,
                            level,
                            W,
                            H,
                            span
                        );

                    const e4 =
                        drawEquipotentialSegment(
                            mc,
                            xA,
                            yA,
                            xA,
                            yB,
                            vTL,
                            vBL,
                            level,
                            W,
                            H,
                            span
                        );

                    [e1,e2,e3,e4]
                        .forEach(e => {
                            if (e) {
                                pts.push(e);
                            }
                        });

                    if (pts.length >= 2) {

                        mc.beginPath();

                        mc.moveTo(
                            pts[0].px,
                            pts[0].py
                        );

                        mc.lineTo(
                            pts[1].px,
                            pts[1].py
                        );

                        mc.stroke();
                    }

                    if (pts.length === 4) {

                        mc.beginPath();

                        mc.moveTo(
                            pts[2].px,
                            pts[2].py
                        );

                        mc.lineTo(
                            pts[3].px,
                            pts[3].py
                        );

                        mc.stroke();
                    }
                }
            }
        });

        // Campo vectorial
        const vecStep = 3;

        let maxE = 1;

        for (
            let j = 1;
            j < grid-1;
            j += vecStep
        ) {

            for (
                let i = 1;
                i < grid-1;
                i += vecStep
            ) {

                const x =
                    -span +
                    2*span*i /
                    (grid-1);

                const y =
                    span -
                    2*span*j /
                    (grid-1);

                const f =
                    fieldAt(
                        x,
                        y,
                        q1,
                        q2,
                        x1,
                        x2
                    );

                const mag =
                    Math.hypot(
                        f.Ex,
                        f.Ey
                    );

                if (
                    Number.isFinite(mag)
                ) {
                    maxE =
                        Math.max(
                            maxE,
                            Math.min(mag, 1e8)
                        );
                }
            }
        }

        for (
            let j = 2;
            j < grid-2;
            j += vecStep
        ) {

            for (
                let i = 2;
                i < grid-2;
                i += vecStep
            ) {

                const x =
                    -span +
                    2*span*i /
                    (grid-1);

                const y =
                    span -
                    2*span*j /
                    (grid-1);

                const f =
                    fieldAt(
                        x,
                        y,
                        q1,
                        q2,
                        x1,
                        x2
                    );

                const mag =
                    Math.hypot(
                        f.Ex,
                        f.Ey
                    );

                if (
                    !Number.isFinite(mag) ||
                    mag > 1e10
                ) {
                    continue;
                }

                const p =
                    mapPointToCanvas(
                        x,
                        y,
                        W,
                        H,
                        span
                    );

                const dirx =
                    f.Ex /
                    (mag || 1);

                const diry =
                    -f.Ey /
                    (mag || 1);

                const len =
                    7 +
                    fieldScale *
                    20 *
                    Math.tanh(
                        mag/maxE*3
                    );

                const tx =
                    p.px +
                    dirx*len;

                const ty =
                    p.py +
                    diry*len;

                drawArrow(
                    mc,
                    p.px,
                    p.py,
                    tx,
                    ty,
                    "rgba(255,255,255,0.65)",
                    1.4
                );
            }
        }

        // Cargas
        drawChargeMap(
            mc,
            x1,
            0,
            q1,
            W,
            H,
            span
        );

        drawChargeMap(
            mc,
            x2,
            0,
            q2,
            W,
            H,
            span
        );

        // Ejes
        mc.strokeStyle =
            "rgba(255,255,255,0.22)";

        mc.lineWidth = 1;

        const centerX =
            W/2;

        const centerY =
            H/2;

        mc.beginPath();

        mc.moveTo(
            0,
            centerY
        );

        mc.lineTo(
            W,
            centerY
        );

        mc.moveTo(
            centerX,
            0
        );

        mc.lineTo(
            centerX,
            H
        );

        mc.stroke();

        // Readouts
        setText(
            "mQ1v",
            (q1/1e-6).toFixed(1) +
            " µC"
        );

        setText(
            "mQ2v",
            (q2/1e-6).toFixed(1) +
            " µC"
        );

        setText(
            "sepv",
            (separation*100).toFixed(1) +
            " cm"
        );

        setText(
            "fieldScalev",
            fieldScale.toFixed(1) +
            "×"
        );

        const safeRange =
            maxAbsV;

        setText(
            "mapPotentialRange",
            "≈ " +
            signed(
                -safeRange/1000,
                0
            ) +
            " a " +
            signed(
                safeRange/1000,
                0
            ) +
            " kV"
        );
    }

    ["mQ1","mQ2","sep","fieldScale","levels"]
        .forEach(id => {

            document
                .getElementById(id)
                .addEventListener(
                    "input",
                    drawMap
                );

            document
                .getElementById(id)
                .addEventListener(
                    "change",
                    drawMap
                );
        });

    // =====================================================
    // EXPERIENCIA 3: Ley de Gauss
    // =====================================================
    const gaussCanvas =
        document.getElementById(
            "gaussCanvas"
        );

    const gc =
        gaussCanvas.getContext("2d");

    function gaussFieldOnSphere(
        theta,
        Q,
        R,
        offset
    ) {
        const r =
            Math.sqrt(
                R*R +
                offset*offset -
                2*R*offset*
                Math.cos(theta)
            );

        return Math.abs(
            k*Q/(r*r)
        );
    }

    function drawGauss() {

        const mode =
            document
                .getElementById("gaussMode")
                .value;

        const Q =
            parseFloat(
                document.getElementById("gQ").value
            )*1e-6;

        const R =
            parseFloat(
                document.getElementById("gR").value
            )/100;

        const offset =
            parseFloat(
                document.getElementById("gOffset").value
            )/100;

        const W =
            gaussCanvas.width;

        const H =
            gaussCanvas.height;

        gc.clearRect(
            0,
            0,
            W,
            H
        );

        gc.fillStyle = "#10151b";

        gc.fillRect(
            0,
            0,
            W,
            H
        );

        const cx = 320;
        const cy = 245;
        const drawR = 165;

        // Superficie gaussiana
        gc.beginPath();

        gc.arc(
            cx,
            cy,
            drawR,
            0,
            Math.PI*2
        );

        gc.fillStyle =
            "rgba(102,252,241,0.04)";

        gc.fill();

        gc.strokeStyle =
            "#66fcf1";

        gc.lineWidth = 3;

        gc.stroke();

        const effectiveOffset =
            mode === "centered"
                ? 0
                : offset;

        const qx =
            cx +
            drawR *
            (effectiveOffset / R);

        const qy = cy;

        gc.beginPath();

        gc.arc(
            qx,
            qy,
            15,
            0,
            Math.PI*2
        );

        gc.fillStyle =
            Q >= 0
                ? "#ff4655"
                : "#4aa8ff";

        gc.fill();

        gc.fillStyle =
            "#ffffff";

        gc.font =
            "bold 16px Segoe UI";

        gc.textAlign =
            "center";

        gc.fillText(
            Q >= 0 ? "+" : "−",
            qx,
            qy+5
        );

        gc.font =
            "12px Segoe UI";

        gc.fillText(
            (Q/1e-6).toFixed(1) +
            " µC",
            qx,
            qy-22
        );

        // Radio
        gc.strokeStyle =
            "rgba(255,255,255,0.4)";

        gc.lineWidth = 1.5;

        gc.beginPath();

        gc.moveTo(
            cx,
            cy
        );

        gc.lineTo(
            cx+drawR,
            cy
        );

        gc.stroke();

        gc.fillStyle =
            "#c5c6c7";

        gc.textAlign =
            "left";

        gc.font =
            "12px Segoe UI";

        gc.fillText(
            "superficie gaussiana",
            cx-drawR,
            cy-drawR-12
        );

        gc.fillText(
            "R",
            cx+drawR/2-5,
            cy-7
        );

        // Campo radial
        const n = 14;

        for (
            let i = 0;
            i < n;
            i++
        ) {

            const th =
                2*Math.PI*i/n;

            const px =
                cx +
                drawR *
                Math.cos(th);

            const py =
                cy +
                drawR *
                Math.sin(th);

            const deltaX =
                px-qx;

            const deltaY =
                py-qy;

            const norm =
                Math.hypot(
                    deltaX,
                    deltaY
                ) || 1;

            const ux =
                deltaX/norm;

            const uy =
                deltaY/norm;

            drawArrow(
                gc,
                px - ux*26,
                py - uy*26,
                px,
                py,
                "rgba(255,255,255,0.65)",
                1.5
            );
        }

        // Flujo exacto
        const Qenc =
            Q;

        const flux =
            Qenc/eps0;

        const Ecentrado =
            k*Math.abs(Q) /
            (R*R);

        setText(
            "qEnc",
            signed(
                Qenc/1e-6,
                3
            ) +
            " µC"
        );

        setText(
            "flux",
            flux.toExponential(3) +
            " N·m²/C"
        );

        setText(
            "eCentered",
            Ecentrado.toExponential(3) +
            " N/C"
        );

        const isUniform =
            mode === "centered";

        setText(
            "uniformField",
            isUniform
                ? "Sí, en la esfera"
                : "No"
        );

        if (mode === "centered") {

            document.getElementById(
                "gaussExplanation"
            ).innerHTML =
                "Con la carga en el centro, la simetría esférica hace que " +
                "|E| sea igual en todos los puntos de la superficie. Por eso " +
                "la integral se reduce a <b>Φ = E·4πR²</b>. El resultado coincide " +
                "con <b>Q/ε₀</b>.";

        } else {

            document.getElementById(
                "gaussExplanation"
            ).innerHTML =
                "Al desplazar la carga, el campo <b>ya no es uniforme</b> sobre " +
                "la esfera. Sin embargo, como la carga continúa completamente " +
                "encerrada, el flujo neto de la superficie cerrada sigue siendo " +
                "<b>Φ = Q/ε₀</b>. Esto muestra por qué la Ley de Gauss no exige " +
                "que el campo sea uniforme: la integral incluye la variación " +
                "del campo y del producto escalar con dA.";
        }

        const tbody =
            document.getElementById(
                "gaussTable"
            );

        tbody.innerHTML = "";

        for (
            let i = 0;
            i < 8;
            i++
        ) {

            const th =
                2*Math.PI*i/8;

            const E =
                gaussFieldOnSphere(
                    th,
                    Q,
                    R,
                    effectiveOffset
                );

            const tr =
                document.createElement(
                    "tr"
                );

            const td1 =
                document.createElement(
                    "td"
                );

            const td2 =
                document.createElement(
                    "td"
                );

            td1.textContent =
                (th*180/Math.PI)
                    .toFixed(0) +
                "°";

            td2.textContent =
                E.toExponential(3);

            tr.appendChild(td1);
            tr.appendChild(td2);

            tbody.appendChild(tr);
        }
    }

    ["gaussMode","gQ","gR","gOffset"]
        .forEach(id => {

            document
                .getElementById(id)
                .addEventListener(
                    "input",
                    drawGauss
                );

            document
                .getElementById(id)
                .addEventListener(
                    "change",
                    drawGauss
                );
        });

    // Inicialización
    drawAxis();
    drawMap();
    drawGauss();

})();
</script>

</body>
</html>
"""

    components.html(
        html_electro,
        height=1650,
        scrolling=True
    )

# ==========================================================
# MÓDULO 2: TUBO DE KUNDT
# ==========================================================
elif modulo_elegido == "🌊 Tubo de Kundt (Ondas)":

    st.write(
        "Interfaz para visualización de ondas estacionarias y medición de nodos acústicos."
    )

    html_ondas = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                background-color: #0b0c10;
                color: #66fcf1;
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }

            .onda {
                width: 80%;
                height: 50px;
                background: repeating-linear-gradient(
                    90deg,
                    #0b0c10,
                    #45a29e 20px,
                    #0b0c10 40px
                );
                margin: 0 auto;
                border-radius: 25px;
            }
        </style>
    </head>

    <body>
        <h2>🌊 Entorno de Acústica</h2>
        <div class="onda"></div>
        <p>
            (Aquí incrustarás los controles del actuador y el micrófono)
        </p>
    </body>
    </html>
    """

    components.html(
        html_ondas,
        height=400,
        scrolling=True
    )

# ==========================================================
# MÓDULO 3: EFECTO FOTOELÉCTRICO
# ==========================================================
elif modulo_elegido == "☀️ Efecto Fotoeléctrico":

    st.write(
        "Análisis de emisión de electrones mediante excitación por fotones."
    )

    html_foto = """
    <div style="
        background-color:#0b0c10;
        color:#c5c6c7;
        text-align:center;
        padding:50px;
        border:1px solid #66fcf1;
    ">
        <h3 style="color:#66fcf1;">
            ☀️ Entorno Cuántico
        </h3>

        <p>
            Espacio reservado para la simulación del efecto fotoeléctrico.
        </p>
    </div>
    """

    components.html(
        html_foto,
        height=400,
        scrolling=True
    )

# ==========================================================
# MÓDULO 4: PRÓXIMAMENTE
# ==========================================================
else:
    st.info(
        "Este módulo se encuentra actualmente en desarrollo. Vuelva pronto."
    )
