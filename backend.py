import pymysql
from pymysql.cursors import DictCursor
import re
from datetime import datetime, date
import hashlib
import json
import random

# -------------------------------
# CONEXIÓN BASE
# -------------------------------

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

# -------------------------------
# CLASE BASE: Tabla
# -------------------------------

class Tabla:
    def __init__(self):
        self.conn = conectar_db()
        self.cursor = self.conn.cursor()

    def crear(self, sql):
        self.cursor.execute(sql)

    def borrar(self, tabla):
        self.cursor.execute(f"DROP TABLE IF EXISTS {tabla}")

    def consultar(self, tabla):
        self.cursor.execute(f"SELECT * FROM {tabla}")
        return self.cursor.fetchall()

    def modificar(self, sql, datos):
        self.cursor.execute(sql, datos)

    def cerrar(self):
        self.conn.close()

# -------------------------------
# FUNCIONES DE GENERACIÓN DE CARTONES (BINGO ARGENTINO)
# -------------------------------

def fila_valida(numeros):
    """Verificar que una fila tenga números de diferentes decenas"""
    if len(numeros) != 5:
        return False
    decenas = [num // 10 if num != 90 else 8 for num in numeros]
    return len(set(decenas)) == 5

def generar_fila(disponibles):
    """Generar una fila válida de 5 números"""
    intentos = 0
    while True:
        if len(disponibles) < 5:
            return None 
        seleccion = random.sample(disponibles, 5)
        if fila_valida(seleccion):
            return sorted(seleccion)
        intentos += 1
        if intentos > 1000:
            return None

def generar_hoja():
    """Generar una hoja completa de 18 filas (6 cartones)"""
    disponibles = list(range(1, 91))
    hoja = []
    for _ in range(18):
        fila = generar_fila(disponibles)
        if not fila:
            return None
        for num in fila:
            disponibles.remove(num)
        hoja.append(fila)
    return hoja

def generar_cartones():
    """Generar cartones de bingo argentino"""
    hoja_final = None
    intentos_totales = 0
    while hoja_final is None:
        hoja_final = generar_hoja()
        intentos_totales += 1
        if intentos_totales > 50:
            raise Exception("No se pudo generar una hoja válida tras múltiples intentos.")
    
    # Estructurar en formato de 9 columnas
    hoja_estructurada = []
    for fila in hoja_final:
        fila_completa = [None] * 9
        for num in fila:
            col = num // 10 if num != 90 else 8
            fila_completa[col] = num
        hoja_estructurada.append(fila_completa)
    
    return hoja_estructurada

def imprimir_carton(hoja):
    """Imprimir cartón en consola para debug"""
    for i, fila in enumerate(hoja):
        print(['{:>2}'.format(n if n else ' ') for n in fila])
        if (i + 1) % 3 == 0:
            print("-" * 30)
    return None

# -------------------------------
# CLASE CLIENTE
# -------------------------------

class Cliente(Tabla):
    def insertar_cliente(self, dni, nombre, apellido, mail, telefono, fecha_nac, password):
        if not self.validar_mail(mail):
            raise ValueError("❌ Mail inválido")
        if not self.chequear_unicidad(dni, mail):
            raise ValueError("❌ DNI o Mail ya existen")
        if not self.mayor_edad(fecha_nac):
            raise ValueError("❌ Menor de edad")

        password_hash = self.hashear_pass(password)

        sql = """
            INSERT INTO Cliente (dni, nombre, apellido, mail, telefono, fecha_nac, password, saldo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (dni, nombre, apellido, mail, telefono, fecha_nac, password_hash, 10000))
        
    def obtener_cliente_por_dni(self, dni):
        self.cursor.execute("SELECT * FROM Cliente WHERE dni = %s", (dni,))
        return self.cursor.fetchone()

    def actualizar_saldo(self, dni, nuevo_saldo):
        """Actualizar el saldo del cliente"""
        sql = "UPDATE Cliente SET saldo = %s WHERE dni = %s"
        self.cursor.execute(sql, (nuevo_saldo, dni))

    def obtener_saldo(self, dni):
        """Obtener el saldo actual del cliente"""
        self.cursor.execute("SELECT saldo FROM Cliente WHERE dni = %s", (dni,))
        resultado = self.cursor.fetchone()
        
        # Asegurarse de que nunca retorne None
        if resultado and resultado['saldo'] is not None:
            return resultado['saldo']
        else:
            return 0  # Saldo por defecto si no existe o es None

    def debitar_saldo(self, dni, monto):
        """Debitar monto del saldo del cliente"""
        saldo_actual = self.obtener_saldo(dni)
        if saldo_actual < monto:
            raise ValueError("Saldo insuficiente")
        nuevo_saldo = saldo_actual - monto
        self.actualizar_saldo(dni, nuevo_saldo)
        return nuevo_saldo

    def acreditar_saldo(self, dni, monto):
        """Acreditar monto al saldo del cliente"""
        saldo_actual = self.obtener_saldo(dni)
        nuevo_saldo = saldo_actual + monto
        self.actualizar_saldo(dni, nuevo_saldo)
        return nuevo_saldo

    def validar_mail(self, mail):
        return re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", mail)

    def chequear_unicidad(self, dni, mail):
        self.cursor.execute("SELECT dni, mail FROM Cliente WHERE dni = %s OR mail = %s", (dni, mail))
        return len(self.cursor.fetchall()) == 0

    def mayor_edad(self, fecha_nac):
        nacimiento = datetime.strptime(str(fecha_nac), "%Y-%m-%d").date()
        hoy = date.today()
        edad = hoy.year - nacimiento.year - ((hoy.month, hoy.day) < (nacimiento.month, nacimiento.day))
        return edad >= 18

    def hashear_pass(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validar_login(self, dni, password):
        """Validar credenciales de login"""
        password_hash = self.hashear_pass(password)
        sql = "SELECT * FROM Cliente WHERE dni = %s AND password = %s"
        self.cursor.execute(sql, (dni, password_hash))
        return self.cursor.fetchone()

# -------------------------------
# CLASE CARTÓN
# -------------------------------

class Carton(Tabla):
    def insertar_carton(self, disposicion, valor, color, activo, cliente_dni):
        # Verificar si la columna fecha_creacion existe
        try:
            # Intentar con fecha_creacion (estructura nueva)
            sql = """
                INSERT INTO Carton (disposicion, valor, color, activo, cliente_dni, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(sql, (disposicion, valor, color, activo, cliente_dni, datetime.now()))
        except Exception as e:
            if "fecha_creacion" in str(e):
                # Fallback para estructura anterior (sin fecha_creacion)
                sql = """
                    INSERT INTO Carton (disposicion, valor, color, activo, cliente_dni)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.execute(sql, (disposicion, valor, color, activo, cliente_dni))
            else:
                raise e
        return self.cursor.lastrowid

    def generar_carton(self, cliente_dni):
        """Generar un cartón de bingo argentino para un cliente"""
        hoja = generar_cartones()  # Esto genera 6 cartones (18 filas en total)
        
        # Convertimos la disposición a JSON para guardarla en la base de datos
        disposicion_json = json.dumps(hoja)
        valor = 1000
        color = random.choice(['rojo', 'azul', 'verde', 'amarillo', 'morado', 'naranja'])
        activo = False  # Esto se cambia si el cartón se juega en una partida
        
        # Insertamos el cartón en la base de datos
        carton_id = self.insertar_carton(disposicion_json, valor, color, activo, cliente_dni)
        return carton_id, hoja

    def obtener_cartones_cliente(self, cliente_dni, activos_solo=False):
        """Obtener todos los cartones de un cliente"""
        # Verificar qué columnas existen en la tabla
        try:
            self.cursor.execute("DESCRIBE Carton")
            columnas = [row['Field'] for row in self.cursor.fetchall()]
            tiene_fecha_creacion = 'fecha_creacion' in columnas
        except:
            tiene_fecha_creacion = False
        
        # Construir query según columnas disponibles
        if tiene_fecha_creacion:
            sql = """
                SELECT id, disposicion, valor, color, activo, fecha_creacion 
                FROM Carton WHERE cliente_dni = %s 
            """
        else:
            sql = """
                SELECT id, disposicion, valor, color, activo 
                FROM Carton WHERE cliente_dni = %s 
            """
        
        params = [cliente_dni]
        
        if activos_solo:
            sql += " AND activo = %s"
            params.append(True)
            
        sql += " ORDER BY id DESC"  # Ordenar por ID si no hay fecha_creacion
        
        self.cursor.execute(sql, params)
        resultados = self.cursor.fetchall()
        
        # Agregar fecha_creacion dummy si no existe
        if not tiene_fecha_creacion:
            for resultado in resultados:
                resultado['fecha_creacion'] = datetime.now()
        
        return resultados

    def obtener_carton_por_id(self, carton_id):
        """Obtener un cartón específico por ID"""
        sql = "SELECT * FROM Carton WHERE id = %s"
        self.cursor.execute(sql, (carton_id,))
        return self.cursor.fetchone()

    def activar_carton(self, carton_id):
        """Activar cartón para jugar"""
        sql = "UPDATE Carton SET activo = %s WHERE id = %s"
        self.cursor.execute(sql, (True, carton_id))

    def desactivar_carton(self, carton_id):
        """Desactivar cartón después del juego"""
        sql = "UPDATE Carton SET activo = %s WHERE id = %s"
        self.cursor.execute(sql, (False, carton_id))

    def eliminar_carton(self, carton_id):
        """Eliminar cartón de la base de datos"""
        sql = "DELETE FROM Carton WHERE id = %s"
        self.cursor.execute(sql, (carton_id,))

# -------------------------------
# CLASE APUESTA
# -------------------------------

class Apuesta(Tabla):
    def insertar_apuesta(self, cliente_dni, carton_id, estado="en juego", ganancia=0):
        sql = """
            INSERT INTO Apuesta (cliente_dni, carton_id, estado, ganancia, fecha_apuesta)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (cliente_dni, carton_id, estado, ganancia, datetime.now()))
        return self.cursor.lastrowid

    def actualizar_estado(self, apuesta_id, nuevo_estado, ganancia=0):
        sql = """
            UPDATE Apuesta SET estado = %s, ganancia = %s WHERE id = %s
        """
        self.cursor.execute(sql, (nuevo_estado, ganancia, apuesta_id))

    def obtener_apuestas_cliente(self, cliente_dni, limite=None):
        """Obtener historial de apuestas de un cliente"""
        sql = """
            SELECT a.*, c.disposicion, c.color, c.valor
            FROM Apuesta a
            JOIN Carton c ON a.carton_id = c.id
            WHERE a.cliente_dni = %s
            ORDER BY a.fecha_apuesta DESC
        """
        params = [cliente_dni]
        
        if limite:
            sql += " LIMIT %s"
            params.append(limite)
            
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def obtener_estadisticas_cliente(self, cliente_dni):
        """Obtener estadísticas completas de un cliente"""
        sql = """
            SELECT 
                COUNT(*) as total_partidas,
                SUM(CASE WHEN estado = 'ganada' THEN 1 ELSE 0 END) as partidas_ganadas,
                SUM(CASE WHEN estado = 'perdida' THEN 1 ELSE 0 END) as partidas_perdidas,
                SUM(CASE WHEN estado = 'en juego' THEN 1 ELSE 0 END) as partidas_en_curso,
                SUM(CASE WHEN ganancia > 0 THEN ganancia ELSE 0 END) as ganancias_totales,
                SUM(CASE WHEN ganancia < 0 THEN ABS(ganancia) ELSE 0 END) as perdidas_totales,
                AVG(CASE WHEN ganancia != 0 THEN ganancia ELSE NULL END) as ganancia_promedio,
                MAX(ganancia) as mayor_ganancia,
                MIN(ganancia) as mayor_perdida
            FROM Apuesta 
            WHERE cliente_dni = %s
        """
        self.cursor.execute(sql, (cliente_dni,))
        resultado = self.cursor.fetchone()
        
        # Validar y limpiar valores None
        if resultado:
            # Convertir None a 0 para valores numéricos
            for key, value in resultado.items():
                if value is None:
                    if key in ['ganancia_promedio']:
                        resultado[key] = 0.0
                    else:
                        resultado[key] = 0
        
        # Calcular ratio de victoria
        total = resultado.get('total_partidas') or 0
        ganadas = resultado.get('partidas_ganadas') or 0
        ratio_victoria = (ganadas / total * 100) if total > 0 else 0
        
        resultado['ratio_victoria'] = round(ratio_victoria, 2)
        return resultado

# -------------------------------
# CLASE PARTIDA
# -------------------------------

class Partida(Tabla):
    def crear_partida(self, cliente_dni, carton_id):
        """Crear nueva partida"""
        sql = """
            INSERT INTO Partida (hora_inicio, jugadores, cliente_dni, carton_id, estado) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (datetime.now(), 1, cliente_dni, carton_id, 'en_curso'))
        return self.cursor.lastrowid

    def cerrar_partida(self, partida_id, numeros_cantados, resultado, ganancia=0):
        """Cerrar partida con resultado"""
        sql = """
            UPDATE Partida
            SET hora_fin = %s, numeros_cantados = %s, resultado = %s, ganancia = %s, estado = %s
            WHERE id = %s
        """
        self.cursor.execute(sql, (datetime.now(), json.dumps(numeros_cantados), resultado, ganancia, 'finalizada', partida_id))

    def obtener_partidas_cliente(self, cliente_dni, limite=None):
        """Obtener historial de partidas de un cliente"""
        sql = """
            SELECT p.*, c.color, c.valor
            FROM Partida p
            LEFT JOIN Carton c ON p.carton_id = c.id
            WHERE p.cliente_dni = %s
            ORDER BY p.hora_inicio DESC
        """
        params = [cliente_dni]
        
        if limite:
            sql += " LIMIT %s"
            params.append(limite)
            
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def obtener_partida_actual(self, cliente_dni):
        """Obtener partida en curso del cliente"""
        sql = """
            SELECT * FROM Partida 
            WHERE cliente_dni = %s AND estado = 'en_curso'
            ORDER BY hora_inicio DESC LIMIT 1
        """
        self.cursor.execute(sql, (cliente_dni,))
        return self.cursor.fetchone()

# -------------------------------
# CLASE PREMIO
# -------------------------------

class Premio(Tabla):
    def asignar_premio(self, partida_id, descripcion, valor, ganador_dni):
        sql = """
            INSERT INTO Premio (partida_id, descripcion, valor, ganador_dni, fecha_premio)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (partida_id, descripcion, valor, ganador_dni, datetime.now()))

    def listar_premios_cliente(self, cliente_dni):
        """Listar premios ganados por un cliente"""
        sql = """
            SELECT p.*, pa.hora_inicio
            FROM Premio p
            JOIN Partida pa ON p.partida_id = pa.id
            WHERE p.ganador_dni = %s
            ORDER BY p.fecha_premio DESC
        """
        self.cursor.execute(sql, (cliente_dni,))
        return self.cursor.fetchall()
    
