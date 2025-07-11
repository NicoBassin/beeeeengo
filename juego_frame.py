import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime
from backend import Carton, Cliente, Apuesta, Partida

class JuegoFrame(tk.Frame):
    def __init__(self, master, usuario_datos=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.usuario_datos = usuario_datos or {}
        
        # Estado del juego
        self.carton_actual = None
        self.carton_data = None
        self.carton_seleccionado = None
        self.en_partida = False
        self.numeros_cantados = []
        self.numeros_marcados = set()
        self.apuesta_id = None
        self.partida_id = None
        
        self._crear_interfaz()

    def _crear_interfaz(self):
        # Frame principal del juego
        game_frame = tk.Frame(self, bg="#ffffff", relief="solid", bd=1)
        game_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título de la sección
        title_frame = tk.Frame(game_frame, bg="#ffffff")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        tk.Label(title_frame,
                text="🎯 Sala de Bingo Argentino",
                font=("Arial", 18, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(side="left")
        
        # Estado del juego
        self.game_status = tk.Label(title_frame,
                                   text="🟢 Listo para jugar",
                                   font=("Arial", 12),
                                   fg="#27ae60",
                                   bg="#ffffff")
        self.game_status.pack(side="right")
        
        # Contenido dividido en dos columnas
        content_frame = tk.Frame(game_frame, bg="#ffffff")
        content_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Columna izquierda: Cartón
        left_column = tk.Frame(content_frame, bg="#ffffff")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self._crear_carton_display(left_column)
        
        # Columna derecha: Controles y números
        right_column = tk.Frame(content_frame, bg="#ffffff")
        right_column.pack(side="right", fill="y", padx=(20, 0))
        
        self._crear_controles_juego(right_column)

    def _crear_carton_display(self, parent):
        carton_frame = tk.Frame(parent, bg="#ffffff")
        carton_frame.pack(fill="both", expand=True)
        
        # Título del cartón
        tk.Label(carton_frame,
                text="Tu Cartón de Bingo Argentino",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 15))
        
        # Frame del cartón - MÁS GRANDE
        self.carton_container = tk.Frame(carton_frame, bg="#ecf0f1", relief="solid", bd=2, width=800, height=500)
        self.carton_container.pack(pady=10, fill="both", expand=True)
        self.carton_container.pack_propagate(False)  # Mantener tamaño fijo
        
        # Crear cartón vacío inicialmente
        self._crear_carton_vacio()

    def _crear_carton_vacio(self):
        # Limpiar container
        for widget in self.carton_container.winfo_children():
            widget.destroy()
        
        # Mensaje de cartón vacío
        empty_frame = tk.Frame(self.carton_container, bg="#ecf0f1")
        empty_frame.pack(padx=50, pady=50)
        
        tk.Label(empty_frame,
                text="🎫",
                font=("Arial", 48),
                bg="#ecf0f1").pack()
        
        tk.Label(empty_frame,
                text="Selecciona o genera un cartón para comenzar",
                font=("Arial", 12),
                fg="#7f8c8d",
                bg="#ecf0f1").pack()

    def _crear_carton_bingo_argentino(self, cartones_data, color='azul'):
        """Crear visualización de 6 cartones de bingo argentino (3x9) con color en layout 3 columnas"""
        # Limpiar container
        for widget in self.carton_container.winfo_children():
            widget.destroy()
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.carton_container, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame para los 6 cartones (3 columnas x 2 filas)
        cartones_grid = tk.Frame(scrollable_frame, bg="#f0f0f0")
        cartones_grid.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Configurar columnas para que se expandan uniformemente
        for col in range(3):
            cartones_grid.grid_columnconfigure(col, weight=1)
        
        self.carton_buttons = {}
        color_hex = self._get_color_hex(color)
        color_light = self._get_color_light(color)
        
        print(f"DEBUG: Creando cartón con color: {color}, hex: {color_hex}")  # Debug
        
        # Mostrar 6 cartones en layout 3x2 (3 columnas, 2 filas)
        for carton_num in range(6):
            # Posición en el grid (3 columnas)
            row = carton_num // 3  # 0 para los primeros 3, 1 para los siguientes 3
            col = carton_num % 3   # 0, 1, 2 para cada fila
            
            # Frame del cartón individual - MÁS GRANDE
            carton_frame = tk.Frame(cartones_grid, bg=color_hex, relief="solid", bd=3)
            carton_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Header del cartón
            header_frame = tk.Frame(carton_frame, bg=color_hex)
            header_frame.pack(fill="x")
            
            tk.Label(header_frame,
                    text=f"Cartón {carton_num + 1}",
                    font=("Arial", 11, "bold"),
                    fg="white",
                    bg=color_hex).pack(pady=6)
            
            # Grid del cartón (3x9) - MÁS GRANDE
            grid_frame = tk.Frame(carton_frame, bg=color_light)
            grid_frame.pack(padx=6, pady=6)
            
            # 3 filas por cartón
            inicio_fila = carton_num * 3
            fin_fila = inicio_fila + 3
            
            for i in range(inicio_fila, fin_fila):
                if i < len(cartones_data):
                    fila_frame = tk.Frame(grid_frame, bg=color_light)
                    fila_frame.pack()
                    
                    for num in cartones_data[i]:
                        if num is not None:
                            btn = tk.Button(fila_frame,
                                           text=str(num),
                                           font=("Arial", 9, "bold"),
                                           bg="white",
                                           fg="#2c3e50",
                                           width=4,
                                           height=2,
                                           relief="solid",
                                           bd=1,
                                           command=lambda n=num: self._marcar_numero(n))
                            
                            self.carton_buttons[num] = btn
                        else:
                            # Celda vacía
                            btn = tk.Button(fila_frame,
                                           text=" ",
                                           font=("Arial", 9),
                                           bg=color_light,
                                           fg="#7f8c8d",
                                           width=4,
                                           height=2,
                                           relief="flat",
                                           state="disabled")
                        
                        btn.pack(side="left", padx=1, pady=1)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _crear_controles_juego(self, parent):
        controls_frame = tk.Frame(parent, bg="#ffffff")
        controls_frame.pack(fill="both", expand=True)
        
        # Botones principales
        tk.Label(controls_frame,
                text="Controles de Juego",
                font=("Arial", 14, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 15))
        
        # ELIMINADO: Botón generar cartón
        # Los usuarios ahora deben ir a la tienda
        
        self.btn_usar_guardado = ttk.Button(controls_frame,
                                           text="📂 Usar Cartón Guardado",
                                           command=self._seleccionar_carton_guardado,
                                           style='Secondary.TButton')
        self.btn_usar_guardado.pack(fill="x", pady=(0, 10))
        
        # Mensaje informativo
        info_label = tk.Label(controls_frame,
                             text="💡 Ve a la Tienda para comprar cartones nuevos",
                             font=("Arial", 10),
                             fg="#7f8c8d",
                             bg="#ffffff")
        info_label.pack(pady=(0, 10))
        
        self.btn_nueva_partida = ttk.Button(controls_frame,
                                           text="🎮 Nueva Partida",
                                           command=self._nueva_partida,
                                           style='Primary.TButton',
                                           state="disabled")
        self.btn_nueva_partida.pack(fill="x", pady=(0, 10))
        
        self.btn_cantar_numero = ttk.Button(controls_frame,
                                           text="🔢 Cantar Número",
                                           command=self._cantar_numero,
                                           style='Secondary.TButton',
                                           state="disabled")
        self.btn_cantar_numero.pack(fill="x", pady=(0, 20))
        
        # Números cantados con grid fijo
        tk.Label(controls_frame,
                text="Números Cantados",
                font=("Arial", 12, "bold"),
                fg="#2c3e50",
                bg="#ffffff").pack(pady=(0, 10))
        
        # Frame para números cantados (grid fijo) - más ancho
        numeros_container = tk.Frame(controls_frame, bg="#ecf0f1", relief="solid", bd=1, height=220, width=400)
        numeros_container.pack(fill="x", pady=(0, 20))
        numeros_container.pack_propagate(False)
        
        # Grid de números del 1 al 90
        self.numeros_grid_frame = tk.Frame(numeros_container, bg="#ecf0f1")
        self.numeros_grid_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Crear grid de 9x10 para números 1-90 (mejor distribución)
        self.numeros_labels = {}
        for i in range(1, 91):
            row = (i - 1) // 10
            col = (i - 1) % 10
            
            label = tk.Label(self.numeros_grid_frame,
                           text=str(i),
                           font=("Arial", 9, "bold"),
                           fg="#7f8c8d",
                           bg="#ffffff",
                           relief="solid",
                           bd=1,
                           width=4,
                           height=1)
            label.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")
            self.numeros_labels[i] = label
        
        # Configurar el peso de las columnas para que se expandan
        for col in range(10):
            self.numeros_grid_frame.grid_columnconfigure(col, weight=1)
        
        # Último número cantado
        self.ultimo_numero_frame = tk.Frame(controls_frame, bg="#e74c3c", relief="solid", bd=2)
        self.ultimo_numero_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(self.ultimo_numero_frame,
                text="Último Número",
                font=("Arial", 10),
                fg="white",
                bg="#e74c3c").pack(pady=(5, 0))
        
        self.ultimo_numero_label = tk.Label(self.ultimo_numero_frame,
                                           text="--",
                                           font=("Arial", 20, "bold"),
                                           fg="white",
                                           bg="#e74c3c")
        self.ultimo_numero_label.pack(pady=(0, 5))
        
        # Botón BINGO
        self.btn_bingo = ttk.Button(controls_frame,
                                   text="🏆 ¡BINGO!",
                                   command=self._verificar_bingo,
                                   style='Primary.TButton',
                                   state="disabled")
        self.btn_bingo.pack(fill="x", pady=(10, 0))

    def _generar_carton(self):
        """Generar un nuevo cartón de bingo argentino"""
        try:
            # Verificar saldo
            cliente_db = Cliente()
            saldo_actual = cliente_db.obtener_saldo(self.usuario_datos.get('dni'))
            
            if saldo_actual < 1000:
                messagebox.showerror("❌ Saldo Insuficiente", 
                                   f"Necesitas $1000 para generar un cartón.\n"
                                   f"Saldo actual: ${saldo_actual}")
                cliente_db.cerrar()
                return
            
            # Generar cartón
            carton_db = Carton()
            carton_id, hoja = carton_db.generar_carton(self.usuario_datos.get('dni'))
            
            # Debitar saldo
            cliente_db.debitar_saldo(self.usuario_datos.get('dni'), 1000)
            
            # Guardar datos del cartón
            self.carton_actual = carton_id
            self.carton_data = hoja
            
            # Crear visualización del cartón
            self._crear_carton_bingo_argentino(hoja)
            
            # Habilitar botón de nueva partida
            self.btn_nueva_partida.configure(state="normal")
            
            carton_db.cerrar()
            cliente_db.cerrar()
            
            messagebox.showinfo("✅ Cartón Generado", 
                              f"¡Tu cartón está listo para jugar!\n"
                              f"ID: #{carton_id}\n"
                              f"Costo: $1000")
            
            # Actualizar saldo en el dashboard padre
            if hasattr(self.master, 'actualizar_saldo'):
                self.master.actualizar_saldo()
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al generar cartón: {str(e)}")

    def _seleccionar_carton_guardado(self):
        """Mostrar ventana para seleccionar cartón guardado"""
        try:
            carton_db = Carton()
            cartones = carton_db.obtener_cartones_cliente(self.usuario_datos.get('dni'))
            carton_db.cerrar()
            
            if not cartones:
                messagebox.showinfo("📂 Sin Cartones", 
                                  "No tienes cartones guardados.\n"
                                  "¡Genera tu primer cartón!")
                return
            
            # Crear ventana de selección
            self._mostrar_ventana_seleccion(cartones)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al cargar cartones: {str(e)}")

    def _mostrar_ventana_seleccion(self, cartones):
        """Mostrar ventana modal para seleccionar cartón"""
        ventana = tk.Toplevel(self)
        ventana.title("📂 Seleccionar Cartón")
        ventana.geometry("900x600")  # Aumentado de 600x400 a 900x600
        ventana.resizable(True, True)
        ventana.configure(bg="#f0f0f0")
        
        # Centrar ventana
        ventana.transient(self)
        ventana.grab_set()
        
        # Header
        header_frame = tk.Frame(ventana, bg="#2c3e50", height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame,
                text="📂 Selecciona un Cartón para Jugar",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#2c3e50").pack(expand=True)
        
        # Lista de cartones en grid
        content_frame = tk.Frame(ventana, bg="#f0f0f0")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Canvas scrolleable
        canvas = tk.Canvas(content_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        cartones_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        cartones_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=cartones_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mostrar cartones en grid de 2 columnas
        for i, carton in enumerate(cartones):
            row = i // 2
            col = i % 2
            self._crear_carton_seleccion_grid(cartones_frame, carton, ventana, row, col)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        ttk.Button(content_frame,
                  text="Cerrar",
                  command=ventana.destroy,
                  style='Secondary.TButton').pack(pady=(10, 0))

    def _crear_carton_seleccion_grid(self, parent, carton, ventana, row, col):
        """Crear widget de cartón para selección en grid"""
        carton_frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        carton_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Configurar peso de columnas
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Info del cartón
        info_frame = tk.Frame(carton_frame, bg=self._get_color_hex(carton.get('color', 'azul')))
        info_frame.pack(fill="x")
        
        tk.Label(info_frame,
                text=f"🎫 Cartón #{carton['id']} - {carton.get('color', 'azul').title()}",
                font=("Arial", 12, "bold"),
                fg="white",
                bg=self._get_color_hex(carton.get('color', 'azul'))).pack(pady=10)
        
        # Info adicional
        details_frame = tk.Frame(carton_frame, bg="#ffffff")
        details_frame.pack(fill="x", padx=15, pady=10)
        
        fecha = carton['fecha_creacion'].strftime("%d/%m/%Y %H:%M")
        tk.Label(details_frame,
                text=f"Creado: {fecha}",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack()
        
        tk.Label(details_frame,
                text=f"Valor: ${carton.get('valor', 1000)}",
                font=("Arial", 10),
                fg="#7f8c8d",
                bg="#ffffff").pack()
        
        # Preview del cartón (más pequeño)
        preview_frame = tk.Frame(carton_frame, bg="#ffffff")
        preview_frame.pack(padx=10, pady=10)
        
        try:
            disposicion = json.loads(carton['disposicion'])
            # Mostrar solo las primeras 3 filas (primer cartón)
            grid_frame = tk.Frame(preview_frame, bg=self._get_color_light(carton.get('color', 'azul')), relief="solid", bd=1)
            grid_frame.pack()
            
            for i in range(3):
                if i < len(disposicion):
                    fila_frame = tk.Frame(grid_frame, bg=self._get_color_light(carton.get('color', 'azul')))
                    fila_frame.pack()
                    
                    for num in disposicion[i]:
                        tk.Label(fila_frame,
                                text=str(num) if num else "  ",
                                font=("Courier", 8),
                                fg="#2c3e50",
                                bg="white" if num else self._get_color_light(carton.get('color', 'azul')),
                                relief="solid",
                                bd=1,
                                width=3,
                                height=1).pack(side="left", padx=1, pady=1)
        except:
            tk.Label(preview_frame,
                    text="Error al mostrar preview",
                    font=("Arial", 10),
                    fg="#e74c3c",
                    bg="#ffffff").pack()
        
        # Botón seleccionar
        ttk.Button(carton_frame,
                  text="🎮 Seleccionar",
                  command=lambda c=carton: self._usar_carton_seleccionado(c, ventana),
                  style='Primary.TButton').pack(fill="x", padx=15, pady=(0, 15))

    def _usar_carton_seleccionado(self, carton, ventana):
        """Usar cartón seleccionado para jugar"""
        try:
            # Parsear disposición del cartón
            disposicion = json.loads(carton['disposicion'])
            
            # Guardar datos del cartón
            self.carton_actual = carton['id']
            self.carton_data = disposicion
            self.carton_seleccionado = carton
            
            # OBTENER EL COLOR DEL CARTÓN
            color_carton = carton.get('color', 'azul')
            print(f"DEBUG: Color extraído: {color_carton}")
            
            # PASAR EL COLOR COMO SEGUNDO PARÁMETRO
            self._crear_carton_bingo_argentino(disposicion, color_carton)
            
            # Habilitar botón de nueva partida
            self.btn_nueva_partida.configure(state="normal")
            
            ventana.destroy()
            
            messagebox.showinfo("✅ Cartón Seleccionado", 
                            f"Cartón #{carton['id']} ({color_carton}) listo para jugar!")
                            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al seleccionar cartón: {str(e)}")

    def seleccionar_carton_guardado(self, carton):
        """Método público para seleccionar cartón desde otras pestañas"""
        try:
            # Parsear disposición del cartón
            disposicion = json.loads(carton['disposicion'])
            
            # Guardar datos del cartón
            self.carton_actual = carton['id']
            self.carton_data = disposicion
            self.carton_seleccionado = carton
            
            # OBTENER EL COLOR DEL CARTÓN
            color_carton = carton.get('color', 'azul')
            print(f"DEBUG: Color extraído desde otras pestañas: {color_carton}")
            
            # PASAR EL COLOR COMO SEGUNDO PARÁMETRO
            self._crear_carton_bingo_argentino(disposicion, color_carton)
            
            # Habilitar botón de nueva partida
            self.btn_nueva_partida.configure(state="normal")
            
            # Mostrar mensaje con el color correcto
            messagebox.showinfo("✅ Cartón Listo", 
                            f"Cartón #{carton['id']} ({color_carton.title()}) listo para jugar!\n"
                            "Presiona 'Nueva Partida' para comenzar.")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al usar cartón: {str(e)}")

    def _nueva_partida(self):
        """Iniciar una nueva partida"""
        print(f"DEBUG NUEVA PARTIDA: Iniciando nueva partida para DNI {self.usuario_datos.get('dni')}")
        
        if not self.carton_actual or not self.carton_data:
            messagebox.showwarning("⚠️ Advertencia", "Primero selecciona un cartón.\nVe a la Tienda o usa un cartón guardado.")
            return
    
        try:
            # Verificar que no haya partida en curso
            if self.en_partida:
                respuesta = messagebox.askyesno("🎮 Partida en Curso", 
                                            "Ya hay una partida en curso.\n"
                                            "¿Deseas terminarla y comenzar una nueva?")
                if respuesta:
                    self._terminar_partida(False)
                    self.partida_id = None
                else:
                    return
        
            print(f"DEBUG NUEVA PARTIDA: Creando apuesta para cartón {self.carton_actual}")
            
            # Crear apuesta en la base de datos
            apuesta_db = Apuesta()
            self.apuesta_id = apuesta_db.insertar_apuesta(
                self.usuario_datos.get('dni'),
                self.carton_actual,
                "en juego"
            )

            # Crear partida en la base de datos
            partida_db = Partida()
            self.partida_id = partida_db.crear_partida(
                self.usuario_datos.get('dni'),
                self.carton_actual
            )
            print(f"DEBUG NUEVA PARTIDA: ✅ Partida creada con ID: {self.partida_id}")
            partida_db.cerrar()
            
            print(f"DEBUG NUEVA PARTIDA: ✅ Apuesta creada con ID: {self.apuesta_id}")
            
            # Activar cartón
            carton_db = Carton()
            carton_db.activar_carton(self.carton_actual)
            
            apuesta_db.cerrar()
            carton_db.cerrar()
            
            # Reiniciar estado
            self.numeros_cantados = []
            self.numeros_marcados = set()
            self.en_partida = True
            
            # Limpiar grid de números cantados
            for numero, label in self.numeros_labels.items():
                label.configure(
                    bg="#ffffff",
                    fg="#7f8c8d",
                    font=("Arial", 9, "bold")
                )
            
            # Reiniciar cartón visual
            if hasattr(self, 'carton_buttons'):
                for btn in self.carton_buttons.values():
                    btn.configure(bg="white", fg="#2c3e50")
            
            # Actualizar controles
            self.btn_cantar_numero.configure(state="normal")
            self.btn_bingo.configure(state="normal")
            self.btn_nueva_partida.configure(state="disabled")
            self.btn_usar_guardado.configure(state="disabled")
            self.game_status.configure(text="🔴 Partida en curso", fg="#e74c3c")
            self.ultimo_numero_label.configure(text="--")
            
            # Actualizar saldo en tiempo real
            if hasattr(self.master, 'actualizar_saldo'):
                self.master.actualizar_saldo()
            
            messagebox.showinfo("🎮 Nueva Partida", "¡Partida iniciada! ¡Buena suerte!")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al iniciar partida: {str(e)}")

    def _cantar_numero(self):
        """Cantar un nuevo número (1-90 para bingo argentino)"""
        if not self.en_partida:
            return
        
        try:
            # Generar número que no haya salido (1-90)
            numeros_disponibles = [n for n in range(1, 91) if n not in self.numeros_cantados]
            
            if not numeros_disponibles:
                messagebox.showinfo("🎉 Partida Terminada", "¡Todos los números han sido cantados!")
                self._terminar_partida(False)
                return
            
            numero = random.choice(numeros_disponibles)
            self.numeros_cantados.append(numero)
            
            # Actualizar display del último número
            self.ultimo_numero_label.configure(text=str(numero))
            
            # Marcar número en el grid fijo
            if numero in self.numeros_labels:
                self.numeros_labels[numero].configure(
                    bg="#3498db",
                    fg="white",
                    font=("Arial", 8, "bold")
                )
            
            # Auto-marcar en el cartón si está presente
            if numero in self.carton_buttons:
                self._marcar_numero(numero, auto=True)
            
            # Actualizar saldo en tiempo real
            if hasattr(self.master, 'actualizar_saldo'):
                self.master.actualizar_saldo()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al cantar número: {str(e)}")

    def _marcar_numero(self, numero, auto=False):
        """Marcar número en el cartón"""
        if numero in self.carton_buttons and numero in self.numeros_cantados:
            btn = self.carton_buttons[numero]
            btn.configure(bg="#27ae60", fg="white")
            self.numeros_marcados.add(numero)
            
            if not auto:
                messagebox.showinfo("✅ Número Marcado", f"Número {numero} marcado correctamente")

    def _verificar_bingo(self):
        """Verificar si hay bingo (cartón completo en cualquiera de los 6 cartones)"""
        if not self.en_partida or not self.carton_data:
            return
        
        print(f"DEBUG: Verificando bingo con {len(self.numeros_marcados)} números marcados")
        print(f"DEBUG: Números marcados: {sorted(self.numeros_marcados)}")
        
        # Verificar cada uno de los 6 cartones individualmente
        for carton_num in range(6):
            # Cada cartón son 3 filas consecutivas
            inicio_fila = carton_num * 3
            fin_fila = inicio_fila + 3
            
            print(f"DEBUG: Verificando cartón {carton_num + 1} (filas {inicio_fila}-{fin_fila-1})")
            
            # Obtener TODOS los números del cartón actual
            numeros_carton = []
            for fila_idx in range(inicio_fila, fin_fila):
                if fila_idx < len(self.carton_data):
                    fila = self.carton_data[fila_idx]
                    # Agregar solo los números (no None)
                    numeros_carton.extend([num for num in fila if num is not None])
            
            print(f"DEBUG: Cartón {carton_num + 1} tiene {len(numeros_carton)} números: {sorted(numeros_carton)}")
            
            # Verificar si TODOS los números del cartón están marcados
            if len(numeros_carton) > 0:
                numeros_marcados_carton = [num for num in numeros_carton if num in self.numeros_marcados]
                print(f"DEBUG: Cartón {carton_num + 1}: {len(numeros_marcados_carton)}/{len(numeros_carton)} marcados")
                
                if len(numeros_marcados_carton) == len(numeros_carton):
                    print(f"DEBUG: ¡BINGO COMPLETO en cartón {carton_num + 1}!")
                    messagebox.showinfo("🏆 ¡BINGO COMPLETO!", 
                                    f"¡Felicitaciones! ¡Has ganado!\n"
                                    f"Cartón {carton_num + 1} completamente lleno\n"
                                    f"Todos los {len(numeros_carton)} números marcados!")
                    self._terminar_partida(ganador=True)
                    return
        
        # Si llegamos aquí, no hay bingo completo
        total_numeros = sum(1 for fila in self.carton_data for num in fila if num is not None)
        numeros_marcados_total = len(self.numeros_marcados)
        
        messagebox.showwarning("❌ No hay Bingo", 
                            f"Aún no tienes un cartón completo.\n"
                            f"Números marcados totales: {numeros_marcados_total}/{total_numeros}")

    def _terminar_partida(self, ganador=False):
        """Terminar la partida actual"""
        print(f"DEBUG TERMINAR PARTIDA: Iniciando. Ganador={ganador}, apuesta_id={self.apuesta_id}")
        
        try:
            if self.apuesta_id:
                print(f"DEBUG TERMINAR PARTIDA: Actualizando apuesta {self.apuesta_id}, partida {self.partida_id}")
                apuesta_db = Apuesta()
                partida_db = Partida()
                
                if ganador:
                    ganancia = 5000  # Premio por ganar
                    estado = "ganada"
                    
                    # Acreditar ganancia al cliente
                    cliente_db = Cliente()
                    cliente_db.acreditar_saldo(self.usuario_datos.get('dni'), ganancia)
                    cliente_db.cerrar()
                    
                    messagebox.showinfo("🏆 ¡BINGO!", 
                                      f"¡Felicitaciones! ¡Has ganado!\n"
                                      f"Premio: ${ganancia}")
                else:
                    ganancia = 0
                    estado = "perdida"
                
                # Actualizar estado de la apuesta
                apuesta_db.actualizar_estado(self.apuesta_id, estado, ganancia)
                apuesta_db.cerrar()

                # Actualizar estado de la partida
                partida_db.cerrar_partida(self.partida_id, self.numeros_cantados, estado, ganancia)
                partida_db.cerrar()
                
                # ELIMINAR el cartón después de usarlo
                if self.carton_actual:
                    carton_db = Carton()
                    carton_db.eliminar_carton(self.carton_actual)
                    carton_db.cerrar()

            else:
                print(f"DEBUG TERMINAR PARTIDA: ❌ NO HAY apuesta_id - partida no se guardará")
            
            # Reiniciar estado
            self.en_partida = False
            self.apuesta_id = None
            self.numeros_marcados = set()
            self.carton_actual = None  # Limpiar referencia al cartón
            self.carton_data = None
            self.carton_seleccionado = None
            
            # Limpiar visualización del cartón
            for widget in self.carton_container.winfo_children():
                widget.destroy()
            self._crear_carton_vacio()
            
            # Restaurar controles
            self.btn_cantar_numero.configure(state="disabled")
            self.btn_bingo.configure(state="disabled")
            self.btn_nueva_partida.configure(state="disabled")  # Deshabilitado hasta seleccionar nuevo cartón
            self.btn_usar_guardado.configure(state="normal")
            self.game_status.configure(text="🟢 Selecciona un cartón para jugar", fg="#f39c12")
            
            # Actualizar saldo en el dashboard padre
            if hasattr(self.master, 'actualizar_saldo'):
                self.master.actualizar_saldo()
            
            # Actualizar lista de cartones (si existe)
            if hasattr(self.master, 'cartones_frame'):
                try:
                    self.master.cartones_frame.actualizar_cartones()
                except:
                    pass
            
            # Mostrar estadísticas post-partida
            if hasattr(self.master, 'mostrar_estadisticas_post_partida'):
                resultado = {
                    'ganado': ganador,
                    'ganancia': ganancia if ganador else -1000
                }
                self.master.mostrar_estadisticas_post_partida(resultado)
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al terminar partida: {str(e)}")

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