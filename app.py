import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import sys
import os

# Agregar el directorio actual al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from login import LoginFrame
from signup import SignupFrame
from dashboard import DashboardFrame

class App(tk.Tk):
    def __init__(self):
        """Constructor de clase App"""
        super().__init__()
        
        # Configuración de la ventana
        self.title("🎯 Bingo Seguro - Simulador de Bingo Argentino")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.minsize(800, 600)
        
        # Configuración tema y colores
        self.configure(bg="#f0f0f0")
        
        # Configuración estilos
        self._configurar_estilos()
        
        # Variables de usuario actual
        self.usuario_actual = None
        
        # Frame container principal
        self.container = tk.Frame(self, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.frame_actual = None
        
        # Mostrar pantalla inicial
        self.mostrar_login()
        
        # Configuración protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _configurar_estilos(self):
        """Configuración de fuentes y estilos de la aplicación"""
        # Configuración fuentes
        self.font_titulo = tkfont.Font(family="Arial", size=20, weight="bold")
        self.font_subtitulo = tkfont.Font(family="Arial", size=14, weight="bold")
        self.font_normal = tkfont.Font(family="Arial", size=11)
        self.font_boton = tkfont.Font(family="Arial", size=11, weight="bold")
        
        # Configuración estilo para ttk
        style = ttk.Style()
        
        # Intentar usar un tema moderno
        try:
            style.theme_use('clam')
        except:
            pass  # Usar tema por defecto si clam no está disponible
        
        # Estilo para botones principales
        style.configure('Primary.TButton', 
                    font=self.font_boton,
                    foreground='white',
                    background='#48c9b0',
                    borderwidth=0,
                    focuscolor='none',
                    padding=(10, 8))
        style.map('Primary.TButton',
                background=[('active', '#17a2b8'),
                        ('pressed', '#138496')])
        
        # Estilo para botones secundarios
        style.configure('Secondary.TButton',
                       font=self.font_boton,
                       foreground='#333',
                       background='#e0e0e0',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8))
        style.map('Secondary.TButton',
                 background=[('active', '#d0d0d0'),
                           ('pressed', '#c0c0c0')])
        
        # Estilo para entries
        style.configure('Custom.TEntry',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='solid',
                       bordercolor='#ddd',
                       lightcolor='#ddd',
                       darkcolor='#ddd',
                       focuscolor='#4CAF50',
                       padding=5)
        
        # Estilo para notebook (pestañas)
        style.configure('TNotebook',
                       background='#f0f0f0',
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background='#e0e0e0',
                       foreground='#333',
                       padding=[20, 10],
                       font=self.font_normal)
        style.map('TNotebook.Tab',
                 background=[('selected', '#ffffff'),
                           ('active', '#f0f0f0')])

    def cambiar_pantalla(self, nuevo_frame_class, **kwargs):
        """Cambiar entre pantallas principales"""
        try:
            # Destruir frame actual si existe
            if self.frame_actual:
                self.frame_actual.destroy()
            
            # Crear nuevo frame
            self.frame_actual = nuevo_frame_class(self.container, **kwargs)
            self.frame_actual.pack(fill="both", expand=True)
            
            # Actualizar título según la pantalla: cambia entre LoginFrame, SignupFrame o DashboardFrame
            # DashboardFrame contiene "Tabs" para cambiar entre Jugar, Tienda, Cartones, Historial o Estadísticas
            if nuevo_frame_class == LoginFrame:
                self.title("🎯 Bingo Seguro - Iniciar Sesión")
            elif nuevo_frame_class == SignupFrame:
                self.title("🎯 Bingo Seguro - Crear Cuenta")
            elif nuevo_frame_class == DashboardFrame:
                nombre = kwargs.get('usuario_datos', {}).get('nombre', 'Usuario')
                self.title(f"🎯 Bingo Seguro - Dashboard de {nombre}")
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al cambiar pantalla: {str(e)}")

    def mostrar_login(self):
        """Mostrar pantalla de login"""
        self.usuario_actual = None
        self.cambiar_pantalla(LoginFrame)

    def mostrar_signup(self):
        """Mostrar pantalla de registro"""
        self.cambiar_pantalla(SignupFrame)

    def mostrar_dashboard(self, usuario_datos=None):
        """Mostrar dashboard principal"""
        # (aclaración: usuario_datos = None es el valor default del parámetro)
        if not usuario_datos:
            messagebox.showerror("❌ Error", "No se pudieron cargar los datos del usuario")
            self.mostrar_login()
            return
        
        # El usuario actual va a ser el parámetro con el que se loguea el cliente
        self.usuario_actual = usuario_datos
        self.cambiar_pantalla(DashboardFrame, usuario_datos=usuario_datos)
    
    def get_font(self, tipo):
        """Obtener fuentes configuradas"""
        fonts = {
            'titulo': self.font_titulo,
            'subtitulo': self.font_subtitulo,
            'normal': self.font_normal,
            'boton': self.font_boton
        }
        return fonts.get(tipo, self.font_normal)

    def obtener_usuario_actual(self):
        """Obtener datos del usuario actual"""
        return self.usuario_actual.copy() if self.usuario_actual else {}

    def _on_closing(self):
        """Manejar cierre de la aplicación"""
        if self.usuario_actual:
            respuesta = messagebox.askyesno(
                "🚪 Cerrar Aplicación",
                "¿Estás seguro que deseas cerrar la aplicación?\n"
                "Se perderá cualquier partida en curso."
            )
            if respuesta:
                self._cleanup_y_cerrar()
        else:
            self._cleanup_y_cerrar()

    def _cleanup_y_cerrar(self):
        """Limpiar recursos y cerrar aplicación"""
        try:
            pass
        except Exception as e:
            print(f"Error durante cleanup: {e}")
        finally:
            self.destroy()

    def mostrar_error_critico(self, titulo, mensaje):
        """Mostrar error crítico y cerrar aplicación"""
        messagebox.showerror(titulo, f"{mensaje}\n\nLa aplicación se cerrará.")
        self._cleanup_y_cerrar()

    def reiniciar_aplicacion(self):
        """Reiniciar la aplicación"""
        respuesta = messagebox.askyesno(
            "🔄 Reiniciar",
            "¿Deseas reiniciar la aplicación?\n"
            "Se perderán los datos no guardados."
        )
        if respuesta:
            # Limpiar estado
            self.usuario_actual = None
            
            # Volver al login
            self.mostrar_login()

