# ============================================================
# app.py
# Prototipo Streamlit - Entregable 3
# Proyecto: Análisis sociodemográfico de personas imputadas por robo en México
# Fuente: INEGI, EHRIIJ, 2018-2021
# ============================================================

import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns

# Intento opcional de usar Plotly para heatmaps
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Entregable 3 | Análisis sociodemográfico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FIG_DIR = BASE_DIR / "figuras"


# ============================================================
# RUTAS EXACTAS DE ARCHIVOS
# ============================================================

FIGURAS = {
    "roc_png": FIG_DIR / "CurvasRoc.png",
    "roc_svg": FIG_DIR / "CurvasRoc.svg",
    "importancia": FIG_DIR / "importancia_variables_modelos_arbol.png",
    "matrices_absolutas_png": FIG_DIR / "matrices_confusion_modelos_absolutas.png",
    "matrices_absolutas_svg": FIG_DIR / "matrices_confusion_modelos_absolutas.svg",
    "matrices_normalizadas_png": FIG_DIR / "matrices_confusion_modelos_normalizadas.png",
    "matrices_normalizadas_svg": FIG_DIR / "matrices_confusion_modelos_normalizadas.svg",
    "ablacion": FIG_DIR / "Ablación por subconjuntos de predictoras.png",
    "sensibilidad_territorial": FIG_DIR / "Prueba de sensibilidad a variables territoriales.png"
}

CSV = {
    "matriz_arbol_decision": DATA_DIR / "matriz_confusion_arbol_decision.csv",
    "matriz_mlp": DATA_DIR / "matriz_confusion_mlp.csv",
    "matriz_naive_bayes": DATA_DIR / "matriz_confusion_naive_bayes.csv",
    "matriz_random_forest": DATA_DIR / "matriz_confusion_random_forest.csv",
    "matriz_xgboost": DATA_DIR / "matriz_confusion_xgboost.csv",

    "matriz_norm_arbol_decision": DATA_DIR / "matriz_confusion_normalizada_arbol_decision.csv",
    "matriz_norm_mlp": DATA_DIR / "matriz_confusion_normalizada_mlp.csv",
    "matriz_norm_naive_bayes": DATA_DIR / "matriz_confusion_normalizada_naive_bayes.csv",
    "matriz_norm_random_forest": DATA_DIR / "matriz_confusion_normalizada_random_forest.csv",
    "matriz_norm_xgboost": DATA_DIR / "matriz_confusion_normalizada_xgboost.csv",

    "ablacion": DATA_DIR / "resultados_ablacion_predictoras.csv",
    "sensibilidad_geografica": DATA_DIR / "resultados_sensibilidad_geografica.csv",
    "errores": DATA_DIR / "tabla_errores_matrices_confusion.csv",
    "importancia_variables": DATA_DIR / "tabla_importancia_variables.csv"
}

MODELOS = {
    "Árbol de decisión": {
        "abs": CSV["matriz_arbol_decision"],
        "norm": CSV["matriz_norm_arbol_decision"]
    },
    "MLP": {
        "abs": CSV["matriz_mlp"],
        "norm": CSV["matriz_norm_mlp"]
    },
    "Naive Bayes": {
        "abs": CSV["matriz_naive_bayes"],
        "norm": CSV["matriz_norm_naive_bayes"]
    },
    "Random Forest": {
        "abs": CSV["matriz_random_forest"],
        "norm": CSV["matriz_norm_random_forest"]
    },
    "XGBoost": {
        "abs": CSV["matriz_xgboost"],
        "norm": CSV["matriz_norm_xgboost"]
    }
}


# ============================================================
# CSS PERSONALIZADO
# ============================================================

