"""
Archivo de configuración para el proyecto Bingo Seguro
"""

import os

class Config:
    """Configuración base"""
    
    # Base de datos
    DB_HOST = "mysql-bingo-estructuras-estructuras-bingo.g.aivencloud.com"
    DB_PORT = 19042
    DB_USER = "avnadmin"
    DB_PASSWORD = "AVNS_PDkPtgvet2IRp0klIVa"
    DB_NAME = "defaultdb"
    
    # Configuración del juego
    SALDO_INICIAL = 10000
    COSTO_CARTON = 1000
    PREMIO_BINGO = 5000
    
    # Configuración de interfaz
    VENTANA_ANCHO = 1200
    VENTANA_ALTO = 800
    VENTANA_MIN_ANCHO = 800
    VENTANA_MIN_ALTO = 600
    
    # Colores
    COLOR_PRIMARIO = "#4CAF50"
    COLOR_SECUNDARIO = "#2c3e50"
    COLOR_FONDO = "#f0f0f0"
    COLOR_EXITO = "#2ecc71"
    COLOR_ERROR = "#e74c3c"
    COLOR_ADVERTENCIA = "#f39c12"
    
    # Fuentes
    FUENTE_TITULO = ("Arial", 20, "bold")
    FUENTE_SUBTITULO = ("Arial", 14, "bold")
    FUENTE_NORMAL = ("Arial", 11)
    FUENTE_BOTON = ("Arial", 11, "bold")

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    MOSTRAR_ERRORES_DETALLADOS = True

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    MOSTRAR_ERRORES_DETALLADOS = False

# Configuración por defecto
config = DevelopmentConfig