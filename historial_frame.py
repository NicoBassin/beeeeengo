import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from backend import Partida

class HistorialFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.usuario_datos = usuario_datos or {}
        
        self._crear_interfaz()
        self._cargar_historial()

    def _crear_interfaz(self):
        # Header
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame,
                text="📊 Historial de Partidas",
                font=("Arial", 18, "bold"),
                fg="#2c3e50",
                bg="#f0f0f0").pack(side="left")
        
        # Filtros
        filter_frame = tk.Frame(header_frame, bg="#f0f0f0")
        filter_frame.pack(side="right")
        
        tk.Label(filter_frame,
                text="Filtrar:",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#f0f0f0").pack(side="left", padx=(0, 5))
        
        self.filtro_var = tk.StringVar(value="todas")
        filtro_combo = ttk.Combobox(filter_frame,
                                   textvariable=self.filtro_var,
                                   values=["todas", "ganadas", "perdidas", "en juego"],
                                   state="readonly",
                                   width=12)
        filtro_combo.pack(side="left", padx=(0, 10))
        filtro_combo.bind("<<ComboboxSelected>>", lambda e: self._cargar_historial())
        
        ttk.Button(filter_frame,
                  text="🔄 Actualizar",
                  command=self._cargar_historial,
                  style='Secondary.TButton').pack(side="left")
        
        # Resumen rápido
        self._crear_resumen()
        
        # Lista de partidas
        self._crear_lista_partidas()

    def _crear_resumen(self):
        """Crear resumen rápido de estadísticas"""
        resumen_frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=1)
        resumen_frame.pack(fill="x", padx=20, pady=10)
        
        title_frame = tk.Frame(resumen_frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        tk.Label(title_frame,
                text="📈 Resumen Rápido",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(side="left")
        
        # Grid de estadísticas
        stats_grid = tk.Frame(resumen_frame, bg="#ffffff")
        stats_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        self.stats_labels = {}
        self._crear_stat_boxes(stats_grid)

    def _crear_stat_boxes(self, parent):
        """Crear cajas de estadísticas"""
        stats = [
            ("total", "🎮 Total Partidas", "0", "#3498db"),
            ("ganadas", "🏆 Ganadas", "0", "#2ecc71"),
            ("perdidas", "❌ Perdidas", "0", "#e74c3c"),
            ("ratio", "📊 Ratio Victoria", "0%", "#9b59b6")
        ]
        
        for i, (key, label, value, color) in enumerate(stats):
            stat_frame = tk.Frame(parent, bg="#f8f9fa", relief="solid", bd=1)
            stat_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            
            parent.grid_columnconfigure(i, weight=1)
            
            tk.Label(stat_frame,
                    text=label,
                    font=("Arial", 9),
                    fg="#6c757d",
                    bg="#f8f9fa").pack(pady=(10, 2))
            
            self.stats_labels[key] = tk.Label(stat_frame,
                                            text=value,
                                            font=("Arial", 16, "bold"),
                                            fg=color,
                                            bg="#f8f9fa")
            self.stats_labels[key].pack(pady=(0, 10))

    def _crear_lista_partidas(self):
        """Crear lista scrolleable de partidas"""
        container_frame = tk.Frame(self, bg="#f0f0f0")
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(container_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        self.partidas_container = tk.Frame(canvas, bg="#f0f0f0")
        
        self.partidas_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.partidas_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _cargar_historial(self):
        """Cargar historial desde la base de datos"""
        try:
            # DEBUG: Verificar DNI
            print(f"DEBUG HISTORIAL: DNI usuario = {self.usuario_datos.get('dni')}")
            
            partida_db = Partida()
            
            # Obtener partidas del cliente
            partidas = partida_db.obtener_partidas_cliente(self.usuario_datos.get('dni'), limite=50)
            
            # DEBUG: Verificar datos obtenidos
            print(f"DEBUG HISTORIAL: Partidas obtenidas = {len(partidas)}")
            if partidas:
                print(f"DEBUG HISTORIAL: Primera partida = {partidas[0]}")
            
            # Calcular estadísticas desde las partidas obtenidas
            stats = self._calcular_estadisticas(partidas)
            self._actualizar_resumen(stats)
            
            partida_db.cerrar()
            
            # Filtrar según selección
            filtro = self.filtro_var.get()
            print(f"DEBUG HISTORIAL: Filtro seleccionado = '{filtro}'")
            
            if filtro != "todas":
                partidas_antes = len(partidas)
                if filtro == "ganadas":
                    partidas = [p for p in partidas if p.get('resultado') == 'ganada']
                elif filtro == "perdidas":
                    partidas = [p for p in partidas if p.get('resultado') == 'perdida']
                elif filtro == "en juego":
                    partidas = [p for p in partidas if p.get('estado') == 'en_curso']
                
                print(f"DEBUG HISTORIAL: Después del filtro = {len(partidas)} (antes: {partidas_antes})")
            
            print(f"DEBUG HISTORIAL: Llamando _mostrar_partidas() con {len(partidas)} partidas")
            self._mostrar_partidas(partidas)
        
        except Exception as e:
            print(f"DEBUG HISTORIAL ERROR: {str(e)}")
            messagebox.showerror("❌ Error", f"Error al cargar historial: {str(e)}")

    def _calcular_estadisticas(self, partidas):
        """Calcular estadísticas desde las partidas"""
        if not partidas:
            return {
                'total_partidas': 0,
                'partidas_ganadas': 0,
                'partidas_perdidas': 0,
                'ratio_victoria': 0
            }
        
        total = len(partidas)
        ganadas = len([p for p in partidas if p.get('resultado') == 'ganada'])
        perdidas = len([p for p in partidas if p.get('resultado') == 'perdida'])
        ratio = round((ganadas / total) * 100, 1) if total > 0 else 0
        
        return {
            'total_partidas': total,
            'partidas_ganadas': ganadas,
            'partidas_perdidas': perdidas,
            'ratio_victoria': ratio
        }

    def _actualizar_resumen(self, stats):
        """Actualizar resumen de estadísticas"""
        if stats:
            # Validar todos los valores para evitar comparaciones None
            total_partidas = stats.get('total_partidas') or 0
            partidas_ganadas = stats.get('partidas_ganadas') or 0
            partidas_perdidas = stats.get('partidas_perdidas') or 0
            ratio_victoria = stats.get('ratio_victoria') or 0
            
            self.stats_labels['total'].configure(text=str(total_partidas))
            self.stats_labels['ganadas'].configure(text=str(partidas_ganadas))
            self.stats_labels['perdidas'].configure(text=str(partidas_perdidas))
            self.stats_labels['ratio'].configure(text=f"{ratio_victoria}%")

    def _mostrar_partidas(self, partidas):
        """Mostrar lista de partidas"""
        # DEBUG: Verificar datos recibidos
        print(f"DEBUG _mostrar_partidas: Recibí {len(partidas)} partidas")
        
        # Limpiar container
        for widget in self.partidas_container.winfo_children():
            widget.destroy()
        
        print(f"DEBUG _mostrar_partidas: Container limpiado")
        
        if not partidas:
            print(f"DEBUG _mostrar_partidas: Sin partidas - mostrando mensaje vacío")
            self._mostrar_sin_partidas()
            return
        
        print(f"DEBUG _mostrar_partidas: Creando widgets para {len(partidas)} partidas")
        
        # Mostrar partidas
        for i, partida in enumerate(partidas):
            print(f"DEBUG _mostrar_partidas: Creando widget {i+1} para partida ID {partida.get('id')}")
            self._crear_partida_widget(partida, i)
        
        print(f"DEBUG _mostrar_partidas: Terminó de crear todos los widgets")

    def _mostrar_sin_partidas(self):
        """Mostrar mensaje cuando no hay partidas"""
        empty_frame = tk.Frame(self.partidas_container, bg="#ffffff", relief="solid", bd=1)
        empty_frame.pack(fill="x", pady=10)
        
        content_frame = tk.Frame(empty_frame, bg="#ffffff")
        content_frame.pack(pady=50, padx=50)
        
        tk.Label(content_frame,
                text="📊",
                font=("Arial", 48),
                bg="#ffffff").pack()
        
        tk.Label(content_frame,
                text="No hay partidas para mostrar",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack()
        
        filtro = self.filtro_var.get()
        if filtro != "todas":
            tk.Label(content_frame,
                    text=f"No se encontraron partidas {filtro}",
                    font=("Arial", 11),
                    fg="#7f8c8d",
                    bg="#ffffff").pack(pady=(5, 0))
        else:
            tk.Label(content_frame,
                    text="¡Comienza a jugar para ver tu historial aquí!",
                    font=("Arial", 11),
                    fg="#7f8c8d",
                    bg="#ffffff").pack(pady=(5, 0))

    def _crear_partida_widget(self, partida, index):
        """Crear widget para mostrar una partida"""
        # Frame principal
        partida_frame = tk.Frame(self.partidas_container, bg="#ffffff", relief="solid", bd=1)
        partida_frame.pack(fill="x", pady=5)
        
        # Header de la partida
        header_frame = tk.Frame(partida_frame, bg="#ffffff")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Info izquierda
        info_left = tk.Frame(header_frame, bg="#ffffff")
        info_left.pack(side="left", fill="y")
        
        # Estado con emoji
        estado = partida.get('estado', 'en_curso')
        resultado = partida.get('resultado')
        
        # Determinar el estado para mostrar
        if estado == 'en_curso':
            estado_display = 'en juego'
        elif estado == 'finalizada':
            estado_display = resultado or 'finalizada'
        else:
            estado_display = estado
            
        estado_emoji = self._get_estado_emoji(estado_display)
        estado_color = self._get_estado_color(estado_display)
        
        tk.Label(info_left,
                text=f"{estado_emoji} Partida #{partida.get('id', 'N/A')}",
                font=("Arial", 12, "bold"),
                fg=estado_color,
                bg="#ffffff").pack(anchor="w")
        
        fecha = partida.get('hora_inicio', datetime.now())
        if isinstance(fecha, str):
            try:
                fecha = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
            except:
                fecha = datetime.now()
        
        tk.Label(info_left,
                text=f"Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack(anchor="w")
        
        # Info centro (cartón)
        carton_frame = tk.Frame(header_frame, bg="#ffffff")
        carton_frame.pack(side="left", padx=(30, 0))
        
        color_carton = partida.get('color', 'gris')
        tk.Label(carton_frame,
                text="🎫",
                font=("Arial", 16),
                fg=self._get_color_hex(color_carton),
                bg="#ffffff").pack()
        
        tk.Label(carton_frame,
                text=f"Cartón {color_carton.title()}",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack()
        
        # Info derecha (resultado)
        resultado_frame = tk.Frame(header_frame, bg="#ffffff")
        resultado_frame.pack(side="right")
        
        ganancia = partida.get('ganancia', 0)
        valor_carton = partida.get('valor', 1000)
        
        if resultado == 'ganada':
            resultado_text = f"+${ganancia}"
            resultado_color = "#2ecc71"
        elif resultado == 'perdida':
            resultado_text = f"-${valor_carton}"
            resultado_color = "#e74c3c"
        else:
            resultado_text = "En curso"
            resultado_color = "#f39c12"
        
        tk.Label(resultado_frame,
                text="Resultado",
                font=("Arial", 9),
                fg="#7f8c8d",
                bg="#ffffff").pack()
        
        tk.Label(resultado_frame,
                text=resultado_text,
                font=("Arial", 12, "bold"),
                fg=resultado_color,
                bg="#ffffff").pack()
        
        # Botón ver detalles
        if estado != 'en_curso':
            ttk.Button(header_frame,
                      text="👁️ Detalles",
                      command=lambda p=partida: self._ver_detalles(p),
                      style='Secondary.TButton').pack(side="right", padx=(10, 0))

    def _get_estado_emoji(self, estado):
        """Obtener emoji según estado"""
        emojis = {
            'ganada': '🏆',
            'perdida': '❌',
            'en juego': '🎮',
            'en_curso': '🎮',
            'finalizada': '🏁'
        }
        return emojis.get(estado, '❓')

    def _get_estado_color(self, estado):
        """Obtener color según estado"""
        colors = {
            'ganada': '#2ecc71',
            'perdida': '#e74c3c',
            'en juego': '#f39c12',
            'en_curso': '#f39c12',
            'finalizada': '#6c757d'
        }
        return colors.get(estado, '#6c757d')

    def _get_color_hex(self, color):
        """Convertir nombre de color a hexadecimal"""
        colors = {
            'rojo': '#e74c3c',
            'azul': '#3498db',
            'verde': '#2ecc71',
            'amarillo': '#f1c40f',
            'gris': '#95a5a6'
        }
        return colors.get(color, '#95a5a6')

    def _ver_detalles(self, partida):
        """Mostrar detalles de la partida en ventana modal"""
        ventana = tk.Toplevel(self)
        ventana.title(f"Detalles - Partida #{partida.get('id', 'N/A')}")
        ventana.geometry("500x400")
        ventana.resizable(False, False)
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
        # Header
        header_frame = tk.Frame(ventana, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        estado = partida.get('estado', 'desconocido')
        emoji = self._get_estado_emoji(estado)
        
        tk.Label(header_frame,
                text=f"{emoji} Detalles de la Partida",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#2c3e50").pack(expand=True)
        
        # Contenido
        content_frame = tk.Frame(ventana, bg="#ffffff", relief="solid", bd=1)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información detallada
        info_frame = tk.Frame(content_frame, bg="#ffffff")
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Datos de la partida
        fecha_inicio = partida.get('hora_inicio', datetime.now())
        fecha_fin = partida.get('hora_fin', None)
        
        if isinstance(fecha_inicio, str):
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d %H:%M:%S")
            except:
                fecha_inicio = datetime.now()
        
        fecha_fin_str = "N/A"
        if fecha_fin:
            if isinstance(fecha_fin, str):
                try:
                    fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d %H:%M:%S")
                    fecha_fin_str = fecha_fin.strftime('%d/%m/%Y %H:%M:%S')
                except:
                    fecha_fin_str = fecha_fin
            else:
                fecha_fin_str = fecha_fin.strftime('%d/%m/%Y %H:%M:%S')
        
        # Obtener números cantados
        numeros_cantados = partida.get('numeros_cantados', '[]')
        if isinstance(numeros_cantados, str):
            try:
                numeros_cantados = json.loads(numeros_cantados)
            except:
                numeros_cantados = []
        
        datos = [
            ("🆔 ID de Partida", partida.get('id', 'N/A')),
            ("📅 Fecha Inicio", fecha_inicio.strftime('%d/%m/%Y %H:%M:%S')),
            ("🏁 Fecha Fin", fecha_fin_str),
            ("👥 Jugadores", partida.get('jugadores', 1)),
            ("🎫 Cartón ID", partida.get('carton_id', 'N/A')),
            ("🎨 Color del Cartón", partida.get('color', 'N/A').title()),
            ("💰 Valor del Cartón", f"${partida.get('valor', 0)}"),
            ("📊 Estado", partida.get('estado', 'N/A').title()),
            ("🎯 Resultado", partida.get('resultado', 'N/A').title() if partida.get('resultado') else 'N/A'),
            ("🏆 Ganancia", f"${partida.get('ganancia', 0)}"),
            ("👤 Cliente DNI", partida.get('cliente_dni', 'N/A')),
            ("🔢 Números Cantados", f"{len(numeros_cantados)} números" if numeros_cantados else "Ninguno")
        ]
        
        for label, valor in datos:
            row_frame = tk.Frame(info_frame, bg="#ffffff")
            row_frame.pack(fill="x", pady=5)
            
            tk.Label(row_frame,
                    text=label,
                    font=("Arial", 11, "bold"),
                    fg="#2c3e50",
                    bg="#ffffff",
                    width=20,
                    anchor="w").pack(side="left")
            
            tk.Label(row_frame,
                    text=str(valor),
                    font=("Arial", 11),
                    fg="#495057",
                    bg="#ffffff",
                    anchor="w").pack(side="left", padx=(10, 0))
        
        # Botón cerrar
        ttk.Button(content_frame,
                  text="Cerrar",
                  command=ventana.destroy,
                  style='Secondary.TButton').pack(pady=(20, 20))

    def actualizar_historial(self):
        """Método público para actualizar el historial"""
        self._cargar_historial()