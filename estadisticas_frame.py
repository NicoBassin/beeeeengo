import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from backend import Apuesta, Cliente, Premio
from backend import Reportes, PerformanceOptimizer

class EstadisticasFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.usuario_datos = usuario_datos or {}
        
        self._crear_interfaz()
        self._cargar_estadisticas()

    def _crear_interfaz(self):
        # Header
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame,
                text="📈 Estadísticas y Reportes",
                font=("Arial", 18, "bold"),
                fg="#2c3e50",
                bg="#f0f0f0").pack(side="left")
        
        ttk.Button(header_frame,
                  text="🔄 Actualizar",
                  command=self._cargar_estadisticas,
                  style='Secondary.TButton').pack(side="right")
        
        self.stats_notebook = ttk.Notebook(self)
        self.stats_notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self._crear_mis_estadisticas()
        
        self._crear_reportes_globales()
        self._crear_herramientas_admin()

    def _crear_mis_estadisticas(self):
        """Pestaña con todas las estadísticas personales"""
        # Frame para la pestaña personal
        personal_frame = tk.Frame(self.stats_notebook, bg="#f0f0f0")
        self.stats_notebook.add(personal_frame, text="👤 Mis Estadísticas")
        
        self._crear_estadisticas_generales_personal(personal_frame)
        self._crear_estadisticas_financieras_personal(personal_frame)
        self._crear_logros_personal(personal_frame)

    def _crear_estadisticas_generales_personal(self, parent):
        """Estadísticas generales de juego"""
        frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Título
        title_frame = tk.Frame(frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        tk.Label(title_frame,
                text="🎮 Estadísticas Generales",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(side="left")
        
        # Grid de estadísticas
        self.stats_general_frame = tk.Frame(frame, bg="#ffffff")
        self.stats_general_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.general_labels = {}

    def _crear_estadisticas_financieras_personal(self, parent):
        """Estadísticas financieras"""
        frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        frame.pack(fill="x", padx=20, pady=10)
        
        # Título
        title_frame = tk.Frame(frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        tk.Label(title_frame,
                text="💰 Estadísticas Financieras",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(side="left")
        
        # Grid de estadísticas financieras
        self.stats_financiero_frame = tk.Frame(frame, bg="#ffffff")
        self.stats_financiero_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.financiero_labels = {}

    def _crear_logros_personal(self, parent):
        """Sección de logros y premios"""
        frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Título
        title_frame = tk.Frame(frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        tk.Label(title_frame,
                text="🏆 Logros y Premios",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(side="left")
        
        # Contenedor de logros
        self.logros_frame = tk.Frame(frame, bg="#ffffff")
        self.logros_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def _crear_reportes_globales(self):
        """Pestaña de reportes globales del sistema"""
        global_frame = tk.Frame(self.stats_notebook, bg="#ffffff")
        self.stats_notebook.add(global_frame, text="🌍 Reportes Globales")
        
        # Canvas con scroll
        canvas = tk.Canvas(global_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(global_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        tk.Label(scrollable_frame,
                text="🌍 Estadísticas del Sistema Completo",
                font=("Arial", 16, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=20)
        
        # Contenedores para diferentes tipos de datos
        self.global_stats_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        self.global_stats_frame.pack(fill="x", padx=30, pady=10)
        
        self.top_jugadores_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        self.top_jugadores_frame.pack(fill="x", padx=30, pady=20)
        
        self.colores_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        self.colores_frame.pack(fill="x", padx=30, pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _crear_herramientas_admin(self):
        """NUEVA: Pestaña de herramientas administrativas"""
        admin_frame = tk.Frame(self.stats_notebook, bg="#ffffff")
        self.stats_notebook.add(admin_frame, text="⚡ Herramientas")
        
        # Título
        tk.Label(admin_frame,
                text="⚡ Herramientas de Optimización",
                font=("Arial", 16, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=20)
        
        # Descripción
        tk.Label(admin_frame,
                text="Optimiza el rendimiento de la base de datos y limpia datos antiguos",
                font=("Arial", 11),
                fg="#7f8c8d",
                bg="#ffffff").pack(pady=(0, 20))
        
        # Botones de herramientas
        botones_frame = tk.Frame(admin_frame, bg="#ffffff")
        botones_frame.pack(fill="x", padx=30, pady=20)
        
        ttk.Button(botones_frame,
                  text="🧹 Limpiar Datos Antiguos (>90 días)",
                  command=self._limpiar_datos,
                  style='Secondary.TButton').pack(fill="x", pady=(0, 10))
        
        ttk.Button(botones_frame,
                  text="🚀 Optimizar Base de Datos",
                  command=self._optimizar_bd,
                  style='Secondary.TButton').pack(fill="x", pady=(0, 10))
        
        ttk.Button(botones_frame,
                  text="📊 Ver Estadísticas de BD",
                  command=self._ver_stats_bd,
                  style='Primary.TButton').pack(fill="x")
        
        # Frame para mostrar resultados
        self.admin_resultados = tk.Frame(admin_frame, bg="#f8f9fa", relief="solid", bd=1, height=200)
        self.admin_resultados.pack(fill="x", padx=30, pady=20)
        self.admin_resultados.pack_propagate(False)
        
        tk.Label(self.admin_resultados,
                text="🔧 Resultados de Operaciones",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#f8f9fa").pack(pady=15)

    def _cargar_estadisticas(self):
        """Cargar todas las estadísticas"""
        try:
            # CARGAR ESTADÍSTICAS PERSONALES
            apuesta_db = Apuesta()
            cliente_db = Cliente()
            
            stats = apuesta_db.obtener_estadisticas_cliente(self.usuario_datos.get('dni'))
            saldo_actual = cliente_db.obtener_saldo(self.usuario_datos.get('dni'))
            
            apuesta_db.cerrar()
            cliente_db.cerrar()
            
            # Actualizar estadísticas personales
            self._actualizar_estadisticas_generales(stats)
            self._actualizar_estadisticas_financieras(stats, saldo_actual)
            self._actualizar_logros(stats)
            
            # CARGAR REPORTES GLOBALES
            self._cargar_reportes_globales()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al cargar estadísticas: {str(e)}")

    def _actualizar_estadisticas_generales(self, stats):
        """Actualizar estadísticas generales"""
        # Limpiar frame
        for widget in self.stats_general_frame.winfo_children():
            widget.destroy()
        
        # Validar todos los valores para evitar comparaciones None
        total_partidas = stats.get('total_partidas') or 0
        partidas_ganadas = stats.get('partidas_ganadas') or 0
        partidas_perdidas = stats.get('partidas_perdidas') or 0
        partidas_en_curso = stats.get('partidas_en_curso') or 0
        ratio_victoria = stats.get('ratio_victoria') or 0
        
        # Datos generales
        datos_generales = [
            ("🎮 Partidas Jugadas", total_partidas, "#3498db"),
            ("🏆 Partidas Ganadas", partidas_ganadas, "#2ecc71"),
            ("❌ Partidas Perdidas", partidas_perdidas, "#e74c3c"),
            ("⏳ En Curso", partidas_en_curso, "#f39c12"),
            ("📊 Ratio de Victoria", f"{ratio_victoria}%", "#9b59b6"),
            ("📅 Días Jugando", self._calcular_dias_jugando(), "#34495e")
        ]
        
        # Crear grid 3x2
        for i, (label, value, color) in enumerate(datos_generales):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(self.stats_general_frame, bg="#f8f9fa", relief="solid", bd=1)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            self.stats_general_frame.grid_columnconfigure(col, weight=1)
            
            tk.Label(stat_frame,
                    text=label,
                    font=("Arial", 9),
                    fg="#6c757d",
                    bg="#f8f9fa").pack(pady=(10, 2))
            
            tk.Label(stat_frame,
                    text=str(value),
                    font=("Arial", 14, "bold"),
                    fg=color,
                    bg="#f8f9fa").pack(pady=(0, 10))

    def _actualizar_estadisticas_financieras(self, stats, saldo_actual):
        """Actualizar estadísticas financieras"""
        # Limpiar frame
        for widget in self.stats_financiero_frame.winfo_children():
            widget.destroy()
        
        # Calcular datos financieros con validación de None
        ganancias_totales = stats.get('ganancias_totales') or 0
        perdidas_totales = stats.get('perdidas_totales') or 0
        balance_neto = ganancias_totales - perdidas_totales
        mayor_ganancia = stats.get('mayor_ganancia') or 0
        ganancia_promedio = stats.get('ganancia_promedio') or 0
        
        # Validar saldo_actual
        if saldo_actual is None:
            saldo_actual = 0
        
        datos_financieros = [
            ("💰 Saldo Actual", f"${saldo_actual}", "#27ae60"),
            ("📈 Ganancias Totales", f"${ganancias_totales}", "#2ecc71"),
            ("📉 Pérdidas Totales", f"${perdidas_totales}", "#e74c3c"),
            ("⚖️ Balance Neto", f"${balance_neto}", "#27ae60" if balance_neto >= 0 else "#e74c3c"),
            ("🎯 Mayor Ganancia", f"${mayor_ganancia}", "#f39c12"),
            ("📊 Ganancia Promedio", f"${ganancia_promedio:.2f}", "#9b59b6")
        ]
        
        # Crear grid 3x2
        for i, (label, value, color) in enumerate(datos_financieros):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(self.stats_financiero_frame, bg="#f8f9fa", relief="solid", bd=1)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            self.stats_financiero_frame.grid_columnconfigure(col, weight=1)
            
            tk.Label(stat_frame,
                    text=label,
                    font=("Arial", 9),
                    fg="#6c757d",
                    bg="#f8f9fa").pack(pady=(10, 2))
            
            tk.Label(stat_frame,
                    text=str(value),
                    font=("Arial", 14, "bold"),
                    fg=color,
                    bg="#f8f9fa").pack(pady=(0, 10))

    def _actualizar_logros(self, stats):
        """Actualizar sección de logros"""
        # Limpiar frame
        for widget in self.logros_frame.winfo_children():
            widget.destroy()
        
        # Definir logros posibles
        logros = self._calcular_logros(stats)
        
        if not logros:
            tk.Label(self.logros_frame,
                    text="🏆 ¡Juega más partidas para desbloquear logros!",
                    font=("Arial", 12),
                    fg="#7f8c8d",
                    bg="#ffffff").pack(pady=30)
            return
        
        # Mostrar logros en grid
        logros_grid = tk.Frame(self.logros_frame, bg="#ffffff")
        logros_grid.pack(fill="x", pady=10)
        
        for i, logro in enumerate(logros):
            row = i // 3
            col = i % 3
            
            logro_frame = tk.Frame(logros_grid, bg="#fff3cd", relief="solid", bd=1)
            logro_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            logros_grid.grid_columnconfigure(col, weight=1)
            
            tk.Label(logro_frame,
                    text=logro['emoji'],
                    font=("Arial", 20),
                    bg="#fff3cd").pack(pady=(10, 5))
            
            tk.Label(logro_frame,
                    text=logro['titulo'],
                    font=("Arial", 10, "bold"),
                    fg="#856404",
                    bg="#fff3cd").pack()
            
            tk.Label(logro_frame,
                    text=logro['descripcion'],
                    font=("Arial", 8),
                    fg="#856404",
                    bg="#fff3cd").pack(pady=(2, 10))

    def _calcular_logros(self, stats):
        """Calcular logros desbloqueados"""
        logros = []
        
        # Validar todos los valores para evitar comparaciones None
        total_partidas = stats.get('total_partidas') or 0
        partidas_ganadas = stats.get('partidas_ganadas') or 0
        ratio_victoria = stats.get('ratio_victoria') or 0
        mayor_ganancia = stats.get('mayor_ganancia') or 0
        
        # Logro: Primera partida
        if total_partidas >= 1:
            logros.append({
                'emoji': '🎮',
                'titulo': 'Primer Juego',
                'descripcion': 'Jugaste tu primera partida'
            })
        
        # Logro: Primera victoria
        if partidas_ganadas >= 1:
            logros.append({
                'emoji': '🏆',
                'titulo': 'Primera Victoria',
                'descripcion': 'Ganaste tu primera partida'
            })
        
        # Logro: Jugador frecuente
        if total_partidas >= 10:
            logros.append({
                'emoji': '🎯',
                'titulo': 'Jugador Frecuente',
                'descripcion': 'Jugaste 10 partidas'
            })
        
        # Logro: Racha ganadora
        if partidas_ganadas >= 5:
            logros.append({
                'emoji': '🔥',
                'titulo': 'En Racha',
                'descripcion': 'Ganaste 5 partidas'
            })
        
        # Logro: Alto ratio de victoria
        if ratio_victoria >= 70 and total_partidas >= 5:
            logros.append({
                'emoji': '⭐',
                'titulo': 'Maestro del Bingo',
                'descripcion': 'Ratio de victoria >70%'
            })
        
        # Logro: Gran ganancia
        if mayor_ganancia >= 5000:
            logros.append({
                'emoji': '💎',
                'titulo': 'Gran Premio',
                'descripcion': 'Ganaste $5000 o más'
            })
        
        return logros

    def _calcular_dias_jugando(self):
        """Calcular días desde el registro (FUNCIÓN ORIGINAL MANTENIDA)"""
        fecha_registro = self.usuario_datos.get('fecha_reg')
        if not fecha_registro:
            return 0
        
        if isinstance(fecha_registro, str):
            try:
                fecha_registro = datetime.strptime(fecha_registro, "%Y-%m-%d %H:%M:%S")
            except:
                return 0
        
        dias = (datetime.now() - fecha_registro).days
        return max(1, dias)  # Mínimo 1 día

    def actualizar_estadisticas(self):
        """Método público para actualizar las estadísticas (FUNCIÓN ORIGINAL MANTENIDA)"""
        self._cargar_estadisticas()

    def mostrar_estadisticas_post_partida(self, resultado_partida):
        """Mostrar estadísticas después de terminar una partida (FUNCIÓN ORIGINAL MANTENIDA)"""
        # Actualizar estadísticas
        self._cargar_estadisticas()
        
        # Mostrar ventana modal con resultado
        self._mostrar_modal_resultado(resultado_partida)

    def _mostrar_modal_resultado(self, resultado):
        """Mostrar modal con resultado de la partida (FUNCIÓN ORIGINAL MANTENIDA)"""
        ventana = tk.Toplevel(self)
        ventana.title("🎉 Resultado de la Partida")
        ventana.geometry("400x300")
        ventana.resizable(False, False)
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
        # Contenido
        content_frame = tk.Frame(ventana, bg="#ffffff", relief="solid", bd=1)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Emoji y título según resultado
        if resultado.get('ganado', False):
            emoji = "🏆"
            titulo = "¡Felicitaciones!"
            subtitulo = "¡Ganaste la partida!"
            color = "#2ecc71"
        else:
            emoji = "😔"
            titulo = "Partida terminada"
            subtitulo = "¡Mejor suerte la próxima vez!"
            color = "#e74c3c"
        
        tk.Label(content_frame,
                text=emoji,
                font=("Arial", 48),
                bg="#ffffff").pack(pady=(30, 10))
        
        tk.Label(content_frame,
                text=titulo,
                font=("Arial", 18, "bold"),
                fg=color,
                bg="#ffffff").pack()
        
        tk.Label(content_frame,
                text=subtitulo,
                font=("Arial", 12),
                fg="#7f8c8d",
                bg="#ffffff").pack(pady=(5, 20))
        
        # Resultado financiero
        ganancia = resultado.get('ganancia', 0)
        if ganancia > 0:
            resultado_text = f"Ganancia: +${ganancia}"
            resultado_color = "#2ecc71"
        else:
            resultado_text = f"Costo del cartón: -${abs(ganancia)}"
            resultado_color = "#e74c3c"
        
        tk.Label(content_frame,
                text=resultado_text,
                font=("Arial", 14, "bold"),
                fg=resultado_color,
                bg="#ffffff").pack()
        
        # Botones
        button_frame = tk.Frame(content_frame, bg="#ffffff")
        button_frame.pack(pady=(30, 20))
        
        ttk.Button(button_frame,
                  text="Ver Estadísticas",
                  command=lambda: [ventana.destroy(), self.master.notebook.select(4)],  # ← Actualizar índice
                  style='Primary.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cerrar",
                  command=ventana.destroy,
                  style='Secondary.TButton').pack(side="left")

    # ============================================================================
    # FUNCIONES PARA REPORTES GLOBALES Y HERRAMIENTAS
    # ============================================================================

    def _cargar_reportes_globales(self):
        """Cargar estadísticas globales del sistema"""
        try:
            reportes_db = Reportes()
            
            # Estadísticas generales del sistema
            stats = reportes_db.reporte_estadisticas_globales()
            self._mostrar_stats_globales(stats)
            
            # Top 5 jugadores
            top_jugadores = reportes_db.reporte_top_jugadores(5)
            self._mostrar_top_jugadores(top_jugadores)
            
            # Colores más populares
            colores = reportes_db.reporte_colores_populares()
            self._mostrar_colores_populares(colores)
            
            reportes_db.cerrar()
            
        except Exception as e:
            print(f"Error al cargar reportes globales: {str(e)}")

    def _mostrar_stats_globales(self, stats):
        """Mostrar estadísticas globales"""
        # Limpiar frame
        for widget in self.global_stats_frame.winfo_children():
            widget.destroy()
        
        if not stats:
            return
        
        tk.Label(self.global_stats_frame,
                text="📊 Métricas Generales",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 15))
        
        # Grid de estadísticas globales
        stats_grid = tk.Frame(self.global_stats_frame, bg="#ffffff")
        stats_grid.pack(fill="x")
        
        stats_data = [
            ("👥", "Total Usuarios", stats.get('total_usuarios', 0)),
            ("🎮", "Total Partidas", stats.get('total_partidas', 0)),
            ("🎫", "Cartones Creados", stats.get('total_cartones_generados', 0)),
            ("💰", "Ganancias Sistema", f"${stats.get('ganancias_totales', 0)}"),
            ("📊", "Saldo Promedio", f"${stats.get('saldo_promedio', 0):.2f}"),
            ("📅", "Activos 7 días", stats.get('usuarios_activos_semana', 0))
        ]
        
        for i, (emoji, titulo, valor) in enumerate(stats_data):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(stats_grid, bg="#f8f9fa", relief="solid", bd=1)
            stat_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            stats_grid.grid_columnconfigure(col, weight=1)
            
            tk.Label(stat_frame, text=emoji, font=("Arial", 20), bg="#f8f9fa").pack(pady=(10, 5))
            tk.Label(stat_frame, text=titulo, font=("Arial", 9), fg="#6c757d", bg="#f8f9fa").pack()
            tk.Label(stat_frame, text=str(valor), font=("Arial", 12, "bold"), fg="#2c3e50", bg="#f8f9fa").pack(pady=(5, 10))

    def _mostrar_top_jugadores(self, jugadores):
        """Mostrar ranking de mejores jugadores"""
        # Limpiar frame
        for widget in self.top_jugadores_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.top_jugadores_frame,
                text="🏆 Top 5 Jugadores",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 15))
        
        if not jugadores:
            tk.Label(self.top_jugadores_frame,
                    text="No hay datos de jugadores disponibles",
                    font=("Arial", 11),
                    fg="#7f8c8d",
                    bg="#ffffff").pack()
            return
        
        # Lista de mejores jugadores
        for i, jugador in enumerate(jugadores[:5], 1):
            player_frame = tk.Frame(self.top_jugadores_frame, bg="#f8f9fa", relief="solid", bd=1)
            player_frame.pack(fill="x", pady=2)
            
            # Posición y medalla
            pos_frame = tk.Frame(player_frame, bg="#f8f9fa")
            pos_frame.pack(side="left", padx=10, pady=5)
            
            medalla = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"#{i}"
            tk.Label(pos_frame,
                    text=medalla,
                    font=("Arial", 16 if i <= 3 else 12, "bold"),
                    fg="#2c3e50",
                    bg="#f8f9fa").pack()
            
            # Información del jugador
            info_frame = tk.Frame(player_frame, bg="#f8f9fa")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
            nombre = f"{jugador.get('nombre', '')} {jugador.get('apellido', '')}"
            tk.Label(info_frame,
                    text=nombre,
                    font=("Arial", 11, "bold"),
                    fg="#2c3e50",
                    bg="#f8f9fa",
                    anchor="w").pack(fill="x")
            
            # Stats del jugador
            total = jugador.get('total_partidas', 0)
            ganadas = jugador.get('ganadas', 0)
            ganancia = jugador.get('ganancia_total', 0)
            
            stats_text = f"Partidas: {total} | Ganadas: {ganadas} | Ganancia: ${ganancia}"
            tk.Label(info_frame,
                    text=stats_text,
                    font=("Arial", 9),
                    fg="#6c757d",
                    bg="#f8f9fa",
                    anchor="w").pack(fill="x")

    def _mostrar_colores_populares(self, colores):
        """Mostrar colores de cartones más populares"""
        # Limpiar frame
        for widget in self.colores_frame.winfo_children():
            widget.destroy()
        
        tk.Label(self.colores_frame,
                text="🎨 Colores Más Populares",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 15))
        
        if not colores:
            tk.Label(self.colores_frame,
                    text="No hay datos de colores disponibles",
                    font=("Arial", 11),
                    fg="#7f8c8d",
                    bg="#ffffff").pack()
            return
        
        # Grid de colores
        colores_grid = tk.Frame(self.colores_frame, bg="#ffffff")
        colores_grid.pack(fill="x")
        
        for i, color_data in enumerate(colores[:6]):  # Mostrar top 6
            col = i % 3
            row = i // 3
            
            color_frame = tk.Frame(colores_grid, bg="#f8f9fa", relief="solid", bd=1)
            color_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            colores_grid.grid_columnconfigure(col, weight=1)
            
            # Círculo de color
            color_hex = self._get_color_hex(color_data.get('color', 'gris'))
            tk.Label(color_frame,
                    text="●",
                    font=("Arial", 24),
                    fg=color_hex,
                    bg="#f8f9fa").pack(pady=(10, 5))
            
            # Nombre del color
            tk.Label(color_frame,
                    text=color_data.get('color', 'N/A').title(),
                    font=("Arial", 11, "bold"),
                    fg="#2c3e50",
                    bg="#f8f9fa").pack()
            
            # Estadísticas
            veces = color_data.get('veces_jugado', 0)
            ratio = color_data.get('ratio_exito', 0)
            tk.Label(color_frame,
                    text=f"{veces} partidas",
                    font=("Arial", 9),
                    fg="#6c757d",
                    bg="#f8f9fa").pack()
            
            tk.Label(color_frame,
                    text=f"{ratio:.1f}% éxito",
                    font=("Arial", 8),
                    fg="#6c757d",
                    bg="#f8f9fa").pack(pady=(0, 10))

    def _get_color_hex(self, color):
        """Obtener color hexadecimal"""
        colors = {
            'rojo': '#e74c3c',
            'azul': '#3498db',
            'verde': '#2ecc71',
            'amarillo': '#f1c40f',
            'morado': '#9b59b6',
            'naranja': '#e67e22'
        }
        return colors.get(color.lower(), '#95a5a6')

    # FUNCIONES DE HERRAMIENTAS ADMINISTRATIVAS

    def _limpiar_datos(self):
        """Limpiar datos antiguos de la base de datos"""
        respuesta = messagebox.askyesno("🧹 Limpiar Datos", 
                                       "¿Eliminar datos de partidas anteriores a 90 días?\n\n"
                                       "Esta acción no se puede deshacer.")
        if not respuesta:
            return
            
        try:
            optimizer = PerformanceOptimizer()
            filas_eliminadas = optimizer.limpiar_datos_antiguos(90)
            optimizer.cerrar()
            
            # Mostrar resultado
            self._mostrar_resultado_admin(f"✅ Eliminados {filas_eliminadas} registros antiguos")
            
            messagebox.showinfo("🧹 Limpieza Completada", 
                              f"Se eliminaron {filas_eliminadas} registros antiguos.")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al limpiar datos: {str(e)}")

    def _optimizar_bd(self):
        """Optimizar índices y rendimiento de la base de datos"""
        try:
            optimizer = PerformanceOptimizer()
            resultados = optimizer.optimizar_indices()
            optimizer.cerrar()
            
            # Mostrar resultados
            self._mostrar_resultado_admin("🚀 Optimización completada:")
            for resultado in resultados[:5]:  # Mostrar solo los primeros 5
                self._mostrar_resultado_admin(resultado[:60] + "..." if len(resultado) > 60 else resultado)
            
            messagebox.showinfo("🚀 Optimización Completada", 
                              f"Base de datos optimizada correctamente.\n"
                              f"Se ejecutaron {len(resultados)} operaciones.")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al optimizar: {str(e)}")

    def _ver_stats_bd(self):
        """Mostrar estadísticas detalladas de la base de datos"""
        try:
            optimizer = PerformanceOptimizer()
            stats = optimizer.estadisticas_rendimiento()
            optimizer.cerrar()
            
            # Crear ventana modal
            ventana = tk.Toplevel(self)
            ventana.title("📊 Estadísticas de Base de Datos")
            ventana.geometry("600x400")
            ventana.configure(bg="#f0f0f0")
            ventana.transient(self)
            ventana.grab_set()
            
            # Header
            header_frame = tk.Frame(ventana, bg="#2c3e50", height=60)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            tk.Label(header_frame,
                    text="📊 Estadísticas de Rendimiento",
                    font=("Arial", 16, "bold"),
                    fg="white",
                    bg="#2c3e50").pack(expand=True)
            
            # Contenido con scroll
            canvas = tk.Canvas(ventana, bg="#ffffff")
            scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#ffffff")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Mostrar estadísticas
            for stat in stats:
                stat_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
                stat_frame.pack(fill="x", padx=20, pady=5)
                
                tk.Label(stat_frame,
                        text=f"📋 {stat.get('tabla', 'N/A')}",
                        font=("Arial", 12, "bold"),
                        fg="#2c3e50",
                        bg="#f8f9fa").pack(anchor="w", padx=15, pady=(10, 5))
                
                detalles = f"Filas: {stat.get('filas', 0):,} | Tamaño: {stat.get('tamaño_mb', 0)} MB | Datos: {stat.get('datos_mb', 0)} MB | Índices: {stat.get('indices_mb', 0)} MB"
                tk.Label(stat_frame,
                        text=detalles,
                        font=("Arial", 10),
                        fg="#6c757d",
                        bg="#f8f9fa").pack(anchor="w", padx=15, pady=(0, 10))
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Botón cerrar
            ttk.Button(ventana,
                      text="Cerrar",
                      command=ventana.destroy,
                      style='Secondary.TButton').pack(pady=20)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al obtener estadísticas: {str(e)}")

    def _mostrar_resultado_admin(self, mensaje):
        """Mostrar resultado de operación administrativa"""
        resultado_label = tk.Label(self.admin_resultados,
                                 text=mensaje,
                                 font=("Arial", 10),
                                 fg="#2ecc71" if "✅" in mensaje or "🚀" in mensaje else "#2c3e50",
                                 bg="#f8f9fa",
                                 anchor="w",
                                 wraplength=400)
        resultado_label.pack(fill="x", padx=20, pady=2)