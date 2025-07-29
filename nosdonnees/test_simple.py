#!/usr/bin/env python
"""
Test simple de l'application Flask
"""

from app import app

def test_app():
    """Test de l'application"""
    with app.test_client() as client:
        print("🧪 Test de l'application Flask...")
        
        # Test de la page d'accueil
        try:
            response = client.get('/')
            print(f"✅ Page d'accueil: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Erreur: {response.data.decode()}")
        except Exception as e:
            print(f"❌ Erreur page d'accueil: {e}")
        
        # Test de la page de connexion
        try:
            response = client.get('/login')
            print(f"✅ Page login: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Erreur: {response.data.decode()}")
        except Exception as e:
            print(f"❌ Erreur page login: {e}")
        
        # Test de la page d'inscription
        try:
            response = client.get('/register')
            print(f"✅ Page register: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Erreur: {response.data.decode()}")
        except Exception as e:
            print(f"❌ Erreur page register: {e}")

if __name__ == '__main__':
    test_app() 