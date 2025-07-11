import tkinter as tk
from tkinter import ttk, messagebox
from backend import Cliente
import re
from datetime import datetime, date

class SignupFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master.master  # Referencia a la ventana principal App
        
        self._crear_interfaz()
        
        # Bind Enter key
        self.bind_all('<Return>', lambda e: self.signup())

    def _crear_interfaz(self):
        # Crear scrollable frame
        self._crear_scrollable_frame()
        
        # Título
        titulo_frame = tk.Frame(self.scrollable_frame, bg="#f0f0f0")
        titulo_frame.pack(pady=(0, 20), fill="x")
        
        tk.Label(titulo_frame, 
                text="✨ Crear Cuenta",
                font=self.master.get_font('titulo'),
                fg="#333",
                bg="#f0f0f0").pack()
        
        tk.Label(titulo_frame, 
                text="Complete todos los campos para registrarse",
                font=self.master.get_font('normal'),
                fg="#666",
                bg="#f0f0f0").pack(pady=(5, 0))
        
        # Frame del formulario
        form_frame = tk.Frame(self.scrollable_frame, bg="#ffffff", relief="solid", bd=1)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Padding interno
        self.form_content = tk.Frame(form_frame, bg="#ffffff")
        self.form_content.pack(padx=30, pady=30, fill="both", expand=True)
        
        # Crear campos en dos columnas
        self._crear_campos_formulario()
        
        # Botones
        self._crear_botones()

    def _crear_scrollable_frame(self):
        # Canvas y scrollbar para formulario largo
        canvas = tk.Canvas(self, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", pady=20, padx=(0, 20))
        
        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _crear_campos_formulario(self):
        # Frame para organizar en columnas
        columns_frame = tk.Frame(self.form_content, bg="#ffffff")
        columns_frame.pack(fill="both", expand=True)
        
        # Columna izquierda
        left_column = tk.Frame(columns_frame, bg="#ffffff")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Columna derecha
        right_column = tk.Frame(columns_frame, bg="#ffffff")
        right_column.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        # Campos columna izquierda
        self.entry_dni = self._crear_campo_entrada(left_column, "DNI", 
                                                  placeholder="12345678",
                                                  validacion=self._validar_dni)
        
        self.entry_nombre = self._crear_campo_entrada(left_column, "Nombre",
                                                     placeholder="Juan")
        
        self.entry_apellido = self._crear_campo_entrada(left_column, "Apellido",
                                                       placeholder="Pérez")
        
        self.entry_fecha_nac = self._crear_campo_entrada(left_column, "Fecha de Nacimiento",
                                                        placeholder="YYYY-MM-DD",
                                                        validacion=self._validar_fecha)
        
        # Campos columna derecha
        self.entry_mail = self._crear_campo_entrada(right_column, "Email",
                                                   placeholder="usuario@email.com",
                                                   validacion=self._validar_email)
        
        self.entry_telefono = self._crear_campo_entrada(right_column, "Teléfono",
                                                       placeholder="1134567890")
        
        self.entry_password = self._crear_campo_entrada(right_column, "Contraseña",
                                                       show="*",
                                                       validacion=self._validar_password)
        
        self.entry_password_confirm = self._crear_campo_entrada(right_column, "Confirmar Contraseña",
                                                              show="*")
        
        # Información sobre edad
        info_edad = tk.Frame(self.form_content, bg="#ffffff")
        info_edad.pack(fill="x", pady=(20, 0))
        
        tk.Label(info_edad,
                text="⚠️ Debes ser mayor de 18 años para registrarte",
                font=self.master.get_font('normal'),
                fg="#ff6b35",
                bg="#ffffff").pack()

    def _crear_campo_entrada(self, parent, label_text, placeholder="", show=None, validacion=None):
        # Frame del campo
        field_frame = tk.Frame(parent, bg="#ffffff")
        field_frame.pack(fill="x", pady=(0, 15))
        
        # Label con indicador de obligatorio
        label_frame = tk.Frame(field_frame, bg="#ffffff")
        label_frame.pack(fill="x")
        
        tk.Label(label_frame, 
                text=label_text,
                font=self.master.get_font('normal'),
                fg="#333",
                bg="#ffffff",
                anchor="w").pack(side="left")
        
        tk.Label(label_frame,
                text="*",
                fg="red",
                bg="#ffffff").pack(side="left", padx=(2, 0))
        
        # Entry con placeholder
        entry = ttk.Entry(field_frame, 
                         font=self.master.get_font('normal'),
                         show=show,
                         style='Custom.TEntry')
        entry.pack(fill="x", ipady=8, pady=(5, 0))
        
        # Placeholder effect
        if placeholder:
            entry.insert(0, placeholder)
            entry.configure(foreground='grey')
            
            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.configure(foreground='black')
            
            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.configure(foreground='grey')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        # Validación en tiempo real
        if validacion:
            def on_validate(event):
                valor = entry.get()
                if valor and valor != placeholder:
                    if validacion(valor):
                        entry.configure(style='Valid.TEntry')
                    else:
                        entry.configure(style='Invalid.TEntry')
                else:
                    entry.configure(style='Custom.TEntry')
            
            entry.bind('<KeyRelease>', on_validate)
            
            # Configurar estilos de validación
            style = ttk.Style()
            style.configure('Valid.TEntry', bordercolor='green')
            style.configure('Invalid.TEntry', bordercolor='red')
        
        return entry

    def _crear_botones(self):
        button_frame = tk.Frame(self.form_content, bg="#ffffff")
        button_frame.pack(fill="x", pady=(30, 0))
        
        # Botón registrarse
        self.btn_signup = ttk.Button(button_frame,
                                   text="Crear Cuenta",
                                   command=self.signup,
                                   style='Primary.TButton')
        self.btn_signup.pack(fill="x", pady=(0, 10))
        
        # Botón volver
        ttk.Button(button_frame,
                  text="← Volver al Login",
                  command=self.ir_a_login,
                  style='Secondary.TButton').pack(fill="x")

    def _validar_dni(self, dni):
        return dni.isdigit() and 7 <= len(dni) <= 8

    def _validar_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _validar_password(self, password):
        return len(password) >= 6

    def _obtener_valor_campo(self, entry, placeholder=""):
        """Obtener valor real del campo (sin placeholder)"""
        valor = entry.get()
        return valor if valor != placeholder else ""

    def _validar_todos_campos(self):
        """Validación completa del formulario"""
        errores = []
        
        # Obtener valores
        dni = self._obtener_valor_campo(self.entry_dni, "12345678")
        nombre = self._obtener_valor_campo(self.entry_nombre, "Juan")
        apellido = self._obtener_valor_campo(self.entry_apellido, "Pérez")
        email = self._obtener_valor_campo(self.entry_mail, "usuario@email.com")
        telefono = self._obtener_valor_campo(self.entry_telefono, "1134567890")
        fecha_nac = self._obtener_valor_campo(self.entry_fecha_nac, "YYYY-MM-DD")
        password = self.entry_password.get()
        password_confirm = self.entry_password_confirm.get()
        
        # Validaciones
        if not dni:
            errores.append("DNI es obligatorio")
        elif not self._validar_dni(dni):
            errores.append("DNI inválido (7-8 dígitos)")
            
        if not nombre:
            errores.append("Nombre es obligatorio")
        elif len(nombre) < 2:
            errores.append("Nombre muy corto")
            
        if not apellido:
            errores.append("Apellido es obligatorio")
        elif len(apellido) < 2:
            errores.append("Apellido muy corto")
            
        if not email:
            errores.append("Email es obligatorio")
        elif not self._validar_email(email):
            errores.append("Email inválido")
            
        if not telefono:
            errores.append("Teléfono es obligatorio")
        elif not telefono.isdigit() or len(telefono) < 8:
            errores.append("Teléfono inválido")
            
        if not fecha_nac:
            errores.append("Fecha de nacimiento es obligatoria")
        elif not self._validar_fecha(fecha_nac):
            errores.append("Fecha inválida (formato YYYY-MM-DD)")
            
        if not password:
            errores.append("Contraseña es obligatoria")
        elif not self._validar_password(password):
            errores.append("Contraseña debe tener al menos 6 caracteres")
            
        if password != password_confirm:
            errores.append("Las contraseñas no coinciden")
            
        return errores, {
            'dni': dni, 'nombre': nombre, 'apellido': apellido,
            'email': email, 'telefono': telefono, 'fecha_nac': fecha_nac,
            'password': password
        }

    def _mostrar_loading(self, mostrar=True):
        """Mostrar estado de carga"""
        if mostrar:
            self.btn_signup.configure(text="Creando cuenta...", state="disabled")
        else:
            self.btn_signup.configure(text="Crear Cuenta", state="normal")

    def signup(self):
        # Validar campos
        errores, datos = self._validar_todos_campos()
        
        if errores:
            messagebox.showerror("Campos inválidos", "\n".join(errores))
            return
        
        # Mostrar loading
        self._mostrar_loading(True)
        
        # Procesar después de mostrar loading
        self.after(100, self._procesar_signup, datos)
    
    def _procesar_signup(self, datos):
        try:
            cliente = Cliente()
            cliente.insertar_cliente(
                datos['dni'], datos['nombre'], datos['apellido'],
                datos['email'], datos['telefono'], datos['fecha_nac'],
                datos['password']
            )
            
            messagebox.showinfo("✅ Éxito", 
                              f"¡Cuenta creada exitosamente!\n"
                              f"Bienvenido {datos['nombre']} {datos['apellido']}")
            
            self.limpiar_campos()
            self.master.mostrar_login()
            
        except ValueError as e:
            messagebox.showerror("❌ Error", str(e))
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
        finally:
            self._mostrar_loading(False)
            try:
                cliente.cerrar()
            except:
                pass

    def limpiar_campos(self):
        """Limpiar todos los campos"""
        campos = [
            (self.entry_dni, "12345678"),
            (self.entry_nombre, "Juan"),
            (self.entry_apellido, "Pérez"),
            (self.entry_mail, "usuario@email.com"),
            (self.entry_telefono, "1134567890"),
            (self.entry_fecha_nac, "YYYY-MM-DD"),
        ]
        
        for entry, placeholder in campos:
            entry.delete(0, tk.END)
            if placeholder:
                entry.insert(0, placeholder)
                entry.configure(foreground='grey')
        
        # Campos de contraseña
        self.entry_password.delete(0, tk.END)
        self.entry_password_confirm.delete(0, tk.END)

    def ir_a_login(self):
        self.master.mostrar_login()