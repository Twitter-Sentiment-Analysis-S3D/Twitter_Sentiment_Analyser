# project/server/config.py
import os


class BaseConfig:
    """Base configuration."""

    FLASK_APP = "main/__init__.py"
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious")
    DEBUG = False
    BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACKslgEAAAAA2K0bF%2B98t7a5z83N33PuwF5185g%3DMCRnSDBsCT0rVRTeuzVawob7XLNbyiFdPTwlgRUTxIzbBCQrHv"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    FLASK_ENV = "development"


class TestingConfig(BaseConfig):
    """Testing configuration."""

    DEBUG = True
    FLASK_ENV = "testing"


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DEBUG = False
    FLASK_ENV = "production"