def verificar_dependencias():
    """Verificar que todas las dependencias estén disponibles"""
    try:
        import pymysql
        return True
    except ImportError:
        messagebox.showerror(
            "❌ Dependencias Faltantes",
            "Faltan dependencias requeridas.\n\n"
            "Instala pymysql ejecutando:\n"
            "pip install pymysql"
        )
        return False

def main():
    """Función principal"""
    try:
        # Verificar dependencias
        if not verificar_dependencias():
            return
        
        # Crear aplicación
        app = App()
        
        # Centrar ventana en pantalla
        app.update_idletasks()
        width = app.winfo_width()
        height = app.winfo_height()
        x = (app.winfo_screenwidth() // 2) - (width // 2)
        y = (app.winfo_screenheight() // 2) - (height // 2)
        app.geometry(f"{width}x{height}+{x}+{y}")
        
        # Mostrar mensaje de bienvenida        print("🎯 Bingo Seguro - Simulador de Bingo Argentino")
        print("=" * 50)
        print("✅ Aplicación iniciada correctamente")
        print("📱 Interfaz gráfica cargada")
        print("🎮 ¡Listo para jugar!")
        print("=" * 50)
        
        # Iniciar aplicación
        app.mainloop()
        
    except Exception as e:
        error_msg = f"Error crítico al iniciar la aplicación: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Intentar mostrar error en GUI si es posible
        try:
            messagebox.showerror("❌ Error Crítico", error_msg)
        except:
            pass

if __name__ == "__main__":
    main()
