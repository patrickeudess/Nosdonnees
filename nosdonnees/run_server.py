#!/usr/bin/env python
"""
Script pour lancer le serveur de développement Nosdonnées
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    """Lancer le serveur de développement"""
    print("🚀 Lancement du serveur de développement Nosdonnées...")
    print("📱 L'application sera disponible sur: http://localhost:8000")
    print("🔧 Interface d'administration: http://localhost:8000/admin")
    print("⏹️  Appuyez sur Ctrl+C pour arrêter le serveur")
    print("-" * 60)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nosdonnees.settings')
    
    # Lancer le serveur
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    main() 