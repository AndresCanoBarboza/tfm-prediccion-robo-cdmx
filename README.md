# tfm-prediccion-robo-cdmx
# Sistema Predictivo de Conducta Delictiva (Robo) — CDMX

Trabajo Final de Maestría · UNIR · Máster en Análisis y Visualización de Datos Masivos
Equipo 1C: Alcantar Huesca L., Cano Barboza A., Vázquez Rueda J.

## Descripción
Sistema de minería de datos y aprendizaje automático que caracteriza el perfil
sociodemográfico de personas imputadas por robo, contrastándolo con la población
general, a partir de dos fuentes públicas del INEGI (EHRIIJ y ENVIPE, 2018–2021).

## Estructura del repositorio
- `data/` — conexión a la base de datos y generación del diagrama del modelo de datos
- `notebooks/` — análisis exploratorio (EDA) y modelado
- `models/` — artefactos generados (diagrama, modelos entrenados)
- `app/` — prototipo interactivo en Streamlit

## Requisitos
Ver `requirements.txt`. Se necesita una variable de entorno `DATABASE_URL`
apuntando a la base PostgreSQL (ver `.env.example`).

## Cómo ejecutar
1. Instalar dependencias: `pip install -r requirements.txt`
2. Copiar `.env.example` a `.env` y completar con las credenciales reales
3. Probar la conexión: `python data/db_connection.py`
4. Lanzar el prototipo: `streamlit run app/streamlit_app.py`

## Fuentes de datos
- INEGI — EHRIIJ (Esquema Homologado de Recolección de Información de Impartición de Justicia)
- INEGI — ENVIPE (Encuesta Nacional de Victimización y Percepción sobre Seguridad Pública)