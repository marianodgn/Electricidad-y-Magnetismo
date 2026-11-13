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
        .right-col { display: flex; flex-direction: column; gap: 15px; width: 440px; }

        canvas {
            background-color: #fff; border-radius: var(--border-radius);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1); border: 1px solid #ddd; width: 100%;
        }

        .panel {
            background: var(--panel-bg); padding: 20px; border-radius: var(--border-radius);
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