# -------------------------------
# CLASE REPORTES
# -------------------------------

class Reportes(Tabla):
    def reporte_usuario_completo(self, cliente_dni):
        """Reporte completo de un usuario específico"""
        sql = """
            SELECT 
                c.dni, c.nombre, c.apellido, c.mail, c.saldo, c.fecha_reg,
                COUNT(a.id) as total_partidas,
                SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) as ganadas,
                SUM(CASE WHEN a.estado = 'perdida' THEN 1 ELSE 0 END) as perdidas,
                SUM(a.ganancia) as ganancia_total,
                MAX(a.ganancia) as mayor_ganancia,
                AVG(a.ganancia) as ganancia_promedio,
                COUNT(DISTINCT car.color) as colores_jugados,
                DATEDIFF(NOW(), c.fecha_reg) as dias_registrado
            FROM Cliente c
            LEFT JOIN Apuesta a ON c.dni = a.cliente_dni
            LEFT JOIN Carton car ON a.carton_id = car.id
            WHERE c.dni = %s
            GROUP BY c.dni
        """
        self.cursor.execute(sql, (cliente_dni,))
        return self.cursor.fetchone()
    
    def reporte_top_jugadores(self, limite=10):
        """Top jugadores por diferentes métricas"""
        sql = """
            SELECT 
                c.dni, c.nombre, c.apellido,
                COUNT(a.id) as total_partidas,
                SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) as ganadas,
                (SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.id)) as ratio_victoria,
                SUM(a.ganancia) as ganancia_total,
                c.saldo
            FROM Cliente c
            LEFT JOIN Apuesta a ON c.dni = a.cliente_dni
            GROUP BY c.dni
            HAVING total_partidas > 0
            ORDER BY ganancia_total DESC, ratio_victoria DESC
            LIMIT %s
        """
        self.cursor.execute(sql, (limite,))
        return self.cursor.fetchall()
    
    def reporte_actividad_diaria(self, dias=30):
        """Reporte de actividad de los últimos N días"""
        sql = """
            SELECT 
                DATE(a.fecha_apuesta) as fecha,
                COUNT(a.id) as partidas_del_dia,
                COUNT(DISTINCT a.cliente_dni) as jugadores_unicos,
                SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) as partidas_ganadas,
                SUM(a.ganancia) as ganancia_total_dia
            FROM Apuesta a
            WHERE a.fecha_apuesta >= DATE_SUB(NOW(), INTERVAL %s DAY)
            GROUP BY DATE(a.fecha_apuesta)
            ORDER BY fecha DESC
        """
        self.cursor.execute(sql, (dias,))
        return self.cursor.fetchall()
    
    def reporte_colores_populares(self):
        """Colores de cartones más populares"""
        sql = """
            SELECT 
                car.color,
                COUNT(a.id) as veces_jugado,
                SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) as veces_ganado,
                (SUM(CASE WHEN a.estado = 'ganada' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.id)) as ratio_exito
            FROM Carton car
            JOIN Apuesta a ON car.id = a.carton_id
            GROUP BY car.color
            ORDER BY veces_jugado DESC
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def reporte_estadisticas_globales(self):
        """Estadísticas globales del sistema"""
        sql = """
            SELECT 
                (SELECT COUNT(*) FROM Cliente) as total_usuarios,
                (SELECT COUNT(*) FROM Apuesta) as total_partidas,
                (SELECT COUNT(*) FROM Carton) as total_cartones_generados,
                (SELECT SUM(ganancia) FROM Apuesta WHERE ganancia > 0) as ganancias_totales,
                (SELECT AVG(saldo) FROM Cliente) as saldo_promedio,
                (SELECT COUNT(*) FROM Apuesta WHERE fecha_apuesta >= DATE_SUB(NOW(), INTERVAL 7 DAY)) as partidas_ultima_semana,
                (SELECT COUNT(DISTINCT cliente_dni) FROM Apuesta WHERE fecha_apuesta >= DATE_SUB(NOW(), INTERVAL 7 DAY)) as usuarios_activos_semana
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

