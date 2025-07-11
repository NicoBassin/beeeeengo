#!/usr/bin/env python3
"""
Script de instalación automática para Bingo Seguro
"""

import subprocess
import sys
import os

def check_python_version():
    """Verificar versión de Python"""
    if sys.version_info < (3, 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {sys.version.split()[0]}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    return True

def install_dependencies():
    """Instalar dependencias automáticamente"""
    print("\n🔄 Instalando dependencias...")
    
    try:
        # Verificar si pymysql ya está instalado
        import pymysql
        print("✅ pymysql ya está instalado")
        return True
    except ImportError:
        # Instalar pymysql
        try:
            print("   Instalando pymysql...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "pymysql>=1.0.2"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ pymysql instalado correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al instalar pymysql: {e}")
            print("   Intenta ejecutar manualmente: pip install pymysql")
            return False

def test_connection():
    """Probar conexión a la base de datos"""
    print("\n🔄 Probando conexión a la base de datos...")
    
    try:
        # Verificar que podemos importar el backend
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from backend import conectar_db
        conn = conectar_db()
        conn.close()
        print("✅ Conexión a base de datos exitosa")
        return True
    except ImportError as e:
        print(f"❌ Error al importar backend.py: {e}")
        print("   Asegúrate de que backend.py esté en el mismo directorio")
        return False
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        print("   Verifica tu conexión a internet")
        return False

def setup_database():
    """Configurar base de datos"""
    print("\n🔄 Configurando base de datos...")
    
    try:
        # Importar y ejecutar la configuración
        from crear_tablas import main as crear_tablas_main
        
        # Ejecutar la configuración
        if crear_tablas_main():
            print("✅ Base de datos configurada correctamente")
            return True
        else:
            print("❌ Error al configurar base de datos")
            return False
            
    except ImportError as e:
        print(f"❌ Error al importar crear_tablas.py: {e}")
        print("   Asegúrate de que crear_tablas.py esté en el mismo directorio")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al configurar base de datos: {e}")
        return False

def verify_files():
    """Verificar que todos los archivos necesarios existan"""
    print("\n🔄 Verificando archivos del proyecto...")
    
    required_files = [
        'app.py',
        'backend.py', 
        'login.py',
        'signup.py',
        'dashboard.py',
        'crear_tablas.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            print(f"❌ Falta: {file}")
        else:
            print(f"✅ Encontrado: {file}")
    
    if missing_files:
        print(f"\n⚠️  Faltan {len(missing_files)} archivo(s) requerido(s)")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    return True

def test_import():
    """Probar importación de módulos principales"""
    print("\n🔄 Probando importación de módulos...")
    
    modules_to_test = [
        ('backend', 'Backend y base de datos'),
        ('login', 'Módulo de login'),
        ('app', 'Aplicación principal')
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description}")
        except Exception as e:
            print(f"❌ Error en {description}: {e}")
            return False
    
    return True

def main():
    """Función principal de instalación"""
    print("🎯 Bingo Seguro - Instalador Automático")
    print("=" * 50)
    
    # Paso 1: Verificar Python
    if not check_python_version():
        return False
    
    # Paso 2: Verificar archivos
    if not verify_files():
        print("\n💡 Asegúrate de ejecutar este script desde el directorio del proyecto")
        return False
    
    # Paso 3: Instalar dependencias
    if not install_dependencies():
        return False
    
    # Paso 4: Probar importaciones
    if not test_import():
        return False
    
    # Paso 5: Probar conexión
    if not test_connection():
        print("\n⚠️  Sin conexión a base de datos. Puedes continuar pero algunas funciones no funcionarán.")
        continuar = input("¿Deseas continuar de todos modos? (s/n): ").lower()
        if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
            return False
    
    # Paso 6: Configurar base de datos (opcional)
    configurar_bd = input("\n¿Deseas configurar la base de datos ahora? (s/n): ").lower()
    if configurar_bd in ['s', 'si', 'sí', 'y', 'yes']:
        if not setup_database():
            print("⚠️  Error al configurar base de datos, pero puedes intentarlo manualmente después")
            print("   Ejecuta: python crear_tablas.py")
    
    # Mensaje final
    print("\n" + "=" * 50)
    print("🎉 ¡Instalación completada!")
    print("\n📋 Para comenzar a jugar:")
    print("   1. Ejecuta: python app.py")
    print("   2. Crea una cuenta o inicia sesión")
    print("   3. ¡Disfruta del bingo!")
    
    print("\n🔧 Si tienes problemas:")
    print("   • Configurar BD manualmente: python crear_tablas.py")
    print("   • Verificar dependencias: pip install pymysql")
    print("   • Revisar conexión a internet")
    
    return True

def quick_start():
    """Inicio rápido sin configuración detallada"""
    print("🚀 Inicio Rápido de Bingo Seguro")
    print("=" * 40)
    
    # Solo instalar dependencias y ejecutar
    if install_dependencies():
        print("\n✅ Listo para ejecutar")
        print("Ejecuta: python app.py")
        return True
    return False

if __name__ == "__main__":
    print("Selecciona el tipo de instalación:")
    print("1. Instalación completa (recomendado)")
    print("2. Inicio rápido")
    
    try:
        opcion = input("\nOpción (1-2): ").strip()
        
        if opcion == "2":
            success = quick_start()
        else:
            success = main()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Instalación cancelada por el usuario")
        success = False
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        success = False
    
    # Mensaje final
    if success:
        print("\n🎮 ¡Todo listo para jugar!")
    else:
        print("\n❌ Instalación no completada")
        print("💡 Puedes intentar ejecutar manualmente:")
        print("   pip install pymysql")
        print("   python crear_tablas.py") 
        print("   python app.py")
    
    input("\nPresiona ENTER para salir...")