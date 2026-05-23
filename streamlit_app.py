import streamlit as st

# --- 1. CONFIGURACIÓN Y ESTADO INICIAL (KISS) ---
# Lista maestra: (Nombre para mostrar, Valor multiplicador, ID interno)
PASOS = [
    ("Monedas de 2 €", 2.0, "2e"), ("Monedas de 1 €", 1.0, "1e"), 
    ("Monedas de 50 Cent", 0.50, "50c"), ("Monedas de 20 Cent", 0.20, "20c"), 
    ("Monedas de 10 Cent", 0.10, "10c"), ("Monedas de 5 Cent", 0.05, "5c"), 
    ("Monedas de 2 Cent", 0.02, "2c"), ("Monedas de 1 Cent", 0.01, "1c"), 
    ("Billetes de 50 €", 50.0, "50b"), ("Billetes de 20 €", 20.0, "20b"), 
    ("Billetes de 10 €", 10.0, "10b"), ("Billetes de 5 €", 5.0, "5b")
]

# Inicializar los 3 únicos estados necesarios
if "paso" not in st.session_state:
    st.session_state.paso = 0 # En qué moneda estamos (0 a 11)
    st.session_state.teclado = "" # Lo que se está tecleando ahora mismo
    st.session_state.cantidades = {item[2]: 0 for item in PASOS} # Diccionario con los totales

# --- 2. FUNCIONES DE LOS BOTONES (CALLBACKS) ---
def teclear(digito):
    st.session_state.teclado += digito

def borrar():
    st.session_state.teclado = st.session_state.teclado[:-1]

def avanzar():
    # 1. Guardar lo tecleado en el diccionario
    id_actual = PASOS[st.session_state.paso][2]
    valor_input = int(st.session_state.teclado) if st.session_state.teclado else 0
    st.session_state.cantidades[id_actual] = valor_input
    
    # 2. Pasar a la siguiente moneda (si no es la última)
    if st.session_state.paso < len(PASOS) - 1:
        st.session_state.paso += 1
        # Cargar lo que ya hubiera guardado antes (por si está editando)
        siguiente_id = PASOS[st.session_state.paso][2]
        cant_guardada = st.session_state.cantidades[siguiente_id]
        st.session_state.teclado = str(cant_guardada) if cant_guardada > 0 else ""

def retroceder():
    if st.session_state.paso > 0:
        st.session_state.paso -= 1
        # Cargar el número del paso anterior para poder editarlo
        id_anterior = PASOS[st.session_state.paso][2]
        cant_guardada = st.session_state.cantidades[id_anterior]
        st.session_state.teclado = str(cant_guardada) if cant_guardada > 0 else ""

def reset_todo():
    st.session_state.paso = 0
    st.session_state.teclado = ""
    st.session_state.cantidades = {item[2]: 0 for item in PASOS}

@st.dialog("⚠️ ¿Reiniciar conteo?")
def modal_confirmar_reset():
    st.write("¿Estás seguro de que quieres borrar todos los datos y volver a empezar?")
    
    col_si, col_no = st.columns(2)
    
    if col_si.button("Sí, borrar", type="primary",width="stretch"):
        reset_todo()
        st.rerun() # Recargamos la app para aplicar el borrado
        
    if col_no.button("Cancelar", type="secondary", width="stretch"):
        st.rerun() # Solo cerramos el pop-up sin hacer nada

# Pop-up final con las cuentas
# Pop-up final con las cuentas ordenadas
@st.dialog("📊 Resumen del Cierre")
def modal_resumen():
    # 1. PASO INVISIBLE: Calcular el total primero de fondo
    total = 0.0
    for _, multiplicador, id_moneda in PASOS:
        cant = st.session_state.cantidades[id_moneda]
        total += cant * multiplicador

    # 2. PASO VISUAL SUPERIOR: Mostrar los totales ya calculados arriba
    st.subheader(f"💰 Total Caja: {total:.2f} €")
    st.subheader(f"📦 A Declarar: {total - 100:.2f} €")
    st.divider()
    
    # 3. PASO VISUAL INFERIOR: Mostrar el desglose de lo que hay
    for nombre, multiplicador, id_moneda in PASOS:
        cant = st.session_state.cantidades[id_moneda]
        if cant > 0:
            subtotal = cant * multiplicador
            st.write(f"- {nombre}: {cant} unds. (**{subtotal:.2f} €**)")
