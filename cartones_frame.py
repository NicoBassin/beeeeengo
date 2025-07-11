import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
from backend import Carton, Cliente

class CartonesFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.usuario_datos = usuario_datos or {}
        
        self._crear_interfaz()
        self._cargar_cartones()

    def _crear_interfaz(self):
        # Título y controles superiores
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame,
                text="🎫 Mis Cartones Guardados",
                font=("Arial", 18, "bold"),
                fg="#2c3e50",
                bg="#f0f0f0").pack(side="left")
        
        # Frame principal con scroll
        self._crear_lista_cartones()
        
        # Información adicional
        info_frame = tk.Frame(self, bg="#f0f0f0")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame,
                text="💡 Los cartones generados se guardan automáticamente. Puedes usar cualquiera para jugar.",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#f0f0f0").pack()

    def _crear_lista_cartones(self):
        # Frame contenedor con scroll
        container_frame = tk.Frame(self, bg="#f0f0f0")
        container_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas y scrollbar
        canvas = tk.Canvas(container_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        self.cartones_container = tk.Frame(canvas, bg="#f0f0f0")
        
        self.cartones_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.cartones_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _cargar_cartones(self):
        """Cargar cartones desde la base de datos"""
        try:
            carton_db = Carton()
            cartones = carton_db.obtener_cartones_cliente(self.usuario_datos.get('dni'))
            carton_db.cerrar()
            
            # Limpiar container
            for widget in self.cartones_container.winfo_children():
                widget.destroy()
            
            if not cartones:
                self._mostrar_sin_cartones()
                return
            
            # Mostrar cartones
            for i, carton in enumerate(cartones):
                self._crear_carton_widget(carton, i)
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al cargar cartones: {str(e)}")

    def _mostrar_sin_cartones(self):
        """Mostrar mensaje cuando no hay cartones"""
        empty_frame = tk.Frame(self.cartones_container, bg="#ffffff", relief="solid", bd=1)
        empty_frame.pack(fill="x", pady=10)
        
        content_frame = tk.Frame(empty_frame, bg="#ffffff")
        content_frame.pack(pady=50, padx=50)
        
        tk.Label(content_frame,
                text="🎫",
                font=("Arial", 48),
                bg="#ffffff").pack()
        
        tk.Label(content_frame,
                text="No tienes cartones guardados",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack()
        
        tk.Label(content_frame,
                text="¡Genera tu primer cartón para comenzar a jugar!",
                font=("Arial", 11),
                fg="#7f8c8d",
                bg="#ffffff").pack(pady=(5, 0))

    def _crear_carton_widget(self, carton, index):
        """Crear widget para mostrar un cartón"""
        # Frame principal del cartón
        carton_frame = tk.Frame(self.cartones_container, bg="#ffffff", relief="solid", bd=1)
        carton_frame.pack(fill="x", pady=5)
        
        # Header del cartón
        header_frame = tk.Frame(carton_frame, bg="#ffffff")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # Info del cartón (izquierda)
        info_left = tk.Frame(header_frame, bg="#ffffff")
        info_left.pack(side="left", fill="y")
        
        tk.Label(info_left,
                text=f"Cartón #{carton['id']}",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(anchor="w")
        
        fecha_creacion = carton['fecha_creacion'].strftime("%d/%m/%Y %H:%M")
        tk.Label(info_left,
                text=f"Creado: {fecha_creacion}",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack(anchor="w")
        
        # Estado y color (centro)
        estado_frame = tk.Frame(header_frame, bg="#ffffff")
        estado_frame.pack(side="left", padx=(20, 0))
        
        color_display = tk.Label(estado_frame,
                                text="●",
                                font=("Arial", 16),
                                fg=self._get_color_hex(carton['color']),
                                bg="#ffffff")
        color_display.pack()
        
        tk.Label(estado_frame,
                text=carton['color'].title(),
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack()
        
        # Botones (derecha)
        buttons_frame = tk.Frame(header_frame, bg="#ffffff")
        buttons_frame.pack(side="right")
        
        ttk.Button(buttons_frame,
                  text="👁️ Ver",
                  command=lambda c=carton: self._ver_carton(c),
                  style='Secondary.TButton').pack(side="right", padx=(5, 0))
        
        ttk.Button(buttons_frame,
                  text="🎮 Usar",
                  command=lambda c=carton: self._usar_carton(c),
                  style='Primary.TButton').pack(side="right")
        
        # Preview del cartón (compacto)
        self._crear_preview_carton(carton_frame, carton)

    def _crear_preview_carton(self, parent, carton):
        """Crear preview compacto del cartón"""
        # OBTENER EL COLOR DEL CARTÓN
        color_carton = carton.get('color', 'azul')
        color_fondo = self._get_color_light(color_carton)
        
        preview_frame = tk.Frame(parent, bg=color_fondo, relief="solid", bd=1)
        preview_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        try:
            disposicion = json.loads(carton['disposicion'])
            
            # Mostrar solo los primeros 3 cartones (9 filas)
            filas_a_mostrar = disposicion[:9]  # Primeros 3 cartones
            
            for i, fila in enumerate(filas_a_mostrar):
                if i % 3 == 0:  # Nueva línea cada 3 filas (nuevo cartón)
                    if i > 0:
                        # Separador entre cartones
                        tk.Frame(preview_frame, height=1, bg="#dee2e6").pack(fill="x", pady=2)
                
                fila_frame = tk.Frame(preview_frame, bg=color_fondo)
                fila_frame.pack()
                
                for num in fila:
                    tk.Label(fila_frame,
                            text=str(num) if num else "  ",
                            font=("Courier", 8),
                            fg="#495057",
                            bg="#ffffff" if num else color_fondo,
                            width=3).pack(side="left", padx=1)
                            
        except Exception as e:
            tk.Label(preview_frame,
                    text="Error al mostrar cartón",
                    font=("Arial", 10),
                    fg="#dc3545",
                    bg=color_fondo).pack(pady=10)

    def _get_color_hex(self, color):
        """Convertir nombre de color a hexadecimal"""
        colors = {
            'rojo': '#e74c3c',
            'azul': '#3498db',
            'verde': '#2ecc71',
            'amarillo': '#f1c40f',
            'morado': '#9b59b6',
            'naranja': '#e67e22'
        }
        return colors.get(color.lower(), '#95a5a6')
    
    def _get_color_light(self, color):
        """Obtener versión clara del color"""
        colors = {
            'rojo': '#fadbd8',
            'azul': '#d6eaf8', 
            'verde': '#d5f4e6',
            'amarillo': '#fcf3cf',
            'morado': '#e8daef',
            'naranja': '#fdebd0'
        }
        return colors.get(color.lower(), '#f8f9fa')

    def _ver_carton(self, carton):
        """Mostrar cartón completo en ventana modal"""
        self._mostrar_carton_completo(carton)

    def _usar_carton(self, carton):
        """Usar cartón para jugar"""
        respuesta = messagebox.askyesno(
            "🎮 Usar Cartón",
            f"¿Deseas usar el Cartón #{carton['id']} para jugar?\n\n"
            f"Color: {carton['color'].title()}\n"
            f"Valor: ${carton['valor']}"
        )
        
        if respuesta:
            # CAMBIO: Usar la referencia directa al dashboard
            if hasattr(self, 'dashboard') and self.dashboard:
                self.dashboard.seleccionar_carton_guardado(carton)
            else:
                print("DEBUG: No se encontró referencia al dashboard")
                
            messagebox.showinfo("✅ Cartón Seleccionado", 
                            f"Cartón #{carton['id']} listo para jugar.\n"
                            "Ve a la pestaña 'Jugar Bingo' para comenzar.")

    def _mostrar_carton_completo(self, carton):
        """Mostrar cartón completo en ventana modal"""
        ventana = tk.Toplevel(self)
        ventana.title(f"Cartón #{carton['id']}")
        ventana.geometry("800x600")
        ventana.resizable(False, False)
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
        # Header
        header_frame = tk.Frame(ventana, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text=f"🎫 Cartón #{carton['id']} - {carton['color'].title()}",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#2c3e50").pack(expand=True)
        
        # Contenido
        content_frame = tk.Frame(ventana, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        try:
            disposicion = json.loads(carton['disposicion'])
            self._crear_carton_visual_completo(content_frame, disposicion)
            
        except Exception as e:
            tk.Label(content_frame,
                    text=f"Error al mostrar cartón: {str(e)}",
                    font=("Arial", 12),
                    fg="#e74c3c",
                    bg="#f0f0f0").pack(expand=True)
        
        # Botón cerrar
        ttk.Button(content_frame,
                  text="Cerrar",
                  command=ventana.destroy,
                  style='Secondary.TButton').pack(pady=(20, 0))

    def _crear_carton_visual_completo(self, parent, disposicion):
        """Crear visualización completa del cartón con 6 cartones"""
        # Frame scrolleable
        canvas = tk.Canvas(parent, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar 6 cartones (3 filas cada uno)
        for carton_num in range(6):
            carton_frame = tk.Frame(scrollable_frame, bg="#ffffff", relief="solid", bd=2)
            carton_frame.pack(pady=10, padx=10, fill="x")
            
            # Título del cartón
            tk.Label(carton_frame,
                    text=f"Cartón {carton_num + 1}",
                    font=("Arial", 12, "bold"),
                    fg="#2c3e50",
                    bg="#ffffff").pack(pady=(10, 5))
            
            # Grid del cartón
            grid_frame = tk.Frame(carton_frame, bg="#ffffff")
            grid_frame.pack(pady=(0, 10))
            
            # 3 filas por cartón
            inicio_fila = carton_num * 3
            fin_fila = inicio_fila + 3
            
            for i in range(inicio_fila, fin_fila):
                if i < len(disposicion):
                    fila_frame = tk.Frame(grid_frame, bg="#ffffff")
                    fila_frame.pack()
                    
                    for num in disposicion[i]:
                        tk.Label(fila_frame,
                                text=str(num) if num else "  ",
                                font=("Courier", 11, "bold"),
                                fg="#2c3e50",
                                bg="#ecf0f1" if num else "#ffffff",
                                relief="solid",
                                bd=1,
                                width=4,
                                height=2).pack(side="left", padx=1, pady=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def actualizar_cartones(self):
        """Método público para actualizar la lista de cartones"""
        self._cargar_cartones()
