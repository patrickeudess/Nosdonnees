#!/usr/bin/env python
import sys
import os

# Ajouter le répertoire courant au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import nosdonnees
    print("✅ Module nosdonnees importé avec succès")
    
    import datasets
    print("✅ Module datasets importé avec succès")
    
    from datasets.models import Dataset, Domain, UserProfile
    print("✅ Modèles importés avec succès")
    
    from datasets.views import home
    print("✅ Vues importées avec succès")
    
    print("\n🎉 Tous les imports fonctionnent correctement!")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print(f"Python path: {sys.path}") 