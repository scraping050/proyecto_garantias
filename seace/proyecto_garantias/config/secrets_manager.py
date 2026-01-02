"""
Módulo de gestión segura de configuración y secretos.
Reemplaza el uso de archivos .env con variables de entorno del sistema.
"""
import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    host: str
    user: str
    password: str
    database: str
    port: int = 3306
    charset: str = 'utf8mb4'
    collation: str = 'utf8mb4_unicode_ci'


@dataclass
class EmailConfig:
    """Configuración de email"""
    host: str
    port: int
    user: str
    password: str
    to: str


@dataclass
class AIConfig:
    """Configuración de servicios de IA"""
    gemini_api_key: str
    groq_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None


class ConfigurationError(Exception):
    """Error de configuración"""
    pass


class Config:
    """
    Gestor de configuración centralizado.
    Lee configuración desde variables de entorno del sistema.
    """
    
    # Prefijo para variables de entorno
    ENV_PREFIX = "GARANTIAS_"
    
    @classmethod
    def get_database_config(cls) -> DatabaseConfig:
        """Obtiene configuración de base de datos"""
        return DatabaseConfig(
            host=cls._get_env("DB_HOST", "localhost"),
            user=cls._get_required_env("DB_USER"),
            password=cls._get_required_env("DB_PASS"),
            database=cls._get_required_env("DB_NAME"),
            port=int(cls._get_env("DB_PORT", "3306"))
        )
    
    @classmethod
    def get_email_config(cls) -> EmailConfig:
        """Obtiene configuración de email"""
        return EmailConfig(
            host=cls._get_env("EMAIL_HOST", "smtp.gmail.com"),
            port=int(cls._get_env("EMAIL_PORT", "587")),
            user=cls._get_required_env("EMAIL_USER"),
            password=cls._get_required_env("EMAIL_PASS"),
            to=cls._get_required_env("EMAIL_TO")
        )
    
    @classmethod
    def get_ai_config(cls) -> AIConfig:
        """Obtiene configuración de IA"""
        # GROQ y OPENAI son opcionales
        groq_key = os.environ.get(f"{cls.ENV_PREFIX}GROQ_API_KEY", None)
        openai_key = os.environ.get(f"{cls.ENV_PREFIX}OPENAI_API_KEY", None)
        return AIConfig(
            gemini_api_key=cls._get_required_env("GEMINI_API_KEY"),
            groq_api_key=groq_key,
            openai_api_key=openai_key
        )
    
    @classmethod
    def _get_env(cls, key: str, default: Optional[str] = None) -> str:
        """Obtiene variable de entorno con prefijo"""
        full_key = f"{cls.ENV_PREFIX}{key}"
        value = os.environ.get(full_key, default)
        if value is None and default is None:
            raise ConfigurationError(
                f"Variable de entorno requerida no encontrada: {full_key}"
            )
        return value
    
    @classmethod
    def _get_required_env(cls, key: str) -> str:
        """Obtiene variable de entorno requerida"""
        return cls._get_env(key)
    
    @classmethod
    def validate_all(cls) -> bool:
        """
        Valida que todas las configuraciones requeridas estén presentes.
        Retorna True si todo está OK, lanza ConfigurationError si falta algo.
        """
        try:
            cls.get_database_config()
            cls.get_email_config()
            cls.get_ai_config()
            return True
        except ConfigurationError as e:
            print(f"ERROR de configuracion: {e}")
            print("\nVariables de entorno requeridas:")
            print("  - GARANTIAS_DB_USER")
            print("  - GARANTIAS_DB_PASS")
            print("  - GARANTIAS_DB_NAME")
            print("  - GARANTIAS_EMAIL_USER")
            print("  - GARANTIAS_EMAIL_PASS")
            print("  - GARANTIAS_EMAIL_TO")
            print("  - GARANTIAS_GEMINI_API_KEY")
            print("\nOpcionales:")
            print("  - GARANTIAS_GROQ_API_KEY (alternativa a Gemini)")
            print("  - GARANTIAS_OPENAI_API_KEY (para procesamiento de consorcios)")
            print("\nEjecuta el script setup_env.bat para configurarlas")
            raise


# Instancia global de configuración
config = Config()


# Funciones de compatibilidad para migración gradual
def get_db_config() -> dict:
    """Retorna configuración de BD en formato dict (compatibilidad)"""
    db = config.get_database_config()
    return {
        'host': db.host,
        'user': db.user,
        'password': db.password,
        'database': db.database,
        'port': db.port,
        'charset': db.charset,
        'collation': db.collation,
        'use_unicode': True,
        'autocommit': False
    }


if __name__ == "__main__":
    # Test de configuración
    print("Validando configuracion...")
    try:
        config.validate_all()
        print("OK - Todas las configuraciones estan correctas")
        
        # Mostrar configuración (sin mostrar secretos)
        db = config.get_database_config()
        print(f"\nBase de Datos:")
        print(f"  Host: {db.host}")
        print(f"  User: {db.user}")
        print(f"  Database: {db.database}")
        print(f"  Password: {'*' * len(db.password)}")
        
        email = config.get_email_config()
        print(f"\nEmail:")
        print(f"  Host: {email.host}:{email.port}")
        print(f"  User: {email.user}")
        print(f"  Password: {'*' * len(email.password)}")
        
        ai = config.get_ai_config()
        print(f"\nIA:")
        print(f"  Gemini API Key: {'*' * 20}...{ai.gemini_api_key[-4:]}")
        if ai.groq_api_key:
            print(f"  Groq API Key: {'*' * 20}...{ai.groq_api_key[-4:]}")
        
    except ConfigurationError:
        print("\nERROR - Configuracion incompleta")
        exit(1)
