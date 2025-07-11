import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime
from backend import generar_cartones, Cliente, Carton

class ComprarCartonFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.usuario_datos = usuario_datos or {}
        
        # Generar cartones de muestra (sin guardar en DB)
        self.cartones_muestra = []
        self.carton_seleccionado = None
        
        self._crear_interfaz()
        self._generar_cartones_muestra()

    def _crear_interfaz(self):
        # Header
        header_frame = tk.Frame(self, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(header_frame,
                text="🛒 Tienda de Cartones",
                font=("Arial", 18, "bold"),
                fg="#2c3e50",
                bg="#f0f0f0").pack(side="left")
        
        # Botón actualizar muestras
        ttk.Button(header_frame,
                  text="🔄 Nuevos Cartones",
                  command=self._generar_cartones_muestra,
                  style='Secondary.TButton').pack(side="right", padx=(0, 10))
        
        # Botón volver
        ttk.Button(header_frame,
                  text="← Volver",
                  command=self._volver,
                  style='Secondary.TButton').pack(side="right")
        
        # Información
        info_frame = tk.Frame(self, bg="#fff3cd", relief="solid", bd=1)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame,
                text="💡 Selecciona el cartón que más te guste. Cada compra incluye 6 cartones de la misma serie.",
                font=("Arial", 11),
                fg="#856404",
                bg="#fff3cd").pack(pady=10)
        
        # Precio
        precio_frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=1)
        precio_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(precio_frame,
                text="💰 Precio por cartón (6 unidades): $1,000",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=10)
        
        # Container para cartones
        self._crear_container_cartones()
        
        # Botón de compra
        self._crear_boton_compra()

    def _crear_container_cartones(self):
        """Crear container scrolleable para mostrar cartones"""
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

    def _crear_boton_compra(self):
        """Crear botón de compra"""
        compra_frame = tk.Frame(self, bg="#f0f0f0")
        compra_frame.pack(fill="x", padx=20, pady=20)
        
        self.btn_comprar = ttk.Button(compra_frame,
                                     text="🛒 Comprar Cartón Seleccionado",
                                     command=self._comprar_carton,
                                     style='Primary.TButton',
                                     state="disabled")
        self.btn_comprar.pack()

    def _generar_cartones_muestra(self):
        """Generar cartones de muestra para elegir"""
        try:
            # Limpiar container
            for widget in self.cartones_container.winfo_children():
                widget.destroy()
            
            # Generar cartones agrupados por color (3 por fila, 2 filas)
            self.cartones_muestra = []
            colores_disponibles = ['rojo', 'azul', 'verde', 'amarillo', 'morado', 'naranja']
            
            for fila in range(2):  # 2 filas
                fila_frame = tk.Frame(self.cartones_container, bg="#f0f0f0")
                fila_frame.pack(fill="x", pady=10)
                
                for col in range(3):  # 3 columnas por fila
                    color_index = fila * 3 + col
                    if color_index < len(colores_disponibles):
                        hoja = generar_cartones()  # 6 cartones por hoja
                        color = colores_disponibles[color_index]
                        
                        carton_muestra = {
                            'id': f'muestra_{color_index}',
                            'disposicion': hoja,
                            'color': color,
                            'precio': 1000
                        }
                        self.cartones_muestra.append(carton_muestra)
                        
                        # Crear widget visual en grid
                        self._crear_carton_muestra_widget_grid(carton_muestra, fila_frame)
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al generar muestras: {str(e)}")

    def _crear_carton_muestra_widget_grid(self, carton, parent_row):
        """Crear widget visual para un cartón de muestra en grid"""
        # Frame del cartón (1/3 del ancho)
        carton_frame = tk.Frame(parent_row, bg="#ffffff", relief="solid", bd=2)
        carton_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Header con color y selección
        header_frame = tk.Frame(carton_frame, bg=self._get_color_hex(carton['color']))
        header_frame.pack(fill="x")
        
        tk.Label(header_frame,
                text=f"🎫 {carton['color'].title()}",
                font=("Arial", 11, "bold"),
                fg="white",
                bg=self._get_color_hex(carton['color'])).pack(pady=8)
        
        # Preview del primer cartón (primeras 3 filas) - más compacto
        preview_frame = tk.Frame(carton_frame, bg="#ffffff")
        preview_frame.pack(padx=10, pady=10)
        
        # Grid del cartón con color - más pequeño
        grid_frame = tk.Frame(preview_frame, bg=self._get_color_light(carton['color']), relief="solid", bd=1)
        grid_frame.pack()
        
        # Mostrar primeras 3 filas (primer cartón) - números más pequeños
        disposicion = carton['disposicion']
        for i in range(3):
            if i < len(disposicion):
                fila_frame = tk.Frame(grid_frame, bg=self._get_color_light(carton['color']))
                fila_frame.pack()
                
                for num in disposicion[i]:
                    tk.Label(fila_frame,
                            text=str(num) if num else "  ",
                            font=("Courier", 8, "bold"),
                            fg="#2c3e50",
                            bg="white" if num else self._get_color_light(carton['color']),
                            relief="solid",
                            bd=1,
                            width=3,
                            height=1).pack(side="left", padx=1, pady=1)
        
        # Botón seleccionar
        btn_frame = tk.Frame(carton_frame, bg="#ffffff")
        btn_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        btn_seleccionar = ttk.Button(btn_frame,
                                   text="✓ Seleccionar",
                                   command=lambda c=carton: self._seleccionar_carton(c),
                                   style='Secondary.TButton')
        btn_seleccionar.pack(fill="x")
        
        # Guardar referencia del botón para poder modificarlo después
        carton['boton'] = btn_seleccionar

    def _seleccionar_carton(self, carton):
        """Seleccionar un cartón específico"""
        self.carton_seleccionado = carton
        
        # Actualizar todos los botones de cartones
        for carton_item in self.cartones_muestra:
            if 'boton' in carton_item:
                if carton_item == carton:
                    carton_item['boton'].configure(text="● Seleccionado")
                else:
                    carton_item['boton'].configure(text="○ Seleccionar")
        
        # Habilitar botón de compra y cambiar a estilo activo
        self.btn_comprar.configure(state="normal", style='Active.TButton')
        
        messagebox.showinfo("✅ Cartón Seleccionado", 
                          f"Has seleccionado el cartón {carton['color'].title()}")

    def _comprar_carton(self):
        """Comprar el cartón seleccionado"""
        if not self.carton_seleccionado:
            messagebox.showwarning("⚠️ Advertencia", "Primero selecciona un cartón")
            return
        
        try:
            # Verificar saldo
            cliente_db = Cliente()
            saldo_actual = cliente_db.obtener_saldo(self.usuario_datos.get('dni'))
            
            if saldo_actual < 1000:
                messagebox.showerror("❌ Saldo Insuficiente", 
                                   f"Necesitas $1000 para comprar un cartón.\n"
                                   f"Saldo actual: ${saldo_actual}")
                cliente_db.cerrar()
                return
            
            # Confirmar compra
            respuesta = messagebox.askyesno("🛒 Confirmar Compra",
                                          f"¿Confirmas la compra del cartón {self.carton_seleccionado['color'].title()}?\n\n"
                                          f"Precio: $1,000\n"
                                          f"Incluye: 6 cartones de la serie")
            
            if not respuesta:
                return
            
            # Crear cartón en la base de datos
            carton_db = Carton()
            disposicion_json = json.dumps(self.carton_seleccionado['disposicion'])
            
            carton_id = carton_db.insertar_carton(
                disposicion_json, 
                1000, 
                self.carton_seleccionado['color'], 
                False, 
                self.usuario_datos.get('dni')
            )
            
            # Debitar saldo
            cliente_db.debitar_saldo(self.usuario_datos.get('dni'), 1000)
            
            carton_db.cerrar()
            cliente_db.cerrar()
            
            messagebox.showinfo("✅ Compra Exitosa", 
                              f"¡Cartón {self.carton_seleccionado['color'].title()} comprado!\n"
                              f"ID: #{carton_id}\n\n"
                              f"Ve a 'Mis Cartones' para verlo.")
            
            # Actualizar saldo en dashboard
            if hasattr(self.master, 'actualizar_saldo'):
                self.master.actualizar_saldo()
            
            # Volver al dashboard
            self._volver()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al comprar cartón: {str(e)}")

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

    def _volver(self):
        """Volver al dashboard"""
        if hasattr(self.master, 'ir_a_tab'):
            self.master.ir_a_tab(0)  # Ir a pestaña de juego
        elif hasattr(self.master, 'mostrar_dashboard'):
            self.master.mostrar_dashboard(self.usuario_datos)