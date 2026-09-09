import os
from sqlalchemy import create_engine, inspect
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def get_engine():
    """
    Crea la conexión a la base de datos Neon (PostgreSQL).
    Requiere la variable de entorno DATABASE_URL definida en un archivo .env
    """
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "No se encontró DATABASE_URL. Asegurate de tener un archivo .env "
            "con la variable definida, o exportarla en tu terminal."
        )
    return create_engine(database_url)

def listar_esquema(engine):
    """Devuelve un diccionario {tabla: [columnas]} de todo el esquema public."""
    inspector = inspect(engine)
    esquema = {}
    for tabla in inspector.get_table_names():
        esquema[tabla] = [col["name"] for col in inspector.get_columns(tabla)]
    return esquema

def preview_tablas(engine, n=5):
    """Muestra las primeras n filas de cada tabla del esquema."""
    inspector = inspect(engine)
    for tabla in inspector.get_table_names():
        print(f"\n{'='*50}\nTabla: {tabla}\n{'='*50}")
        df = pd.read_sql(f'SELECT * FROM "{tabla}" LIMIT {n}', engine)
        print(df)

if __name__ == "__main__":
    engine = get_engine()
    esquema = listar_esquema(engine)
    for tabla, columnas in esquema.items():
        print(f"{tabla} → {columnas}")