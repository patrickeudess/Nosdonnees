#!/usr/bin/env python
"""
Configuration pour l'application Nosdonnées Flask
"""

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'nosdonnees-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///nosdonnees.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration des uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # Configuration de sécurité
    SESSION_COOKIE_SECURE = False  # True en production avec HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Configuration des fichiers
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json', 'xml', 'sql', 'zip'}
    MAX_FILENAME_LENGTH = 255
    
    # Configuration de l'application
    APP_NAME = 'Nosdonnées'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Plateforme de partage de bases de données'
    
    # Configuration des domaines par défaut
    DEFAULT_DOMAINS = [
        {'name': 'Santé', 'description': 'Bases de données liées à la santé publique', 'icon': 'fas fa-heartbeat'},
        {'name': 'Éducation', 'description': 'Données sur l\'éducation et les écoles', 'icon': 'fas fa-graduation-cap'},
        {'name': 'Agriculture', 'description': 'Données agricoles et production', 'icon': 'fas fa-seedling'},
        {'name': 'Environnement', 'description': 'Données environnementales', 'icon': 'fas fa-leaf'},
        {'name': 'Économie', 'description': 'Données économiques et financières', 'icon': 'fas fa-chart-line'},
        {'name': 'Transport', 'description': 'Données de transport et mobilité', 'icon': 'fas fa-car'},
        {'name': 'Démographie', 'description': 'Données démographiques', 'icon': 'fas fa-users'},
        {'name': 'Technologie', 'description': 'Données technologiques', 'icon': 'fas fa-microchip'},
        {'name': 'Culture', 'description': 'Données culturelles et artistiques', 'icon': 'fas fa-palette'},
        {'name': 'Sport', 'description': 'Données sportives', 'icon': 'fas fa-futbol'}
    ]
    
    # Configuration des rôles
    ROLES = {
        'visitor': 'Visiteur',
        'contributor': 'Contributeur', 
        'admin': 'Administrateur'
    }
    
    # Configuration des formats de fichiers
    FILE_FORMATS = {
        'csv': 'CSV - Comma Separated Values',
        'xlsx': 'XLSX - Excel Spreadsheet',
        'json': 'JSON - JavaScript Object Notation',
        'xml': 'XML - eXtensible Markup Language',
        'sql': 'SQL - Structured Query Language',
        'zip': 'ZIP - Compressed Archive'
    }
    
    # Configuration des statistiques
    STATS_CACHE_DURATION = 3600  # 1 heure
    POPULAR_DATASETS_LIMIT = 6
    ACTIVE_DOMAINS_LIMIT = 5
    DATASETS_PER_PAGE = 12
    
    # Configuration des notifications
    FLASH_MESSAGES = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    }

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
class TestingConfig(Config):
    """Configuration pour les tests"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Mapping des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retourner la configuration appropriée"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default']) 