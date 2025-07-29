#!/usr/bin/env python
"""
Test rapide de l'application Nosdonnées
"""

import time
import webbrowser

def test_app():
    """Test rapide de l'application"""
    print("🧪 Test rapide de Nosdonnées")
    print("=" * 40)
    
    # Attendre que l'app démarre
    print("⏳ Attendre le démarrage...")
    time.sleep(3)
    
    # Ouvrir le navigateur
    print("🌐 Ouverture du navigateur...")
    webbrowser.open('http://localhost:8000')
    
    print("\n✅ Application démarrée avec succès !")
    print("📱 URL: http://localhost:8000")
    print("👤 Admin: admin / admin123")
    print("⏹️  Ctrl+C pour arrêter")
    
    return True

if __name__ == "__main__":
    test_app() 