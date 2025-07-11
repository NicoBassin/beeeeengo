
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from backend import Cliente
from juego_frame import JuegoFrame
from cartones_frame import CartonesFrame
from historial_frame import HistorialFrame
from estadisticas_frame import EstadisticasFrame

class DashboardFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master.master  # Referencia a App
        self.usuario_datos = usuario_datos or {}
        
        # Variables de estado
        self.saldo_actual = 0
        self.actualizacion_saldo_id = None  # Para el timer de actualización
        
        self._crear_interfaz()
        self._cargar_saldo_inicial()
        self._iniciar_actualizacion_automatica()

    def _crear_interfaz(self):
        # Header con info del usuario
        self._crear_header()
        
        # Contenido principal con tabs
        self._crear_contenido_principal()

    def _crear_header(self):
        header_frame = tk.Frame(self, bg="#2c3e50", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Contenido del header
        header_content = tk.Frame(header_frame, bg="#2c3e50")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Info del usuario (izquierda)
        user_info = tk.Frame(header_content, bg="#2c3e50")
        user_info.pack(side="left", fill="y")
        
        nombre_completo = f"{self.usuario_datos.get('nombre', 'Usuario')} {self.usuario_datos.get('apellido', '')}"
        
        tk.Label(user_info,
                text=f"🎯 ¡Hola, {nombre_completo}!",
                font=("Arial", 14, "bold"),
                fg="white",
                bg="#2c3e50").pack(anchor="w")
        
        tk.Label(user_info,
                text=f"DNI: {self.usuario_datos.get('dni', 'N/A')} | Último acceso: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                font=("Arial", 10),
                fg="#bdc3c7",
                bg="#2c3e50").pack(anchor="w")
        
        # Saldo (centro)
        saldo_frame = tk.Frame(header_content, bg="#2c3e50")
        saldo_frame.pack(side="left", fill="y", padx=(50, 0))
        
        tk.Label(saldo_frame,
                text="💰 Saldo Actual",
                font=("Arial", 10),
                fg="#bdc3c7",
                bg="#2c3e50").pack()
        
        self.saldo_label = tk.Label(saldo_frame,
                                   text="$0",
                                   font=("Arial", 16, "bold"),
                                   fg="#2ecc71",
                                   bg="#2c3e50")
        self.saldo_label.pack()
        
        # Botones del header (derecha)
        header_buttons = tk.Frame(header_content, bg="#2c3e50")
        header_buttons.pack(side="right", fill="y")
        
        ttk.Button(header_buttons,
                  text="👤 Perfil",
                  command=self._mostrar_perfil,
                  style='Secondary.TButton').pack(side="right", padx=(10, 0))
        
        ttk.Button(header_buttons,
                  text="🚪 Cerrar Sesión",
                  command=self._cerrar_sesion,
                  style='Secondary.TButton').pack(side="right")

    def _crear_contenido_principal(self):
        # Notebook para tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Crear frames para cada pestaña
        self._crear_tabs()
        
        # Bind para actualizar contenido al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _crear_tabs(self):
        """Crear todas las pestañas del dashboard"""
        
        # Tab 1: Jugar Bingo
        self.juego_frame = JuegoFrame(self.notebook, self.usuario_datos)
        self.notebook.add(self.juego_frame, text="🎯 Jugar Bingo")
        
        # Tab 2: Tienda de Cartones (NUEVO)
        from comprar_carton_frame import ComprarCartonFrame
        self.tienda_frame = ComprarCartonFrame(self.notebook, self.usuario_datos)
        self.notebook.add(self.tienda_frame, text="🛒 Tienda")
        
        # Tab 3: Mis Cartones - PASAR REFERENCIA AL DASHBOARD
        self.cartones_frame = CartonesFrame(self.notebook, self.usuario_datos)
        self.cartones_frame.dashboard = self  # ← AGREGAR ESTA LÍNEA
        self.notebook.add(self.cartones_frame, text="🎫 Mis Cartones")
        
        # Tab 4: Historial
        self.historial_frame = HistorialFrame(self.notebook, self.usuario_datos)
        self.notebook.add(self.historial_frame, text="📊 Historial")
        
        # Tab 5: Estadísticas
        self.estadisticas_frame = EstadisticasFrame(self.notebook, self.usuario_datos)
        self.notebook.add(self.estadisticas_frame, text="📈 Estadísticas")

    def _cargar_saldo_inicial(self):
        """Cargar saldo inicial del usuario"""
        self.actualizar_saldo()

    def _iniciar_actualizacion_automatica(self):
        """Iniciar actualización automática del saldo cada 5 segundos"""
        self._actualizar_saldo_automatico()

    def _actualizar_saldo_automatico(self):
        """Actualizar saldo automáticamente y programar próxima actualización"""
        try:
            saldo_anterior = self.saldo_actual
            self.actualizar_saldo()
            
            # Si el saldo cambió, actualizar otras pestañas también
            if saldo_anterior != self.saldo_actual:
                self._notificar_cambio_saldo()
                
        except Exception as e:
            print(f"Error en actualización automática: {e}")
        
        # Programar próxima actualización en 5 segundos
        self.actualizacion_saldo_id = self.after(5000, self._actualizar_saldo_automatico)

    def _notificar_cambio_saldo(self):
        """Notificar cambio de saldo a otras pestañas"""
        try:
            # Actualizar pestaña de cartones si está visible
            if hasattr(self, 'cartones_frame'):
                tab_actual = self.notebook.select()
                tab_text = self.notebook.tab(tab_actual, "text")
                if "Cartones" in tab_text or "Tienda" in tab_text:
                    # Solo actualizar si está en pestañas relevantes
                    pass
        except:
            pass

    def _detener_actualizacion_automatica(self):
        """Detener la actualización automática"""
        if self.actualizacion_saldo_id:
            self.after_cancel(self.actualizacion_saldo_id)
            self.actualizacion_saldo_id = None

    def _on_tab_changed(self, event):
        """Evento cuando se cambia de pestaña"""
        selection = event.widget.select()
        tab_text = event.widget.tab(selection, "text")
        
        # Actualizar contenido según la pestaña seleccionada
        if "Tienda" in tab_text:
            # Regenerar muestras en la tienda
            if hasattr(self, 'tienda_frame'):
                try:
                    self.tienda_frame._generar_cartones_muestra()
                except:
                    pass
        elif "Cartones" in tab_text:
            self.cartones_frame.actualizar_cartones()
        elif "Historial" in tab_text:
            self.historial_frame.actualizar_historial()
        elif "Estadísticas" in tab_text:
            self.estadisticas_frame.actualizar_estadisticas()

    def actualizar_saldo(self):
        """Actualizar saldo mostrado en el header"""
        try:
            cliente_db = Cliente()
            self.saldo_actual = cliente_db.obtener_saldo(self.usuario_datos.get('dni'))
            cliente_db.cerrar()
            
            # Validar que saldo no sea None
            if self.saldo_actual is None:
                self.saldo_actual = 0
            
            # Actualizar label con formato de moneda
            self.saldo_label.configure(text=f"${self.saldo_actual:,}")
            
            # Cambiar color según saldo
            if self.saldo_actual >= 5000:
                color = "#2ecc71"  # Verde
            elif self.saldo_actual >= 1000:
                color = "#f39c12"  # Naranja
            else:
                color = "#e74c3c"  # Rojo
            
            self.saldo_label.configure(fg=color)
            
        except Exception as e:
            print(f"Error al actualizar saldo: {str(e)}")
            # En caso de error, mostrar 0
            self.saldo_actual = 0
            self.saldo_label.configure(text="$0", fg="#e74c3c")

    def seleccionar_carton_guardado(self, carton):
        """Método para seleccionar cartón desde la pestaña de cartones"""
        # Cambiar a la pestaña de juego
        self.notebook.select(0)  # Índice 0 = primera pestaña (Jugar Bingo)
        
        # Pasar el cartón al frame de juego
        self.juego_frame.seleccionar_carton_guardado(carton)

    def mostrar_estadisticas_post_partida(self, resultado_partida):
        """Mostrar estadísticas después de terminar una partida"""
        # Actualizar todos los frames
        self.actualizar_saldo()
        self.cartones_frame.actualizar_cartones()
        self.historial_frame.actualizar_historial()
        
        # Mostrar modal de estadísticas
        self.estadisticas_frame.mostrar_estadisticas_post_partida(resultado_partida)

    def _mostrar_perfil(self):
        """Mostrar información del perfil en ventana modal"""
        ventana = tk.Toplevel(self)
        ventana.title("👤 Mi Perfil")
        ventana.geometry("500x600")
        ventana.resizable(False, False)
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
        # Header
        header_frame = tk.Frame(ventana, bg="#2c3e50", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text="👤 Información del Perfil",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#2c3e50").pack(expand=True)
        
        # Contenido
        content_frame = tk.Frame(ventana, bg="#ffffff", relief="solid", bd=1)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información personal
        self._crear_seccion_perfil(content_frame, "📋 Información Personal", [
            ("Nombre Completo", f"{self.usuario_datos.get('nombre', 'N/A')} {self.usuario_datos.get('apellido', '')}"),
            ("DNI", self.usuario_datos.get('dni', 'N/A')),
            ("Email", self.usuario_datos.get('mail', 'N/A')),
            ("Teléfono", self.usuario_datos.get('telefono', 'N/A')),
            ("Fecha de Nacimiento", str(self.usuario_datos.get('fecha_nac', 'N/A'))),
            ("Fecha de Registro", str(self.usuario_datos.get('fecha_reg', 'N/A')))
        ])
        
        # Información de cuenta
        self._crear_seccion_perfil(content_frame, "💰 Información de Cuenta", [
            ("Saldo Actual", f"${self.saldo_actual:,}"),
            ("Última Sesión", datetime.now().strftime('%d/%m/%Y %H:%M')),
            ("Estado de Cuenta", "Activa" if self.saldo_actual >= 0 else "Saldo Bajo")
        ])
        
        # Botones
        button_frame = tk.Frame(content_frame, bg="#ffffff")
        button_frame.pack(fill="x", pady=(30, 20))
        
        ttk.Button(button_frame,
                  text="📊 Ver Estadísticas",
                  command=lambda: [ventana.destroy(), self.notebook.select(3)],
                  style='Primary.TButton').pack(side="left", padx=(0, 10))
        
        ttk.Button(button_frame,
                  text="Cerrar",
                  command=ventana.destroy,
                  style='Secondary.TButton').pack(side="left")

    def _crear_seccion_perfil(self, parent, titulo, datos):
        """Crear sección de información en el perfil"""
        # Frame de la sección
        seccion_frame = tk.Frame(parent, bg="#ffffff")
        seccion_frame.pack(fill="x", pady=10)
        
        # Título de la sección
        tk.Label(seccion_frame,
                text=titulo,
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(anchor="w", pady=(0, 10))
        
        # Datos de la sección
        for label, valor in datos:
            row_frame = tk.Frame(seccion_frame, bg="#f8f9fa", relief="solid", bd=1)
            row_frame.pack(fill="x", pady=2)
            
            tk.Label(row_frame,
                    text=label + ":",
                    font=("Arial", 10, "bold"),
                    fg="#495057",
                    bg="#f8f9fa",
                    width=20,
                    anchor="w").pack(side="left", padx=(10, 0), pady=5)
            
            tk.Label(row_frame,
                    text=str(valor),
                    font=("Arial", 10),
                    fg="#6c757d",
                    bg="#f8f9fa",
                    anchor="w").pack(side="left", padx=(10, 0), pady=5)

    def _cerrar_sesion(self):
        """Cerrar sesión y volver al login"""
        respuesta = messagebox.askyesno("🚪 Cerrar Sesión", 
                                       "¿Estás seguro que deseas cerrar sesión?\n"
                                       "Se perderá cualquier partida en curso.")
        if respuesta:
            # Detener actualización automática
            self._detener_actualizacion_automatica()
            
            # Limpiar datos de sesión
            self.usuario_datos = {}
            self.saldo_actual = 0
            
            # Volver al login
            self.master.mostrar_login()

    def get_font(self, tipo):
        """Obtener fuentes para compatibilidad"""
        return self.master.get_font(tipo)

    def mostrar_notificacion(self, titulo, mensaje, tipo="info"):
        """Mostrar notificación al usuario"""
        if tipo == "success":
            messagebox.showinfo(titulo, mensaje)
        elif tipo == "warning":
            messagebox.showwarning(titulo, mensaje)
        elif tipo == "error":
            messagebox.showerror(titulo, mensaje)
        else:
            messagebox.showinfo(titulo, mensaje)

    def ir_a_tab(self, indice):
        """Navegar a una pestaña específica"""
        try:
            self.notebook.select(indice)
        except:
            pass  # Ignorar errores de índice inválido

    def ir_a_tienda(self):
        """Ir a la tienda de cartones"""
        self.ir_a_tab(1)

    def ir_a_juego(self):
        """Ir a la pestaña de juego"""
        self.ir_a_tab(0)

    def ir_a_cartones(self):
        """Ir a mis cartones"""
        self.ir_a_tab(2)

    def ir_a_historial(self):
        """Ir al historial"""
        self.ir_a_tab(3)

    def ir_a_estadisticas(self):
        """Ir a estadísticas"""
        self.ir_a_tab(4)

    def recargar_dashboard(self):
        """Recargar todos los datos del dashboard"""
        self.actualizar_saldo()
        
        # Actualizar frames según la pestaña actual
        tab_actual = self.notebook.select()
        tab_text = self.notebook.tab(tab_actual, "text")
        
        if "Cartones" in tab_text:
            self.cartones_frame.actualizar_cartones()
        elif "Historial" in tab_text:
            self.historial_frame.actualizar_historial()
        elif "Estadísticas" in tab_text:
            self.estadisticas_frame.actualizar_estadisticas()

    def obtener_usuario_datos(self):
        """Obtener datos del usuario actual"""
        return self.usuario_datos.copy()

    def es_usuario_valido(self):
        """Verificar si hay un usuario válido logueado"""
        return bool(self.usuario_datos.get('dni'))