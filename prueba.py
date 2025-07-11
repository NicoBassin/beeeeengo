import pymysql
from pymysql.cursors import DictCursor

def conectar_db():
    return pymysql.connect(
        host="mysql-bingo-estructuras-estructuras-bingo.g.aivencloud.com",
        port=19042,
        user="avnadmin",
        password="AVNS_PDkPtgvet2IRp0klIVa",
        db="defaultdb",
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True
    )

def crear_tablas(cursor):
    # Borrar si existen (en orden por dependencias)
    cursor.execute("DROP TABLE IF EXISTS Premio")
    cursor.execute("DROP TABLE IF EXISTS Apuesta")
    cursor.execute("DROP TABLE IF EXISTS Partida")
    cursor.execute("DROP TABLE IF EXISTS Carton")
    cursor.execute("DROP TABLE IF EXISTS Cliente")

def look(cursor):
    # Ejecutar consultas y mostrar resultados para cada tabla
    tablas = ["Premio", "Apuesta", "Partida", "Carton", "Cliente"]
    
    for tabla in tablas:
        print(f"\n--- {tabla} ---")  # Encabezado para cada tabla
        
        # Ejecutar consulta
        cursor.execute(f"SELECT * FROM {tabla}")
        
        # Recuperar TODOS los registros
        resultados = cursor.fetchall()
        
        # Obtener nombres de columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Imprimir nombres de columnas
        print(" | ".join(columnas))
        
        # Imprimir cada fila
        for fila in resultados:
            print(" | ".join(str(valor) for valor in fila))
    
if __name__ == "__main__":
    try:
        print("🔄 Conectando a la base de datos...")
        conn = conectar_db()
        
        with conn.cursor() as cursor:
            print("🔄 Creando tablas...")
            look(cursor)
            print("✅ Tablas creadas correctamente")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        input("\nPresiona ENTER para salir...")
        if 'conn' in locals():
            conn.close()