# -------------------------------
# OPTIMIZACIÓN DE RENDIMIENTO
# -------------------------------

class PerformanceOptimizer(Tabla):
    def limpiar_datos_antiguos(self, dias_antiguedad=90):
        """Limpiar datos antiguos para mejorar rendimiento"""
        # Eliminar apuestas muy antiguas
        sql_apuestas = """
            DELETE FROM Apuesta 
            WHERE fecha_apuesta < DATE_SUB(NOW(), INTERVAL %s DAY)
            AND estado != 'en juego'
        """
        self.cursor.execute(sql_apuestas, (dias_antiguedad,))
        
        # Eliminar cartones huérfanos (sin apuestas asociadas)
        sql_cartones = """
            DELETE car FROM Carton car
            LEFT JOIN Apuesta a ON car.id = a.carton_id
            WHERE a.carton_id IS NULL
            AND car.activo = FALSE
        """
        self.cursor.execute(sql_cartones)
        
        return self.cursor.rowcount
    
    def optimizar_indices(self):
        """Crear/optimizar índices para mejor rendimiento"""
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_apuesta_fecha ON Apuesta(fecha_apuesta)",
            "CREATE INDEX IF NOT EXISTS idx_apuesta_estado ON Apuesta(estado)",
            "CREATE INDEX IF NOT EXISTS idx_carton_color ON Carton(color)",
            "CREATE INDEX IF NOT EXISTS idx_cliente_fecha_reg ON Cliente(fecha_reg)",
            "OPTIMIZE TABLE Cliente",
            "OPTIMIZE TABLE Apuesta", 
            "OPTIMIZE TABLE Carton"
        ]
        
        resultados = []
        for sql in indices:
            try:
                self.cursor.execute(sql)
                resultados.append(f"✅ {sql[:50]}...")
            except Exception as e:
                resultados.append(f"❌ Error: {str(e)[:50]}...")
        
        return resultados
    
    def estadisticas_rendimiento(self):
        """Obtener estadísticas de rendimiento de la BD"""
        sql = """
            SELECT 
                table_name as tabla,
                table_rows as filas,
                ROUND(((data_length + index_length) / 1024 / 1024), 2) as tamaño_mb,
                ROUND((data_length / 1024 / 1024), 2) as datos_mb,
                ROUND((index_length / 1024 / 1024), 2) as indices_mb
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            AND table_name IN ('Cliente', 'Carton', 'Apuesta', 'Partida', 'Premio')
            ORDER BY (data_length + index_length) DESC
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()