"""
Genera el diagrama del modelo de datos del proyecto (linaje de tablas en Neon).
Salida: models/diagrama_modelo_datos.png
Uso: python data/diagrama_modelo_datos.py
"""
from graphviz import Digraph

dot = Digraph(comment="Modelo de datos - TFM Predicción Robo CDMX", format="png")
dot.attr(rankdir="TB", fontname="Helvetica", bgcolor="white")
dot.attr("node", fontname="Helvetica", fontsize="10")

# --- Colores por capa ---
c_fuente = "#E3F2FD"
c_integrado = "#FFF3E0"
c_balanceado = "#F1F8E9"
c_particion = "#E8F5E9"
c_diagnostico = "#FCE4EC"
c_gobierno = "#F3E5F5"

# CAPA 1 — Fuentes
dot.node("envipe", "envipe_demograficos\n(318,419)\nENVIPE — clase negativa",
         shape="cylinder", style="filled", fillcolor=c_fuente)
dot.node("ehriij", "EHRIIJ (INEGI)\nvía proceso externo\nclase positiva",
         shape="cylinder", style="filled", fillcolor=c_fuente)
dot.node("fgj", "fgj_carpetas\n(0 — sin cargar)\n[geoespacial, no usada]",
         shape="cylinder", style="filled,dashed", fillcolor="#ECEFF1")

# CAPA 2 — Integrado
dot.node("integrado", "dataset_integrado\n(884,471)\n15 columnas · alcance nacional",
         shape="box", style="filled,rounded", fillcolor=c_integrado)

# CAPA 3 — Balanceado
dot.node("balanceado", "dataset_modelo_balanceado\n(163,203)\nbalanceo 35/65 · semilla=42",
         shape="box", style="filled,rounded", fillcolor=c_balanceado)

# CAPA 3b — Particiones
dot.node("train", "x_entrenamiento\n(130,562)\n4 predictoras + clase",
         shape="box", style="filled,rounded", fillcolor=c_particion)
dot.node("test", "x_prueba\n(32,641)\n4 predictoras + clase",
         shape="box", style="filled,rounded", fillcolor=c_particion)
dot.node("geo", "x_variante_con_geografia\n(163,203)\n4 pred + 31 dummies entidad\nAUC 0.9204 (diagnóstico)",
         shape="box", style="filled,rounded", fillcolor=c_diagnostico)

# CAPA 4 — Gobierno / resultados
dot.node("gob", "GOBIERNO Y RESULTADOS\n"
                "sensibilidad_ablacion (5)\n"
                "sensibilidad_geografia (4)\n"
                "contexto_robo_alcaldia (64)\n"
                "meta_bitacora_validacion (12)\n"
                "meta_completitud_por_fuente (16)\n"
                "meta_sesgo_territorial (32)",
         shape="note", style="filled", fillcolor=c_gobierno)

# --- Relaciones (flechas) ---
dot.edge("envipe", "integrado", label="integración")
dot.edge("ehriij", "integrado")
dot.edge("integrado", "balanceado", label="balanceo")
dot.edge("balanceado", "train", label="split 80%")
dot.edge("balanceado", "test", label="split 20%")
dot.edge("balanceado", "geo", label="variante\nterritorial", style="dashed")

# Render
dot.render("models/diagrama_modelo_datos", cleanup=True)
print("✅ Diagrama generado en: models/diagrama_modelo_datos.png")