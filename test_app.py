#!/usr/bin/env python
"""
Script de test pour l'application Nosdonnées Flask
"""

import requests
import time
import sys

def test_app():
    """Tester l'application Flask"""
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'application Nosdonnées Flask")
    print("=" * 50)
    
    # Test 1: Page d'accueil
    print("\n1. Test de la page d'accueil...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Page d'accueil accessible")
        else:
            print(f"❌ Erreur {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Impossible d'accéder à l'application: {e}")
        return False
    
    # Test 2: Page de connexion
    print("\n2. Test de la page de connexion...")
    try:
        response = requests.get(f"{base_url}/login", timeout=5)
        if response.status_code == 200:
            print("✅ Page de connexion accessible")
        else:
            print(f"❌ Erreur {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Page d'inscription
    print("\n3. Test de la page d'inscription...")
    try:
        response = requests.get(f"{base_url}/register", timeout=5)
        if response.status_code == 200:
            print("✅ Page d'inscription accessible")
        else:
            print(f"❌ Erreur {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur: {e}")
    
    # Test 4: Liste des bases de données
    print("\n4. Test de la liste des bases de données...")
    try:
        response = requests.get(f"{base_url}/datasets", timeout=5)
        if response.status_code == 200:
            print("✅ Liste des bases de données accessible")
        else:
            print(f"❌ Erreur {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur: {e}")
    
    # Test 5: API de recherche
    print("\n5. Test de l'API de recherche...")
    try:
        response = requests.get(f"{base_url}/api/search?q=test", timeout=5)
        if response.status_code == 200:
            print("✅ API de recherche fonctionnelle")
        else:
            print(f"❌ Erreur {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés !")
    print(f"📱 Application accessible sur: {base_url}")
    print("🔧 Interface d'administration: http://localhost:8000/admin")
    print("👤 Compte admin par défaut: admin / admin123")
    
    return True

if __name__ == "__main__":
    print("⏳ Attendre que l'application démarre...")
    time.sleep(3)  # Attendre que l'app démarre
    test_app() 