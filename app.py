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
                
                // Obtenemos la posición desde el slider
                let offset = parseFloat(slider.value);
                let qx = cx + offset;
                let qy = cy;
                
                // Actualizar la etiqueta del texto
                let proporcion = (offset / R).toFixed(2);
                valorPos.innerText = (proporcion >= 0 ? "+" : "") + proporcion + " R";

                // 1. Dibujar líneas de campo exteriores (Invariantes)
                ctx.lineWidth = 2;
                ctx.strokeStyle = 'rgba(102, 252, 241, 0.7)'; 
                for(let i=0; i<16; i++) {
                    let ang = i * (Math.PI / 8);
                    ctx.beginPath();
                    ctx.moveTo(cx + R * Math.cos(ang), cy + R * Math.sin(ang));
                    ctx.lineTo(cx + (R + 150) * Math.cos(ang), cy + (R + 150) * Math.sin(ang));
                    ctx.stroke();
                }

                // 2. Dibujar líneas de campo interiores (Dinámicas)
                ctx.strokeStyle = 'rgba(255, 70, 85, 0.8)';
                for(let i=0; i<16; i++) {
                    let ang = i * (Math.PI / 8);
                    
                    let endX = cx + R * Math.cos(ang);
                    let endY = cy + R * Math.sin(ang);
                    
                    // Cálculo dinámico del punto de control para forzar incidencia normal (90 grados)
                    // Ajustamos la tensión de la curva en función de la distancia de la carga
                    let tension = 0.4 + (Math.abs(offset) / R) * 0.2;
                    let cpX = cx + (R * tension) * Math.cos(ang);
                    let cpY = cy + (R * tension) * Math.sin(ang);

                    ctx.beginPath();
                    ctx.moveTo(qx, qy); 
                    ctx.quadraticCurveTo(cpX, cpY, endX, endY);
                    ctx.stroke();
                }

                // 3. Cascarón conductor
                ctx.beginPath();
                ctx.arc(cx, cy, R, 0, 2 * Math.PI);
                ctx.lineWidth = 6;
                ctx.strokeStyle = '#c5c6c7'; 
                ctx.stroke();

                // 4. Carga puntual +q móvil
                ctx.beginPath();
                ctx.arc(qx, qy, 10, 0, 2 * Math.PI);
                ctx.fillStyle = '#ff4655';
                ctx.fill();
                
                ctx.fillStyle = 'white';
                ctx.font = '16px Arial bold';
                ctx.fillText('+', qx - 5, qy + 5);
            }

            // Escuchar cambios en el slider y redibujar al instante
            slider.addEventListener('input', dibujarEscena);
            
            // Dibujo inicial
            dibujarEscena();
        </script>
    </body>
    </html>
    """
    components.html(html_electro_interactivo, height=550, scrolling=False)
