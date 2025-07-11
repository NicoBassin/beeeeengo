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

    # Cliente con DNI como clave primaria
    cursor.execute("""
        CREATE TABLE Cliente (
            dni INT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            mail VARCHAR(100) UNIQUE,
            telefono VARCHAR(20),
            saldo INT NOT NULL DEFAULT 10000,
            fecha_nac DATE,
            fecha_reg TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            password VARCHAR(100) NOT NULL
        )
    """)

    # Carton (hoja completa de 6 cartones representada como JSON)
    cursor.execute("""
        CREATE TABLE Carton (
            id INT AUTO_INCREMENT PRIMARY KEY,
            disposicion TEXT NOT NULL,
            valor DECIMAL(10,2) NOT NULL DEFAULT 1000.00,
            color VARCHAR(30),
            activo BOOLEAN DEFAULT FALSE,
            cliente_dni INT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cliente_dni) REFERENCES Cliente(dni) ON DELETE SET NULL
        )
    """)

    # Partida (simplificada para el simulador)
    cursor.execute("""
        CREATE TABLE Partida (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hora_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
            hora_fin DATETIME NULL,
            numeros_cantados TEXT,
            jugadores INT DEFAULT 1,
            cliente_dni INT,
            carton_id INT,
            resultado ENUM('ganada', 'perdida', 'abandonada') NULL,
            ganancia DECIMAL(10,2) DEFAULT 0,
            estado ENUM('en_curso', 'finalizada') DEFAULT 'en_curso',
            FOREIGN KEY (cliente_dni) REFERENCES Cliente(dni) ON DELETE SET NULL,
            FOREIGN KEY (carton_id) REFERENCES Carton(id) ON DELETE SET NULL
        )
    """)

    # Apuesta (relaciona cliente, cartón y resultado)
    cursor.execute("""
        CREATE TABLE Apuesta (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_dni INT,
            carton_id INT,
            fecha_apuesta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            estado ENUM('ganada', 'perdida', 'en juego') DEFAULT 'en juego',
            ganancia DECIMAL(10,2) DEFAULT 0,
            FOREIGN KEY (cliente_dni) REFERENCES Cliente(dni) ON DELETE CASCADE,
            FOREIGN KEY (carton_id) REFERENCES Carton(id) ON DELETE CASCADE
        )
    """)

    # Premio (premios especiales y logros)
    cursor.execute("""
        CREATE TABLE Premio (
            id INT AUTO_INCREMENT PRIMARY KEY,
            partida_id INT,
            descripcion VARCHAR(200),
            valor DECIMAL(10,2),
            ganador_dni INT,
            fecha_premio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo ENUM('bingo', 'linea', 'especial') DEFAULT 'bingo',
            FOREIGN KEY (partida_id) REFERENCES Partida(id) ON DELETE SET NULL,
            FOREIGN KEY (ganador_dni) REFERENCES Cliente(dni) ON DELETE SET NULL
        )
    """)

    # Índices para mejorar rendimiento
    cursor.execute("CREATE INDEX idx_cliente_dni ON Apuesta(cliente_dni)")
    cursor.execute("CREATE INDEX idx_carton_cliente ON Carton(cliente_dni)")
    cursor.execute("CREATE INDEX idx_partida_cliente ON Partida(cliente_dni)")
    cursor.execute("CREATE INDEX idx_premio_ganador ON Premio(ganador_dni)")
    cursor.execute("CREATE INDEX idx_fecha_apuesta ON Apuesta(fecha_apuesta)")

def insertar_datos_ejemplo(cursor):
    """Insertar algunos datos de ejemplo para testing"""
    try:
        # Cliente de ejemplo
        cursor.execute("""
            INSERT INTO Cliente (dni, nombre, apellido, mail, telefono, fecha_nac, password, saldo)
            VALUES (12345678, 'Juan', 'Pérez', 'juan@ejemplo.com', '1134567890', '1990-01-01', 
                    SHA2('123456', 256), 15000)
        """)
        
        # Cartón de ejemplo
        disposicion_ejemplo = '''[
            [1, null, 23, null, null, 56, null, null, 89],
            [null, 12, null, 34, null, null, 67, null, null],
            [null, null, null, null, 45, null, null, 78, null],
            [2, null, 24, null, null, 57, null, null, 80],
            [null, 13, null, 35, null, null, 68, null, null],
            [null, null, null, null, 46, null, null, 79, null]
        ]'''
        
        cursor.execute("""
            INSERT INTO Carton (disposicion, valor, color, activo, cliente_dni)
            VALUES (%s, 1000.00, 'azul', FALSE, 12345678)
        """, (disposicion_ejemplo,))
        
        print("✅ Datos de ejemplo insertados correctamente")
        
    except Exception as e:
        print(f"⚠️ Error al insertar datos de ejemplo: {e}")

def verificar_tablas(cursor):
    """Verificar que las tablas se crearon correctamente"""
    tablas = ['Cliente', 'Carton', 'Partida', 'Apuesta', 'Premio']
    
    print("\n📋 Verificando tablas creadas:")
    for tabla in tablas:
        cursor.execute(f"SHOW TABLES LIKE '{tabla}'")
        if cursor.fetchone():
            cursor.execute(f"SELECT COUNT(*) as count FROM {tabla}")
            count = cursor.fetchone()['count']
            print(f"✅ {tabla}: {count} registros")
        else:
            print(f"❌ {tabla}: No encontrada")

if __name__ == "__main__":
    try:
        print("🔄 Conectando a la base de datos...")
        conn = conectar_db()
        
        with conn.cursor() as cursor:
            print("🔄 Creando tablas...")
            crear_tablas(cursor)
            print("✅ Tablas creadas correctamente")
            
            # Preguntar si insertar datos de ejemplo
            respuesta = input("\n¿Deseas insertar datos de ejemplo? (s/n): ").lower()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                print("🔄 Insertando datos de ejemplo...")
                insertar_datos_ejemplo(cursor)
            
            # Verificar tablas
            verificar_tablas(cursor)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        print(f"\n📊 Estructura de base de datos:")
        print("=" * 50)
        print("📋 Cliente: Información de usuarios registrados")
        print("🎫 Carton: Cartones de bingo generados (formato argentino)")
        print("🎮 Partida: Partidas individuales de bingo")
        print("💰 Apuesta: Relación cliente-cartón-resultado")
        print("🏆 Premio: Premios y logros especiales")
        print("=" * 50)
        
        input("\nPresiona ENTER para salir...")
        if 'conn' in locals():
            conn.close()
