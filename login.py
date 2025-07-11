import tkinter as tk
from tkinter import ttk, messagebox
from backend import Cliente
import re

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0")
        self.master = master.master  # Referencia a la ventana principal App
        
        self._crear_interfaz()
        
        # Bind Enter key para login rápido
        self.bind_all('<Return>', lambda e: self.evento_log_in())

    def _crear_interfaz(self):
        # Frame principal centrado
        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Título
        titulo_frame = tk.Frame(main_frame, bg="#f0f0f0")
        titulo_frame.pack(pady=(0, 30))
        
        tk.Label(titulo_frame, 
                text="🎯", 
                font=("Arial", 48),
                bg="#f0f0f0").pack()
        
        tk.Label(titulo_frame, 
                text="Bingo Seguro", 
                font=self.master.get_font('titulo'),
                fg="#333",
                bg="#f0f0f0").pack()
        
        tk.Label(titulo_frame, 
                text="Inicia sesión para continuar", 
                font=self.master.get_font('normal'),
                fg="#666",
                bg="#f0f0f0").pack(pady=(5, 0))
        
        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="solid", bd=1)
        form_frame.pack(pady=20, padx=40, fill="x")
        
        # Padding interno del formulario
        form_content = tk.Frame(form_frame, bg="#ffffff")
        form_content.pack(padx=30, pady=30, fill="x")
        
        # Campo DNI
        self._crear_campo_entrada(form_content, "DNI", "entry_dni")
        
        # Campo Contraseña
        self._crear_campo_entrada(form_content, "Contraseña", "entry_password", show="*")
        
        # Frame de botones
        button_frame = tk.Frame(form_content, bg="#ffffff")
        button_frame.pack(fill="x", pady=(20, 0))
        
        # Botón de login
        self.btn_login = ttk.Button(button_frame, 
                                  text="Iniciar Sesión",
                                  command=self.evento_log_in,
                                  style='Primary.TButton')
        self.btn_login.pack(fill="x", pady=(0, 10))
        
        # Botón de registro
        ttk.Button(button_frame, 
                  text="¿No tienes cuenta? Regístrate",
                  command=self.ir_a_signup,
                  style='Secondary.TButton').pack(fill="x")
        
        # Información adicional
        info_frame = tk.Frame(main_frame, bg="#f0f0f0")
        info_frame.pack(pady=(20, 0))
        
        tk.Label(info_frame, 
                text="🔒 Plataforma segura y confiable",
                font=self.master.get_font('normal'),
                fg="#666",
                bg="#f0f0f0").pack()

    def _crear_campo_entrada(self, parent, label_text, attr_name, show=None):
        # Frame del campo
        field_frame = tk.Frame(parent, bg="#ffffff")
        field_frame.pack(fill="x", pady=(0, 15))
        
        # Label
        tk.Label(field_frame, 
                text=label_text,
                font=self.master.get_font('normal'),
                fg="#333",
                bg="#ffffff",
                anchor="w").pack(fill="x", pady=(0, 5))
        
        # Entry
        entry = ttk.Entry(field_frame, 
                         font=self.master.get_font('normal'),
                         show=show,
                         style='Custom.TEntry')
        entry.pack(fill="x", ipady=8)
        
        # Guardar referencia
        setattr(self, attr_name, entry)
        
        return entry

    def _validar_campos(self):
        """Validar campos antes del login"""
        dni = self.entry_dni.get().strip()
        password = self.entry_password.get()
        
        errores = []
        
        if not dni:
            errores.append("El DNI es obligatorio")
        elif not dni.isdigit():
            errores.append("El DNI debe contener solo números")
        elif len(dni) < 7 or len(dni) > 8:
            errores.append("El DNI debe tener entre 7 y 8 dígitos")
            
        if not password:
            errores.append("La contraseña es obligatoria")
        elif len(password) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres")
            
        return errores

    def _mostrar_loading(self, mostrar=True):
        """Mostrar estado de carga"""
        try:
            if mostrar:
                if hasattr(self, 'btn_login') and self.btn_login.winfo_exists():
                    self.btn_login.configure(text="Verificando...", state="disabled")
                if hasattr(self, 'entry_dni') and self.entry_dni.winfo_exists():
                    self.entry_dni.configure(state="disabled")
                if hasattr(self, 'entry_password') and self.entry_password.winfo_exists():
                    self.entry_password.configure(state="disabled")
            else:
                if hasattr(self, 'btn_login') and self.btn_login.winfo_exists():
                    self.btn_login.configure(text="Iniciar Sesión", state="normal")
                if hasattr(self, 'entry_dni') and self.entry_dni.winfo_exists():
                    self.entry_dni.configure(state="normal")
                if hasattr(self, 'entry_password') and self.entry_password.winfo_exists():
                    self.entry_password.configure(state="normal")
        except tk.TclError:
            # Widget ya fue destruido, ignorar
            pass

    def log_in(self, dni, password):
        """Lógica mejorada de login"""
        try:
            cliente = Cliente()
            datos = cliente.obtener_cliente_por_dni(dni)
            
            if not datos:
                return False, "DNI no registrado", None
            
            if cliente.hashear_pass(password) == datos['password']:
                return True, f"¡Bienvenido {datos['nombre']} {datos['apellido']}!", datos
            else:
                return False, "Contraseña incorrecta", None
                
        except Exception as e:
            return False, f"Error de conexión: {str(e)}", None
        finally:
            try:
                cliente.cerrar()
            except:
                pass

    def evento_log_in(self):
        # Validar campos
        errores = self._validar_campos()
        if errores:
            messagebox.showerror("Campos inválidos", "\n".join(errores))
            return
        
        # Obtener datos
        dni = self.entry_dni.get().strip()
        password = self.entry_password.get()
        
        # Mostrar loading
        self._mostrar_loading(True)
        
        # Procesar después de mostrar loading
        self.after(100, self._procesar_login, dni, password)
    
    def _procesar_login(self, dni, password):
        try:
            exito, mensaje, datos_usuario = self.log_in(dni, password)
            
            if exito:
                messagebox.showinfo("✅ Éxito", mensaje)
                self._limpiar_campos()
                self.master.mostrar_dashboard(datos_usuario)
                return  # Salir temprano para evitar _mostrar_loading
            else:
                messagebox.showerror("❌ Error", mensaje)
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error inesperado: {str(e)}")
        finally:
            # Solo restaurar loading si el widget aún existe
            try:
                self._mostrar_loading(False)
            except:
                pass  # Ignorar si el widget ya fue destruido

    def _limpiar_campos(self):
        """Limpiar campos del formulario"""
        self.entry_dni.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def ir_a_signup(self):
        self.master.mostrar_signup()