# --- CSS DEFINITIVO ---
st.markdown("""
<style>
    /*---- HEADER OCULTO ----*/ 
    header[data-testid="stHeader"] {
        visibility: hidden;
        transition: opacity .3s ease;
    }
    header[data-testid="stHeader"]:hover {
        opacity: 1;
    }
    
    /* 1. CONTENEDOR PRINCIPAL: Seguridad de Scroll */
    .stMainBlockContainer {
        padding-top: 0rem !important;
        margin-top: -1rem !important;
        padding-bottom: 1rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important;
        overflow-y: auto !important; 
        overflow-x: hidden !important;
    }
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important; 
    }

    /* 2. REGLA PARA FILAS (Alinea la top bar y el teclado) */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            width: 100% !important;
            gap: 8px !important; 
            margin-bottom: 8px !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            flex: 1 1 0% !important; 
            min-width: 0 !important;
            margin: 0 !important; 
        }

        /* --- COMPRIMIR EL ENCABEZADO (Título) --- */
        div[data-testid="stHeadingWithActionElements"] {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            margin-bottom: -15px !important; 
        }
        hr[data-testid="stHeadingDivider"] {
            margin-top: 5px !important;
            margin-bottom: 5px !important;
        }

        /* =========================================
           ESTILOS DE BOTONES (Sin bombas nucleares)
           ========================================= */

        /* A. EL TECLADO (Regla base para los botones en columnas) */
        div[data-testid="stHorizontalBlock"] button {
            width: 100% !important;
            height: 9vh !important; 
            min-height: 45px !important; 
            max-height: 80px !important;
            border-radius: 10px !important;
            transition: background-color 0.1s !important;
            padding: 0 !important; 
        }
        div[data-testid="stHorizontalBlock"] button p {
            font-size: 30px !important; 
            font-weight: bold !important;
            margin: 0 !important;
        }

        /* B. EXCEPCIÓN: BOTÓN VOLVER (Usando su KEY) */
        /* Sumamos las clases para ganarle a la regla base del teclado */
        div[data-testid="stHorizontalBlock"] div.st-key-volver button {
            height: 6vh !important; 
            min-height: 35px !important;
            margin-bottom: -20px; 
            border-radius: 6px !important;
            background-color: transparent !important; /* Le quito el rojo, si quieres ponlo aquí */
        }
        div[data-testid="stHorizontalBlock"] div.st-key-volver button p {
            font-size: 14px !important;
            font-weight: normal !important;
        }
    }

    /* C. BOTONES DE ABAJO (Usando sus KEYS para no romper nada más) */
    div.st-key-contar button, div.st-key-reset button {
        height: 8vh !important; 
        min-height: 50px !important;
        border-radius: 8px !important;
    }
    div.st-key-contar button p, div.st-key-reset button p {
        font-size: 22px !important;
        font-weight: bold !important;
    }

    /* ========================================= */

    /* EL DISPLAY CENTRAL */
    .display-caja {
        background-color: transparent;
        color: #000;
        text-align: center;
        font-size: 50px; 
        font-weight: 300;
        margin-top: 0px;
        margin-bottom: 20px; 
        min-height: 60px;
        border: 2px solid #000; 
        border-radius: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* EFECTO IPHONE (Mantenido intacto) */
    button[kind="secondary"]:focus:not(:active) {
        background-color: transparent !important;
        border-color: rgba(49, 51, 63, 0.2) !important; 
    }
    button[kind="secondary"]:active {
        background-color: #e5e5ea !important; 
        border-color: #e5e5ea !important;
        transform: scale(0.99); 
    }
    /* =========================================
       EFECTO IPHONE PARA BOTONES PRIMARY
       ========================================= */

    /* 1. Fijamos el color base (Rojo Streamlit) para tomar el control */
    button[kind="primary"] {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
        color: white !important;
        transition: background-color 0.1s, transform 0.1s !important;
    }

    /* 2. Matamos el color pegajoso del focus (lo devolvemos al base) */
    button[kind="primary"]:focus:not(:active) {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
        color: white !important;
    }

    /* 3. El efecto al tocar la pantalla (Rojo más oscuro y hundimiento) */
    button[kind="primary"]:active {
        background-color: #e63939 !important; /* Rojo intenso */
        border-color: #e63939 !important;
        transform: scale(0.99) !important; 
    }
    /* --- EL DIVIDER (Línea separadora final) --- */
    div[data-testid="stMarkdownContainer"] hr {
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# --- INTERFAZ VISUAL ---

st.header("Contador", text_alignment="center", divider="green")

# ... (Tu CSS intocable sigue arriba) ...

# Extraemos la info del paso actual
nombre_moneda_actual = PASOS[st.session_state.paso][0]
texto_pantalla = st.session_state.teclado if st.session_state.teclado else "0"

# 1. BARRA SUPERIOR
col_volver, col_progreso = st.columns([1, 1])
with col_volver:
    # Se desactiva solo si estamos en el paso 0
    st.button("⬅ Volver", disabled=(st.session_state.paso == 0), on_click=retroceder, width="stretch", key="volver")
with col_progreso:
    st.markdown(f"<p style='text-align: right; color: gray; margin-top: 5px; font-weight: bold;'>Paso {st.session_state.paso + 1}/12</p>", unsafe_allow_html=True)

# 2. TÍTULO Y PANTALLA (Dinámicos)
st.markdown(f"<h3 style='text-align: center; color: #1f80cf; margin-bottom: 5px;'>{nombre_moneda_actual}</h3>", unsafe_allow_html=True)
st.markdown(f"<div class='display-caja'>{texto_pantalla}</div>", unsafe_allow_html=True)

# 3. EL TECLADO NUMÉRICO (Con los on_click)
c1, c2, c3 = st.columns(3)
c1.button("1", width="stretch", on_click=teclear, args=("1",))
c2.button("2", width="stretch", on_click=teclear, args=("2",))
c3.button("3", width="stretch", on_click=teclear, args=("3",))

c4, c5, c6 = st.columns(3)
c4.button("4", width="stretch", on_click=teclear, args=("4",))
c5.button("5", width="stretch", on_click=teclear, args=("5",))
c6.button("6", width="stretch", on_click=teclear, args=("6",))

c7, c8, c9 = st.columns(3)
c7.button("7", width="stretch", on_click=teclear, args=("7",))
c8.button("8", width="stretch", on_click=teclear, args=("8",))
c9.button("9", width="stretch", on_click=teclear, args=("9",))

c10, c11, c12 = st.columns(3)
c10.button("⌫", width="stretch", on_click=borrar)
c11.button("0", width="stretch", on_click=teclear, args=("0",))
c12.button("➔", type="primary", width="stretch", on_click=avanzar) 

st.divider() 

# 4. BOTONES FINALES DE ACCIÓN
if st.button("Contar Caja", type="primary", width="stretch", key="contar"):
    avanzar() # Guardamos el último número escrito antes de calcular
    modal_resumen() # Abrimos el pop-up

st.button("Reset", type="secondary", width="stretch", key="reset", on_click=modal_confirmar_reset)
