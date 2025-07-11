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

if __name__ == "__main__":
    try:
        conn = conectar_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Apuesta ORDER BY fecha_apuesta DESC LIMIT 5")
            datos = cursor.fetchall()
            print("=== ÚLTIMAS 5 APUESTAS ===")
            if datos:
                for dato in datos:
                    print(dato)
            else:
                print("No hay apuestas en la tabla")
            
            cursor.execute("SELECT COUNT(*) as total FROM Apuesta")
            total = cursor.fetchone()
            print(f"\n=== TOTAL APUESTAS: {total['total']} ===")
            
            # Agregar al final del archivo de prueba:

            # Verificar qué trae la consulta del historial
            cursor.execute("""
                SELECT a.*, c.disposicion, c.color, c.valor
                FROM Apuesta a
                JOIN Carton c ON a.carton_id = c.id
                WHERE a.cliente_dni = %s
                ORDER BY a.fecha_apuesta DESC
            """, (45620374,))  # ← CAMBIAR por tu DNI

            datos_historial = cursor.fetchall()
            print(f"\n=== HISTORIAL PARA DNI 46437775 ===")
            if datos_historial:
                for dato in datos_historial:
                    print(f"ID: {dato['id']}, Estado: {dato['estado']}, Fecha: {dato['fecha_apuesta']}")
            else:
                print("No hay datos de historial para este DNI")

                # Verificar datos del usuario 46437775
            cursor.execute("SELECT dni, nombre, apellido FROM Cliente WHERE dni = %s", (45620374,))
            usuario = cursor.fetchone()
            if usuario:
                print(f"\n=== USUARIO 45620374 ===")
                print(f"Nombre: {usuario['nombre']} {usuario['apellido']}")
                print(f"DNI: {usuario['dni']}")
            else:
                print("Usuario no encontrado")

                    # En tu archivo de prueba, agregar:
            # En tu archivo de prueba:
            cursor.execute("SELECT * FROM Apuesta WHERE id >= 19")
            apuestas_recientes = cursor.fetchall()
            print(f"\n=== APUESTAS ID 19+ ===")
            for apuesta in apuestas_recientes:
                print(f"ID: {apuesta['id']}, Estado: {apuesta['estado']}, Fecha: {apuesta['fecha_apuesta']}")

            # También verificar todas las apuestas de tu DNI:
            cursor.execute("SELECT * FROM Apuesta WHERE cliente_dni = 45620374 ORDER BY id DESC")
            todas_mis_apuestas = cursor.fetchall()
            print(f"\n=== TODAS MIS APUESTAS ===")
            for apuesta in todas_mis_apuestas:
                print(f"ID: {apuesta['id']}, Estado: {apuesta['estado']}, Fecha: {apuesta['fecha_apuesta']}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")


        # Agregar al final del archivo de prueba:

# Importar la clase que usa el historial
import sys
sys.path.append('.')  # Agregar directorio actual
from backend import Apuesta

print("\n=== TESTING FUNCIÓN PYTHON ===")

# Testear la función exacta que usa historial_frame.py
apuesta_db = Apuesta()
try:
    partidas = apuesta_db.obtener_apuestas_cliente(46437775, limite=50)
    print(f"Función obtener_apuestas_cliente() devuelve: {len(partidas)} registros")
    
    if partidas:
        print("Primeras 3 partidas:")
        for i, partida in enumerate(partidas[:3]):
            print(f"{i+1}. ID: {partida.get('id')}, Estado: {partida.get('estado')}, Fecha: {partida.get('fecha_apuesta')}")
    else:
        print("❌ La función Python no devuelve datos")
        
except Exception as e:
    print(f"❌ ERROR en función Python: {e}")
finally:
    apuesta_db.cerrar()

    # Testear con TU DNI correcto
print(f"\n=== TESTING CON TU DNI: 45620374 ===")

apuesta_db = Apuesta()
try:
    # Usar TU DNI en lugar del otro
    partidas_tuyas = apuesta_db.obtener_apuestas_cliente(45620374, limite=50)
    print(f"Función con TU DNI devuelve: {len(partidas_tuyas)} registros")
    
    if partidas_tuyas:
        print("Tus partidas:")
        for i, partida in enumerate(partidas_tuyas):
            print(f"{i+1}. ID: {partida.get('id')}, Estado: {partida.get('estado')}, Fecha: {partida.get('fecha_apuesta')}")
    else:
        print("❌ No devuelve TUS datos")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
finally:
    apuesta_db.cerrar()