def aplicar_estilos():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #020617 0%, #030712 45%, #020617 100%);
            color: #F8FAFC;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
            border-right: 1px solid #334155;
        }

        section[data-testid="stSidebar"] * {
            color: #F8FAFC !important;
        }

        h1, h2, h3, h4 {
            color: #F8FAFC !important;
            font-weight: 800 !important;
        }

        p, li, span, div {
            color: #E5E7EB;
        }

        a {
            color: #38BDF8 !important;
        }

        button[data-baseweb="tab"] {
            color: #F8FAFC !important;
            font-weight: 600;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #38BDF8 !important;
            border-bottom: 2px solid #38BDF8 !important;
        }

        div[data-testid="stMetric"] {
            background-color: #0F172A;
            border: 1px solid #334155;
            padding: 1rem;
            border-radius: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }

        div[data-testid="stMetricLabel"] {
            color: #CBD5E1 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
        }

        .hero-card {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 55%, #111827 100%);
            border: 1px solid #334155;
            border-radius: 24px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        }

        .hero-title {
            font-size: 2.1rem;
            font-weight: 900;
            color: #F8FAFC;
            margin-bottom: 0.6rem;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            line-height: 1.7;
            color: #CBD5E1;
        }

        .card {
            background: #0F172A;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 1.3rem 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 12px 28px rgba(0,0,0,0.25);
        }

        .card-title {
            color: #38BDF8;
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }

        .card-text {
            color: #F8FAFC;
            font-size: 1rem;
            line-height: 1.7;
        }

        .note-card {
            background: linear-gradient(135deg, #111827 0%, #0F172A 100%);
            border: 1px solid #475569;
            border-left: 6px solid #38BDF8;
            border-radius: 18px;
            padding: 1.1rem 1.4rem;
            margin: 1rem 0;
            color: #E2E8F0;
            line-height: 1.7;
        }

        .warning-card {
            background: linear-gradient(135deg, rgba(120,53,15,0.78), rgba(15,23,42,0.96));
            border: 1px solid #F59E0B;
            border-left: 7px solid #F59E0B;
            border-radius: 18px;
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
            color: #FEF3C7;
            font-weight: 600;
            line-height: 1.7;
        }

        .success-card {
            background: linear-gradient(135deg, rgba(20,83,45,0.75), rgba(15,23,42,0.96));
            border: 1px solid #22C55E;
            border-left: 7px solid #22C55E;
            border-radius: 18px;
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
            color: #DCFCE7;
            font-weight: 600;
            line-height: 1.7;
        }

        .danger-card {
            background: linear-gradient(135deg, rgba(127,29,29,0.78), rgba(15,23,42,0.96));
            border: 1px solid #EF4444;
            border-left: 7px solid #EF4444;
            border-radius: 18px;
            padding: 1.2rem 1.5rem;
            margin: 1rem 0;
            color: #FEE2E2;
            font-weight: 600;
            line-height: 1.7;
        }

        .image-box {
            background: #0F172A;
            border: 1px solid #334155;
            border-radius: 20px;
            padding: 1rem;
            margin: 1rem 0 1.5rem 0;
        }

        .small-muted {
            color: #94A3B8;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        hr {
            border: none;
            border-top: 1px solid #334155;
            margin: 1.5rem 0;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            border: 1px solid #334155;
            overflow: hidden;
        }

        details {
            background-color: #0F172A !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            padding: 0.5rem;
        }

        details summary {
            color: #F8FAFC !important;
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


aplicar_estilos()


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def card(titulo, texto, icono="📌"):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-title">{icono} {titulo}</div>
            <div class="card-text">{texto}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def note_card(texto):
    texto = textwrap.dedent(texto).strip()

    st.markdown(
        f"""
<div class="note-card">
{texto}
</div>
        """,
        unsafe_allow_html=True
    )


def warning_card(texto):
    st.markdown(
        f"""
        <div class="warning-card">
            ⚠️ {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


def success_card(texto):
    st.markdown(
        f"""
        <div class="success-card">
            ✅ {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


def danger_card(texto):
    st.markdown(
        f"""
        <div class="danger-card">
            🚫 {texto}
        </div>
        """,
        unsafe_allow_html=True
    )


def leer_csv(ruta):
    """
    Lee CSV con varios encodings posibles para evitar errores con acentos.
    """
    if not ruta.exists():
        return None

    encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]

    for enc in encodings:
        try:
            return pd.read_csv(ruta, encoding=enc)
        except Exception:
            continue

    try:
        return pd.read_csv(ruta)
    except Exception:
        return None


def preparar_matriz_confusion(df):
    """
    Intenta preparar una matriz de confusión para visualizarla correctamente.
    Soporta CSV con índice guardado como primera columna.
    """
    if df is None or df.empty:
        return df

    df2 = df.copy()

    # Si la primera columna parece ser índice o etiquetas, se usa como índice.
    primera_col = df2.columns[0]

    if (
        "Unnamed" in str(primera_col)
        or str(primera_col).lower() in ["index", "clase", "categoria", "categoría", "real", "true"]
        or not pd.api.types.is_numeric_dtype(df2[primera_col])
    ):
        df2 = df2.set_index(primera_col)

    # Intentar convertir todo a numérico
    for col in df2.columns:
        df2[col] = pd.to_numeric(df2[col], errors="coerce")

    return df2


def mostrar_tabla(ruta, titulo=None, descripcion=None):
    if titulo:
        st.markdown(f"### {titulo}")

    if descripcion:
        st.write(descripcion)

    if not ruta.exists():
        warning_card(f"No se encontró el archivo: <strong>{ruta.name}</strong>")
        return None

    df = leer_csv(ruta)

    if df is None:
        warning_card(f"No se pudo leer el archivo: <strong>{ruta.name}</strong>")
        return None

    st.dataframe(df, use_container_width=True)

    with st.expander("📄 Información del archivo"):
        st.write(f"**Ruta:** `{ruta}`")
        st.write(f"**Filas:** {df.shape[0]}")
        st.write(f"**Columnas:** {df.shape[1]}")
        st.write("**Columnas detectadas:**")
        st.write(list(df.columns))

    return df


def mostrar_imagen(ruta, titulo=None, caption=None):
    if titulo:
        st.markdown(f"### {titulo}")

    if not ruta.exists():
        warning_card(f"No se encontró la figura: <strong>{ruta.name}</strong>")
        return False

    st.markdown('<div class="image-box">', unsafe_allow_html=True)

    try:
        if ruta.suffix.lower() == ".svg":
            st.image(str(ruta), caption=caption or ruta.name, use_container_width=True)
        else:
            img = Image.open(ruta)
            st.image(img, caption=caption or ruta.name, use_container_width=True)
    except Exception:
        st.image(str(ruta), caption=caption or ruta.name, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return True


def mostrar_heatmap_matriz(ruta, titulo, normalizada=False):
    st.markdown(f"### {titulo}")

    if not ruta.exists():
        warning_card(f"No se encontró el archivo: <strong>{ruta.name}</strong>")
        return None

    df = leer_csv(ruta)
    df_matriz = preparar_matriz_confusion(df)

    if df_matriz is None or df_matriz.empty:
        warning_card(f"No se pudo preparar la matriz: <strong>{ruta.name}</strong>")
        return None

    if PLOTLY_AVAILABLE:
        try:
            fig = px.imshow(
                df_matriz,
                text_auto=True,
                color_continuous_scale="Blues",
                aspect="auto",
                labels=dict(x="Clase predicha", y="Clase real", color="Valor")
            )

            fig.update_layout(
                paper_bgcolor="#020617",
                plot_bgcolor="#020617",
                font=dict(color="#F8FAFC"),
                margin=dict(l=40, r=40, t=40, b=40),
                coloraxis_colorbar=dict(
                    title="Proporción" if normalizada else "Frecuencia"
                )
            )

            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.dataframe(df_matriz, use_container_width=True)
    else:
        st.dataframe(df_matriz, use_container_width=True)

    with st.expander("📄 Ver datos de la matriz"):
        st.dataframe(df_matriz, use_container_width=True)

    return df_matriz


def calcular_metricas_desde_matriz(df_matriz):
    """
    Calcula métricas simples desde matriz de confusión multiclase:
    total, aciertos, errores, accuracy.
    """
    try:
        matriz = df_matriz.fillna(0).values
        total = matriz.sum()
        aciertos = matriz.diagonal().sum()
        errores = total - aciertos
        accuracy = aciertos / total if total > 0 else 0

        return {
            "total": total,
            "aciertos": aciertos,
            "errores": errores,
            "accuracy": accuracy
        }
    except Exception:
        return None


def listar_archivos_disponibles():
    archivos = []

    if DATA_DIR.exists():
        archivos.extend(list(DATA_DIR.glob("*")))

    if FIG_DIR.exists():
        archivos.extend(list(FIG_DIR.glob("*")))

    return sorted([a for a in archivos if a.is_file()])


def boton_descarga(ruta, key):
    if not ruta.exists():
        return

    with open(ruta, "rb") as f:
        data = f.read()

    mime = "application/octet-stream"

    if ruta.suffix.lower() == ".csv":
        mime = "text/csv"
    elif ruta.suffix.lower() == ".png":
        mime = "image/png"
    elif ruta.suffix.lower() == ".svg":
        mime = "image/svg+xml"

    st.download_button(
        label=f"⬇️ Descargar {ruta.name}",
        data=data,
        file_name=ruta.name,
        mime=mime,
        key=key
    )


def contar_existentes(diccionario):
    return sum(1 for _, ruta in diccionario.items() if ruta.exists())


#===================================================
#
#====================================================
def render_punto_3_evaluacion_modelos():
    st.markdown(
        """
        <h1 style='color:#F2F2F2;'>3. Evaluación comparativa de modelos</h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background-color:#1E1E1E;
            padding:18px;
            border-radius:12px;
            border-left:5px solid #2E86AB;
            color:#F2F2F2;
            margin-bottom:20px;">
            <h3>Propósito de la evaluación</h3>
            <p>
            En esta sección se comparan los modelos supervisados utilizados para analizar patrones
            sociodemográficos asociados con personas imputadas por robo. La evaluación considera
            matrices de confusión, métricas generales, errores de clasificación, sensibilidad e
            interpretación responsable de los resultados.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    modelos = {
        "Árbol de decisión": {
            "abs": "matriz_confusion_arbol_decision.csv",
            "norm": "matriz_confusion_normalizada_arbol_decision.csv"
        },
        "MLP": {
            "abs": "matriz_confusion_mlp.csv",
            "norm": "matriz_confusion_normalizada_mlp.csv"
        },
        "Naive Bayes": {
            "abs": "matriz_confusion_naive_bayes.csv",
            "norm": "matriz_confusion_normalizada_naive_bayes.csv"
        },
        "Random Forest": {
            "abs": "matriz_confusion_random_forest.csv",
            "norm": "matriz_confusion_normalizada_random_forest.csv"
        },
        "XGBoost": {
            "abs": "matriz_confusion_xgboost.csv",
            "norm": "matriz_confusion_normalizada_xgboost.csv"
        }
    }

    st.subheader("📊 Comparación general de modelos")

    resumen_modelos = []

    for nombre_modelo, archivos in modelos.items():
        ruta_matriz = DATA_DIR / archivos["abs"]

        if ruta_matriz.exists():
            matriz = pd.read_csv(ruta_matriz, index_col=0)

            total = matriz.values.sum()
            aciertos = matriz.values.diagonal().sum()
            accuracy = aciertos / total if total > 0 else 0

            resumen_modelos.append(
                {
                    "Modelo": nombre_modelo,
                    "Total de casos evaluados": int(total),
                    "Clasificaciones correctas": int(aciertos),
                    "Accuracy aproximado": round(accuracy, 4)
                }
            )

    if resumen_modelos:
        df_resumen = pd.DataFrame(resumen_modelos)
        st.dataframe(df_resumen, use_container_width=True)

        mejor_modelo = df_resumen.sort_values(
            "Accuracy aproximado",
            ascending=False
        ).iloc[0]

        st.markdown(
            f"""
            <div style="
                background-color:#16213E;
                padding:18px;
                border-radius:12px;
                border-left:5px solid #21BF73;
                color:#F2F2F2;
                margin-top:15px;
                margin-bottom:20px;">
                <h3>Modelo con mejor desempeño global</h3>
                <p><strong>Modelo:</strong> {mejor_modelo['Modelo']}</p>
                <p><strong>Accuracy aproximado:</strong> {mejor_modelo['Accuracy aproximado']}</p>
                <p>
                Este resultado debe interpretarse con cautela, ya que una métrica global alta no
                necesariamente implica ausencia de sesgos o buen desempeño en todos los grupos.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("No se encontraron matrices de confusión absolutas para calcular el resumen.")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🧮 Matrices de confusión",
            "📉 Figuras comparativas",
            "📋 Tabla de errores",
            "⚖️ Interpretación ética"
        ]
    )

    with tab1:
        st.subheader("🧮 Matrices de confusión por modelo")

        tipo_matriz = st.radio(
            "Selecciona el tipo de matriz:",
            ["Absoluta", "Normalizada"],
            horizontal=True
        )

        for nombre_modelo, archivos in modelos.items():
            st.markdown(f"### {nombre_modelo}")

            archivo = archivos["abs"] if tipo_matriz == "Absoluta" else archivos["norm"]
            ruta = DATA_DIR / archivo

            if ruta.exists():
                matriz = pd.read_csv(ruta, index_col=0)

                fig, ax = plt.subplots(figsize=(7, 4))

                if tipo_matriz == "Absoluta":
                    sns.heatmap(
                        matriz,
                        annot=True,
                        fmt="g",
                        cmap="Blues",
                        cbar=True,
                        ax=ax
                    )
                else:
                    sns.heatmap(
                        matriz,
                        annot=True,
                        fmt=".2f",
                        cmap="Purples",
                        cbar=True,
                        ax=ax
                    )

                ax.set_xlabel("Clase predicha")
                ax.set_ylabel("Clase real")
                ax.set_title(f"Matriz de confusión {tipo_matriz.lower()} - {nombre_modelo}")

                st.pyplot(fig)
            else:
                st.warning(f"No se encontró el archivo: {archivo}")

    with tab2:
        st.subheader("📉 Figuras comparativas generadas en Python")

        figuras = {
            "Matrices de confusión absolutas": "matrices_confusion_modelos_absolutas.png",
            "Matrices de confusión normalizadas": "matrices_confusion_modelos_normalizadas.png",
            "Curvas ROC comparativas": "CurvasRoc.png",
            "Curvas ROC en formato SVG": "CurvasRoc.svg",
            "Importancia de variables en modelos de árbol": "importancia_variables_modelos_arbol.png",
            "Prueba de sensibilidad a variables territoriales": "Prueba de sensibilidad a variables territoriales.png",
            "Ablación por subconjuntos de predictoras": "Ablación por subconjuntos de predictoras.png"
        }

        for titulo, archivo in figuras.items():
            ruta_figura = FIG_DIR / archivo

            if ruta_figura.exists():
                st.markdown(f"### {titulo}")
                st.image(str(ruta_figura), use_container_width=True)
            else:
                st.info(f"No se encontró la figura: {archivo}")

    with tab3:
        st.subheader("📋 Tabla de errores y resultados complementarios")

        ruta_errores = DATA_DIR / "tabla_errores_matrices_confusion.csv"

        if ruta_errores.exists():
            df_errores = pd.read_csv(ruta_errores)
            st.markdown("### Errores derivados de matrices de confusión")
            st.dataframe(df_errores, use_container_width=True)
        else:
            st.warning("No se encontró el archivo tabla_errores_matrices_confusion.csv")

        ruta_ablacion = DATA_DIR / "resultados_ablacion_predictoras.csv"

        if ruta_ablacion.exists():
            df_ablacion = pd.read_csv(ruta_ablacion)
            st.markdown("### Resultados de ablación de predictoras")
            st.dataframe(df_ablacion, use_container_width=True)

        ruta_sensibilidad = DATA_DIR / "resultados_sensibilidad_geografica.csv"

        if ruta_sensibilidad.exists():
            df_sensibilidad = pd.read_csv(ruta_sensibilidad)
            st.markdown("### Resultados de sensibilidad geográfica")
            st.dataframe(df_sensibilidad, use_container_width=True)

        ruta_importancia = DATA_DIR / "tabla_importancia_variables.csv"

        if ruta_importancia.exists():
            df_importancia = pd.read_csv(ruta_importancia)
            st.markdown("### Importancia de variables")
            st.dataframe(df_importancia, use_container_width=True)

    with tab4:
        st.subheader("⚖️ Interpretación metodológica y ética")

        st.markdown(
            """
            <div style="
                background-color:#1E1E1E;
                padding:18px;
                border-radius:12px;
                border-left:5px solid #F9A826;
                color:#F2F2F2;
                margin-bottom:20px;">
                <h3>Interpretación de resultados</h3>
                <p>
                Las matrices de confusión permiten identificar qué categorías son clasificadas
                correctamente y cuáles presentan mayores niveles de error. Esta información es
                importante porque una métrica global, como el accuracy, puede ocultar problemas
                de desempeño en clases minoritarias o menos representadas.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color:#1E1E1E;
                padding:18px;
                border-radius:12px;
                border-left:5px solid #C44536;
                color:#F2F2F2;
                margin-bottom:20px;">
                <h3>Consideraciones éticas</h3>
                <p>
                Los modelos desarrollados en este proyecto no deben utilizarse para tomar decisiones
                judiciales, policiales o administrativas sobre personas. Su finalidad es exclusivamente
                académica y exploratoria, orientada a identificar patrones agregados dentro de los datos
                disponibles.
                </p>
                <p>
                Además, los resultados pueden estar influidos por sesgos de judicialización,
                subrepresentación territorial, desbalance de clases y disponibilidad limitada de
                variables sociodemográficas.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                background-color:#16213E;
                padding:18px;
                border-radius:12px;
                border-left:5px solid #2E86AB;
                color:#F2F2F2;">
                <h3>Criterio de selección responsable</h3>
                <p>
                La selección del mejor modelo no debe basarse únicamente en la métrica de desempeño
                más alta. También deben considerarse la interpretabilidad, la estabilidad, la sensibilidad
                a variables territoriales y el riesgo de reproducir sesgos existentes en los registros.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )



# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## 📊 Navegación")
 
    seccion = st.radio(
        "Selecciona una sección",
        [
            "🏠 Inicio",
            "📁 Datos y metodología",
            "🎯 Evaluación de modelos",
            "📊 Matrices de confusión",
            "📉 Curvas ROC",
            "🧩 Importancia de variables",
            "🧪 Pruebas de sensibilidad",
            "⚖️ Ética y limitaciones",
            "📊 Evaluación comparativa modelos",
            "✅ Conclusiones",
            "⬇️ Descargas"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        """
        **Materia:**  
        Seminario de Innovación en Análisis y Visualización de Datos.

        **Proyecto:**  
        Análisis de perfiles sociodemográficos de personas imputadas por robo en México.

        **Fuente:**  
        INEGI, EHRIIJ, 2018-2021.

        **Variables principales:**  
        sexo, edad, nivel de instrucción y ocupación.
        """
    )

    st.markdown("---")

    st.metric("CSV detectados", contar_existentes(CSV))
    st.metric("Figuras detectadas", contar_existentes(FIGURAS))


# ============================================================
# SECCIÓN: INICIO
# ============================================================

if seccion == "🏠 Inicio":

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-title">
                📊 Análisis sociodemográfico de personas imputadas por robo en México
            </div>
            <div class="hero-subtitle">
                Este prototipo interactivo presenta los principales resultados del análisis exploratorio,
modelado predictivo, evaluación comparativa y discusión ética desarrollados en el marco del
proyecto final de la materia de Seminario de Visualización y Análisis de Datos.

El estudio utiliza información pública proveniente del INEGI, específicamente del esquema
EHRIIJ para los ejercicios 2018 a 2021. El objetivo general es identificar patrones
sociodemográficos asociados con personas imputadas por el delito de robo, considerando
variables como sexo, edad, nivel de instrucción y ocupación.

El prototipo permite navegar entre distintas secciones analíticas, visualizar resultados
generados en Python, consultar métricas de evaluación de modelos y reflexionar sobre las
limitaciones metodológicas, los sesgos potenciales y las implicaciones éticas del uso de
modelos predictivos en contextos relacionados con justicia.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Fuente", "INEGI")
    with col2:
        st.metric("Periodo", "2018-2021")
    with col3:
        st.metric("Modelos", "5")
    with col4:
        st.metric("Enfoque", "Nacional")

    card(
        "Objetivo del prototipo",
        """
        Presentar de manera clara, visual e interactiva los hallazgos principales del análisis,
        permitiendo revisar el desempeño de los modelos, sus errores, la importancia de variables
        y la estabilidad de los resultados ante distintas pruebas de sensibilidad.
        """,
        "🎯"
    )

    note_card(
        """
        <strong>Nota metodológica:</strong> el análisis se realiza con cobertura nacional debido a
        limitaciones de representatividad para una lectura exclusiva de CDMX. Los resultados son
        exploratorios y no deben emplearse para decisiones judiciales, policiales o administrativas
        sobre personas.
        """
    )

    st.markdown("## Vista rápida de resultados")

    col_a, col_b = st.columns(2)

    with col_a:
        mostrar_imagen(
            FIGURAS["roc_png"],
            "Curvas ROC comparativas",
            "Comparación del desempeño discriminativo de los modelos."
        )

    with col_b:
        mostrar_imagen(
            FIGURAS["importancia"],
            "Importancia de variables",
            "Variables con mayor peso en los modelos basados en árboles."
        )


# ============================================================
# SECCIÓN: DATOS Y METODOLOGÍA
# ============================================================

elif seccion == "📁 Datos y metodología":

    st.markdown("## 📁 Datos y metodología")

    card(
        "Fuente de datos",
        """
  La fuente principal de información utilizada en este proyecto corresponde a los registros
del INEGI integrados bajo el esquema EHRIIJ, correspondientes a los ejercicios 2018-2021.

La base de datos fue organizada en una infraestructura relacional en PostgreSQL, compuesta
por trece tablas. A partir de esta estructura se realizaron procesos de extracción,
limpieza, integración y selección de variables relevantes para el análisis.

Las variables consideradas en la etapa final del modelado fueron:

- Sexo.
- Edad.
- Nivel de instrucción.
- Ocupación.

Aunque el planteamiento inicial consideraba un análisis focalizado en la Ciudad de México,
durante el desarrollo del proyecto se identificó una baja representatividad territorial para
esa entidad. Por ello, el modelo fue entrenado con cobertura nacional y sus resultados se
interpretan con cautela en el contexto de la Ciudad de México.

La metodología general incluyó las siguientes etapas:

1. Integración de información desde PostgreSQL.
2. Limpieza y transformación de variables.
3. Análisis exploratorio de datos.
4. Generación de visualizaciones descriptivas.
5. Entrenamiento de modelos de clasificación supervisada.
6. Evaluación comparativa mediante métricas y matrices de confusión.
7. Pruebas de sensibilidad.
8. Discusión metodológica, ética y de limitaciones.
        """,
        "🗂️"
    )

    card(
        "Variables consideradas",
        """
        <ul>
            <li><strong>Sexo:</strong> característica sociodemográfica básica.</li>
            <li><strong>Edad:</strong> variable utilizada para identificar diferencias por grupo etario.</li>
            <li><strong>Nivel de instrucción:</strong> aproximación al contexto educativo.</li>
            <li><strong>Ocupación:</strong> aproximación al contexto laboral de los registros.</li>
        </ul>
        """,
        "📌"
    )

    card(
        "Modelos evaluados",
        """
        Se compararon cinco enfoques de clasificación supervisada:
        <ul>
            <li>Árbol de decisión.</li>
            <li>MLP.</li>
            <li>Naive Bayes.</li>
            <li>Random Forest.</li>
            <li>XGBoost.</li>
        </ul>
        """,
        "🤖"
    )

    note_card(
        """
        Las variables utilizadas no deben interpretarse como causas del delito. El análisis es de
        carácter exploratorio, descriptivo y predictivo, no causal.
        """
    )

    st.markdown("### Archivos disponibles en la carpeta `data`")

    archivos_data = sorted(DATA_DIR.glob("*.csv")) if DATA_DIR.exists() else []

    if archivos_data:
        df_archivos = pd.DataFrame({
            "archivo": [a.name for a in archivos_data],
            "ruta": [str(a.relative_to(BASE_DIR)) for a in archivos_data]
        })
        st.dataframe(df_archivos, use_container_width=True)
    else:
        warning_card("No se encontraron archivos CSV en la carpeta data.")


# ============================================================
# SECCIÓN: EVALUACIÓN DE MODELOS
# ============================================================

elif seccion == "🎯 Evaluación de modelos":

    st.markdown("## 🎯 Evaluación comparativa de modelos")

    card(
        "Propósito de la evaluación",
        """
        En esta sección se presentan los resultados del entrenamiento y evaluación de distintos
modelos de clasificación supervisada. El propósito de esta etapa fue comparar el desempeño
de diferentes algoritmos para identificar patrones en los perfiles sociodemográficos de
personas imputadas por robo.

Los modelos considerados incluyen árboles de decisión, Random Forest, Naive Bayes, redes
neuronales tipo MLP y XGBoost. La comparación se realizó mediante métricas generales de
desempeño, matrices de confusión, curvas ROC y análisis de errores.

Es importante señalar que el objetivo del modelado no es predecir comportamientos
individuales ni generar perfiles de riesgo aplicables a personas específicas. Los modelos
se utilizan exclusivamente como herramientas exploratorias para analizar patrones agregados
en los datos disponibles.

La interpretación de los resultados debe considerar posibles sesgos derivados de la fuente
de información, entre ellos:

- Sesgos de judicialización.
- Subrepresentación de ciertos territorios.
- Desbalance entre clases.
- Limitaciones en la disponibilidad de variables sociodemográficas.
- Posibles diferencias entre registros administrativos y fenómenos delictivos reales.
        """,
        "📊"
    )

    st.markdown("### Resumen de errores por matriz de confusión")

    df_errores = mostrar_tabla(
        CSV["errores"],
        titulo=None,
        descripcion=(
            "Esta tabla resume los errores derivados de las matrices de confusión. "
            "Sirve para comparar el comportamiento de los modelos desde una perspectiva de aciertos y fallos."
        )
    )

    if df_errores is not None:
        with st.expander("🔎 Interpretación sugerida de la tabla de errores"):
            st.write(
                """
                - Un menor número de errores no necesariamente implica que el modelo sea éticamente más adecuado.
                - Es importante revisar si los errores se concentran en alguna clase específica.
                - En datos institucionales, los errores pueden reflejar sesgos de registro, desbalance de clases
                  o falta de variables contextuales.
                """
            )

    st.markdown("### Métricas aproximadas calculadas desde matrices absolutas")

    resumen_metricas = []

    for modelo, rutas in MODELOS.items():
        df = leer_csv(rutas["abs"])
        matriz = preparar_matriz_confusion(df)

        if matriz is not None:
            metricas = calcular_metricas_desde_matriz(matriz)
            if metricas:
                resumen_metricas.append({
                    "Modelo": modelo,
                    "Total registros evaluados": int(metricas["total"]),
                    "Aciertos": int(metricas["aciertos"]),
                    "Errores": int(metricas["errores"]),
                    "Accuracy aproximado": round(metricas["accuracy"], 4)
                })

    if resumen_metricas:
        df_resumen = pd.DataFrame(resumen_metricas)
        st.dataframe(df_resumen, use_container_width=True)

        mejor = df_resumen.sort_values("Accuracy aproximado", ascending=False).iloc[0]

        note_card(
            f"""
             <strong>Modelo con mayor accuracy aproximado:</strong> {mejor['Modelo']}<br>
             <strong>Accuracy aproximado:</strong> {mejor['Accuracy aproximado']:.4f}<br><br>
            Esta selección debe complementarse con criterios de interpretabilidad, sensibilidad y análisis ético.
            """
        )
    else:
        warning_card("No fue posible calcular métricas aproximadas desde las matrices absolutas.")

    card(
        "Criterio de selección responsable",
        """
        La selección del modelo no debe basarse únicamente en accuracy. En este proyecto se recomienda
        considerar también la interpretabilidad, la estabilidad de resultados, el análisis de errores y el
        riesgo de uso indebido en contextos judiciales o policiales.
        """,
        "⚖️"
    )


# ============================================================
# SECCIÓN: MATRICES DE CONFUSIÓN
# ============================================================

elif seccion == "📊 Matrices de confusión":

    st.markdown("## 📊 Matrices de confusión")

    st.write(
        """
        Las matrices de confusión permiten evaluar el desempeño de los modelos comparando las
clases reales con las clases predichas. Esta herramienta facilita la identificación de
aciertos y errores de clasificación para cada categoría analizada.

En el contexto de este proyecto, las matrices de confusión son útiles porque permiten
observar si un modelo concentra sus aciertos en las clases mayoritarias o si mantiene un
desempeño relativamente equilibrado entre distintas categorías.

Se presentan matrices en dos formatos:

- **Matrices absolutas:** muestran el número de casos clasificados en cada combinación
  de clase real y clase predicha.
- **Matrices normalizadas:** muestran proporciones, lo que facilita la comparación entre
  categorías con tamaños diferentes.

La lectura de estas matrices debe hacerse con cautela. Un modelo con buen desempeño global
puede presentar errores relevantes en grupos menos representados. Por ello, la matriz de
confusión complementa las métricas generales y permite una evaluación más detallada del
comportamiento del modelo.
        """
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Figuras comparativas",
            "Matrices por modelo",
            "Tabla de errores"
        ]
    )

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            mostrar_imagen(
                FIGURAS["matrices_absolutas_png"],
                "Matrices absolutas",
                "Matrices de confusión absolutas por modelo."
            )

        with col2:
            mostrar_imagen(
                FIGURAS["matrices_normalizadas_png"],
                "Matrices normalizadas",
                "Matrices de confusión normalizadas por modelo."
            )

        note_card(
            """
            Las matrices absolutas muestran frecuencias, mientras que las matrices normalizadas permiten
            comparar proporciones entre clases y modelos, especialmente cuando existen desbalances.
            """
        )

    with tab2:
        modelo_sel = st.selectbox(
            "Selecciona un modelo",
            list(MODELOS.keys())
        )

        rutas = MODELOS[modelo_sel]

        col1, col2 = st.columns(2)

        with col1:
            matriz_abs = mostrar_heatmap_matriz(
                rutas["abs"],
                f"Matriz absoluta - {modelo_sel}",
                normalizada=False
            )

        with col2:
            matriz_norm = mostrar_heatmap_matriz(
                rutas["norm"],
                f"Matriz normalizada - {modelo_sel}",
                normalizada=True
            )

        if matriz_abs is not None:
            metricas = calcular_metricas_desde_matriz(matriz_abs)

            if metricas:
                st.markdown("### Indicadores calculados desde la matriz absoluta")

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric("Total", int(metricas["total"]))
                with c2:
                    st.metric("Aciertos", int(metricas["aciertos"]))
                with c3:
                    st.metric("Errores", int(metricas["errores"]))
                with c4:
                    st.metric("Accuracy aprox.", round(metricas["accuracy"], 4))

    with tab3:
        mostrar_tabla(
            CSV["errores"],
            "Tabla de errores de matrices de confusión",
            "Resumen tabular de errores por modelo."
        )

        card(
            "Interpretación de errores",
            """
            El análisis de errores es fundamental para evaluar el comportamiento real de los modelos.
            Un modelo puede tener buen desempeño global, pero presentar errores desiguales entre clases.
            En contextos sensibles, estos errores deben documentarse y discutirse desde una perspectiva ética.
            """,
            "🔎"
        )


# ============================================================
# SECCIÓN: CURVAS ROC
# ============================================================

elif seccion == "📉 Curvas ROC":

    st.markdown("## 📉 Curvas ROC")

    card(
        "Función de las curvas ROC",
        """
        Las curvas ROC permiten comparar la capacidad de los modelos para discriminar entre clases.
Estas curvas representan la relación entre la tasa de verdaderos positivos y la tasa de
falsos positivos bajo distintos umbrales de clasificación.

En este proyecto, las curvas ROC se utilizan como una herramienta complementaria para
comparar el desempeño de los modelos supervisados. Una curva más cercana al extremo
superior izquierdo indica una mejor capacidad discriminativa.

Sin embargo, estas curvas no deben interpretarse de forma aislada. En contextos con clases
desbalanceadas o con implicaciones sociales sensibles, es necesario complementar la
interpretación con matrices de confusión, métricas desagregadas, análisis de errores y
consideraciones éticas.

El objetivo no es seleccionar automáticamente el modelo con mayor rendimiento numérico,
sino identificar cuál ofrece un equilibrio razonable entre desempeño, interpretabilidad,
estabilidad y responsabilidad metodológica.
        """,
        "📈"
    )

    mostrar_imagen(
        FIGURAS["roc_png"],
        "Curvas ROC comparativas",
        "Comparación del desempeño discriminativo de los modelos evaluados."
    )

    with st.expander("📄 Archivo SVG disponible"):
        if FIGURAS["roc_svg"].exists():
            st.write(f"Archivo detectado: `{FIGURAS['roc_svg'].relative_to(BASE_DIR)}`")
            boton_descarga(FIGURAS["roc_svg"], "descargar_roc_svg")
        else:
            warning_card("No se encontró el archivo CurvasRoc.svg.")

    note_card(
        """
        <strong>Lectura responsable:</strong> una curva ROC favorable no elimina la necesidad de revisar
        sesgos, errores por clase, sensibilidad geográfica y estabilidad ante cambios en predictores.
        """
    )


# ============================================================
# SECCIÓN: IMPORTANCIA DE VARIABLES
# ============================================================

elif seccion == "🧩 Importancia de variables":

    st.markdown("## 🧩 Importancia de variables")

    card(
        "Objetivo de esta sección",
        """
        La importancia de variables permite identificar cuáles características tienen mayor peso
en las decisiones de ciertos modelos, especialmente aquellos basados en árboles, como
árboles de decisión, Random Forest o XGBoost.

En este análisis se consideran variables sociodemográficas como sexo, edad, nivel de
instrucción y ocupación. La importancia atribuida a estas variables permite explorar cuáles
dimensiones contribuyen en mayor medida a la clasificación realizada por los modelos.

No obstante, la importancia estadística de una variable no debe confundirse con causalidad.
Que una variable sea relevante para el modelo no significa que explique por sí misma la
ocurrencia del fenómeno analizado ni que deba utilizarse para tomar decisiones sobre
personas.

Este punto es especialmente importante en estudios vinculados con justicia, seguridad o
registros administrativos, ya que las variables disponibles pueden reflejar no solo patrones
del fenómeno estudiado, sino también sesgos institucionales, desigualdades estructurales y
diferencias en los procesos de registro.
        """,
        "🧠"
    )

    mostrar_imagen(
        FIGURAS["importancia"],
        "Importancia de variables en modelos de árbol",
        "Variables con mayor contribución relativa dentro de los modelos evaluados."
    )

    df_importancia = mostrar_tabla(
        CSV["importancia_variables"],
        "Tabla de importancia de variables",
        "Valores exportados de importancia de variables."
    )

    if df_importancia is not None:
        columnas = list(df_importancia.columns)

        with st.expander("🔎 Revisión rápida de columnas"):
            st.write(columnas)

    danger_card(
        """
        La importancia de una variable en el modelo no significa que dicha variable cause el fenómeno analizado.
        En particular, sexo, edad, ocupación o nivel de instrucción no deben usarse para justificar perfilamiento,
        vigilancia ni toma de decisiones sobre individuos.
        """
    )


# ============================================================
# SECCIÓN: PRUEBAS DE SENSIBILIDAD
# ============================================================

elif seccion == "🧪 Pruebas de sensibilidad":

    st.markdown("## 🧪 Pruebas de sensibilidad")

    st.write(
        """
        Las pruebas de sensibilidad permiten analizar qué tan estables son los resultados del modelo
ante cambios en las variables utilizadas o en las condiciones del análisis. En este proyecto,
estas pruebas son relevantes porque ayudan a identificar si el desempeño depende en exceso
de ciertas variables o de determinados componentes territoriales.

Se realizaron ejercicios de sensibilidad asociados con:

- Inclusión o exclusión de variables territoriales.
- Ablación de subconjuntos de predictoras.
- Comparación del desempeño bajo diferentes configuraciones de variables.
- Revisión de la estabilidad de los modelos ante cambios en la información disponible.

Estos ejercicios permiten fortalecer la evaluación metodológica, ya que un modelo puede
tener buen desempeño en una configuración específica, pero perder estabilidad cuando se
modifican las variables de entrada.

Desde una perspectiva responsable, la sensibilidad del modelo es especialmente importante
porque permite detectar dependencias problemáticas, posibles sesgos territoriales o
sobreajustes relacionados con características particulares de los datos.
        """
    )

    tab1, tab2 = st.tabs(
        [
            "Ablación de predictoras",
            "Sensibilidad territorial"
        ]
    )

    with tab1:
        card(
            "Ablación por subconjuntos de predictoras",
            """
            La ablación permite observar cómo cambia el desempeño del modelo cuando se modifican o eliminan
            subconjuntos de variables. Esto ayuda a identificar si el modelo depende excesivamente de ciertas
            variables.
            """,
            "🧪"
        )

        mostrar_imagen(
            FIGURAS["ablacion"],
            "Ablación por subconjuntos de predictoras",
            "Resultados de la prueba de ablación de variables predictoras."
        )

        mostrar_tabla(
            CSV["ablacion"],
            "Resultados tabulares de ablación",
            "Tabla exportada con resultados por subconjunto de predictores."
        )

    with tab2:
        card(
            "Sensibilidad a variables territoriales",
            """
            La prueba de sensibilidad territorial evalúa el efecto de incorporar o modificar variables
            geográficas. Es relevante porque los registros institucionales pueden tener diferencias de
            cobertura entre entidades o regiones.
            """,
            "🌎"
        )

        mostrar_imagen(
            FIGURAS["sensibilidad_territorial"],
            "Prueba de sensibilidad a variables territoriales",
            "Evaluación del impacto de variables geográficas o territoriales."
        )

        mostrar_tabla(
            CSV["sensibilidad_geografica"],
            "Resultados de sensibilidad geográfica",
            "Tabla exportada con resultados de sensibilidad territorial."
        )

    note_card(
        """
        <strong>Interpretación:</strong> si el desempeño cambia mucho al modificar predictores o variables
        territoriales, el modelo puede ser sensible a la configuración del conjunto de datos. Esto debe reportarse
        como una limitación metodológica.
        """
    )


# ============================================================
# SECCIÓN: ÉTICA Y LIMITACIONES
# ============================================================

elif seccion == "⚖️ Ética y limitaciones":

    st.markdown("## ⚖️ Ética, sesgos y limitaciones")

    card(
        "Sesgo de judicialización",
        """
        El análisis de datos relacionados con personas imputadas por delitos requiere una reflexión
ética rigurosa. Aunque la información utilizada proviene de fuentes públicas y se trabaja
a nivel agregado, los resultados pueden tener implicaciones sensibles si se interpretan de
manera inadecuada.

Este proyecto no busca construir perfiles individuales de riesgo ni proponer herramientas
para la toma de decisiones judiciales, policiales o administrativas. Su finalidad es
académica, exploratoria y metodológica.

Entre las principales limitaciones del estudio se identifican:

- Los registros analizados corresponden a personas imputadas, no necesariamente a personas
  condenadas.
- La información puede reflejar sesgos de judicialización y prácticas institucionales.
- No todos los territorios tienen la misma representación en los datos.
- Las variables disponibles son limitadas y no capturan toda la complejidad social del
  fenómeno.
- El desempeño de los modelos puede verse afectado por clases desbalanceadas.
- Los resultados no deben generalizarse sin considerar el contexto de producción de los
  datos.

Por estas razones, los modelos deben entenderse como instrumentos de análisis exploratorio
y no como mecanismos de predicción individual o de clasificación normativa de personas.
        """,
        "⚠️"
    )

    card(
        "Representatividad territorial",
        """
        Aunque el interés interpretativo puede ubicarse en contextos específicos como CDMX, la baja
        representatividad local obliga a mantener un entrenamiento de cobertura nacional y a interpretar
        los resultados con cautela.
        """,
        "🗺️"
    )

    card(
        "Limitaciones de variables",
        """
        El modelo solo utiliza variables disponibles en la fuente original. La ausencia de variables
        contextuales, socioeconómicas, institucionales o territoriales más detalladas limita el alcance
        explicativo del análisis.
        """,
        "📌"
    )

    card(
        "No causalidad",
        """
        Las asociaciones observadas por los modelos son estadísticas y predictivas, no causales. No debe
        afirmarse que características como edad, sexo, ocupación o escolaridad causen participación en delitos.
        """,
        "🚫"
    )

    danger_card(
        """
        Este prototipo no debe utilizarse para tomar decisiones automáticas sobre individuos, orientar acciones
        policiales, justificar perfilamiento sociodemográfico ni apoyar decisiones judiciales.
        """
    )

    note_card(
        """
        <strong>Uso adecuado:</strong> el valor del proyecto es académico, exploratorio y de visualización.
        Su aportación principal es organizar, analizar y comunicar resultados con una perspectiva crítica
        sobre sesgos, límites y riesgos de interpretación.
        """
    )

# ============================================================
# SECCIÓN: Evaluación comparativa modelos
# ============================================================

elif seccion == "📊 Evaluación comparativa modelos":
   st.markdown("""
# Evaluación comparativa de modelos

La evaluación comparativa permite analizar el desempeño relativo de los distintos modelos
supervisados implementados en el proyecto. Esta comparación considera tanto métricas
globales como elementos visuales y análisis de errores.

Los modelos evaluados fueron comparados mediante:

- Accuracy aproximado.
- Matrices de confusión absolutas.
- Matrices de confusión normalizadas.
- Curvas ROC.
- Tabla de errores.
- Resultados de sensibilidad.
- Resultados de ablación de variables.
- Importancia de variables.

Aunque las métricas cuantitativas permiten identificar diferencias de desempeño, la
selección de un modelo no debe basarse exclusivamente en el valor más alto de accuracy.
También deben considerarse la interpretabilidad, la estabilidad, la sensibilidad a variables
territoriales y el riesgo de reproducir sesgos presentes en los datos.

En este sentido, la evaluación comparativa tiene una doble finalidad: identificar el modelo
con mejor comportamiento técnico y, al mismo tiempo, discutir los límites éticos y
metodológicos de su uso.
""")
   render_punto_3_evaluacion_modelos()


# ============================================================
# SECCIÓN: CONCLUSIONES
# ============================================================

elif seccion == "✅ Conclusiones":

    st.markdown("## ✅ Conclusiones")

    card(
        "Conclusión general",
        """
       El proyecto permitió desarrollar un flujo integral de análisis de datos, desde la integración
de información en PostgreSQL hasta la construcción de visualizaciones, modelos supervisados,
pruebas de sensibilidad y un prototipo interactivo en Streamlit.

Los resultados muestran que es posible identificar patrones sociodemográficos agregados en
los registros de personas imputadas por robo. Sin embargo, dichos patrones deben
interpretarse con cautela debido a las características de la fuente de información y a los
posibles sesgos presentes en los registros administrativos.

La evaluación comparativa de modelos permitió observar diferencias de desempeño entre los
algoritmos utilizados. No obstante, el análisis también evidenció que una métrica global
no es suficiente para determinar la calidad o pertinencia de un modelo. Es necesario
considerar errores por clase, sensibilidad a variables, interpretabilidad y riesgos éticos.

Como producto final, el prototipo en Streamlit facilita la exploración interactiva de los
resultados y complementa el dashboard desarrollado en Power BI. Ambos productos permiten
presentar de manera visual, ordenada y accesible los principales hallazgos del proyecto.

Finalmente, se concluye que el uso de técnicas de ciencia de datos en contextos vinculados
con justicia debe realizarse bajo criterios de responsabilidad, transparencia y cautela,
evitando interpretaciones deterministas o usos que puedan afectar derechos individuales.
        """,
        "📌"
    )

    card(
        "Hallazgos técnicos",
        """
        La comparación de modelos mediante matrices de confusión, curvas ROC, análisis de errores e importancia
        de variables permitió evaluar el desempeño predictivo desde diferentes perspectivas. Las pruebas de
        sensibilidad fortalecen la revisión de estabilidad y robustez.
        """,
        "📊"
    )

    card(
        "Hallazgos metodológicos",
        """
        El análisis confirma la necesidad de interpretar los resultados con cautela, especialmente por tratarse
        de datos institucionales sobre personas imputadas. La cobertura nacional mejora la disponibilidad de datos,
        pero limita interpretaciones estrictamente locales.
        """,
        "🧭"
    )

    card(
        "Recomendaciones",
        """
        <ul>
            <li>Reportar siempre matrices absolutas y normalizadas.</li>
            <li>Incluir análisis de errores y sensibilidad en la discusión.</li>
            <li>Priorizar modelos interpretables cuando el contexto sea sensible.</li>
            <li>No interpretar resultados como causalidad.</li>
            <li>No utilizar el modelo para decisiones sobre personas.</li>
        </ul>
        """,
        "✅"
    )


# ============================================================
# SECCIÓN: DESCARGAS
# ============================================================

elif seccion == "⬇️ Descargas":

    st.markdown("## ⬇️ Descargas")

    st.write(
        """
        Esta sección concentra los principales archivos generados durante el desarrollo del
proyecto. Su objetivo es facilitar la consulta, reproducción y revisión de los resultados.

Los materiales disponibles pueden incluir:

- Bases de resultados en formato CSV.
- Figuras generadas en Python.
- Matrices de confusión.
- Resultados de pruebas de sensibilidad.
- Tablas de importancia de variables.
- Reportes o documentos complementarios.
- Archivos relacionados con el dashboard y el prototipo.


La disponibilidad de estos archivos fortalece la transparencia del análisis y permite
documentar de forma más clara las decisiones metodológicas tomadas durante el proyecto.
        """
    )

    tab1, tab2 = st.tabs(["📊 Figuras", "📁 CSV"])

    with tab1:
        st.markdown("### Figuras disponibles")

        figuras_existentes = [ruta for ruta in FIGURAS.values() if ruta.exists()]

        if figuras_existentes:
            for i, ruta in enumerate(figuras_existentes):
                st.write(f"`{ruta.relative_to(BASE_DIR)}`")
                boton_descarga(ruta, f"figura_{i}_{ruta.name}")
        else:
            warning_card("No se detectaron figuras disponibles.")

    with tab2:
        st.markdown("### Archivos CSV disponibles")

        csv_existentes = [ruta for ruta in CSV.values() if ruta.exists()]

        if csv_existentes:
            for i, ruta in enumerate(csv_existentes):
                st.write(f"`{ruta.relative_to(BASE_DIR)}`")
                boton_descarga(ruta, f"csv_{i}_{ruta.name}")
        else:
            warning_card("No se detectaron archivos CSV disponibles.")


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="small-muted">
        Proyecto académico desarrollado para la Maestría en Big Data. 
        Fuente principal: INEGI, EHRIIJ, ejercicios 2018-2021. 
        Los resultados tienen fines exploratorios y no deben utilizarse para decisiones automáticas
        sobre individuos ni para fines policiales, judiciales o administrativos.
    </div>
    """,
    unsafe_allow_html=True
)