#!/usr/bin/env python
"""
Script de démarrage pour Nosdonnées
"""

import os
import sys
import webbrowser
import threading
import time

def start_app():
    """Démarrer l'application Flask"""
    print("🚀 Démarrage de Nosdonnées...")
    print("=" * 50)
    
    # Vérifier que app.py existe
    if not os.path.exists('app.py'):
        print("❌ Erreur: app.py non trouvé")
        return False
    
    # Importer et démarrer l'application
    try:
        from app import app, init_db
        
        # Initialiser la base de données
        print("📊 Initialisation de la base de données...")
        init_db()
        
        # Démarrer le serveur
        print("🌐 Démarrage du serveur web...")
        print("📱 Application accessible sur: http://localhost:8000")
        print("🔧 Interface d'administration: http://localhost:8000/admin")
        print("👤 Compte admin par défaut: admin / admin123")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        # Ouvrir le navigateur après un délai
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8000')
        
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Démarrer l'application
        app.run(debug=True, host='0.0.0.0', port=8000)
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Assurez-vous d'avoir installé les dépendances:")
        print("   pip install -r requirements_flask.txt")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def check_dependencies():
    """Vérifier les dépendances"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = [
        'flask',
        'flask_sqlalchemy', 
        'flask_login',
        'werkzeug'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MANQUANT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("💡 Installez-les avec: pip install -r requirements_flask.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def main():
    """Fonction principale"""
    print("🎯 Nosdonnées - Plateforme de partage de bases de données")
    print("=" * 60)
    
    # Vérifier les dépendances
    if not check_dependencies():
        return
    
    print("\n" + "=" * 60)
    
    # Démarrer l'application
    start_app()

if __name__ == "__main__":
    main() 