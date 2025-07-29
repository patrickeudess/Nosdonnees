# 🚀 Démarrage rapide - Nosdonnées

## ⚡ Démarrage en 3 étapes

### 1. Lancer l'application
```bash
python app.py
```

### 2. Ouvrir le navigateur
- **URL** : http://localhost:8000
- **Admin** : admin / admin123

### 3. Commencer à utiliser
- **Parcourir** : Catalogue des bases de données
- **S'inscrire** : Créer un compte contributeur
- **Proposer** : Uploader une base de données
- **Administrer** : Valider les contributions (admin)

## 🎯 Fonctionnalités principales

### 👥 Rôles utilisateurs
- **Visiteur** : Consulter et télécharger
- **Contributeur** : Proposer des bases
- **Administrateur** : Valider et gérer

### 📂 Actions disponibles
- ✅ **Consulter** : Catalogue avec filtres
- ✅ **Rechercher** : Par mots-clés et domaines
- ✅ **Télécharger** : Bases validées
- ✅ **Proposer** : Upload de nouveaux fichiers
- ✅ **Commenter** : Noter et donner son avis
- ✅ **Administrer** : Validation des contributions

## 🔧 Comptes par défaut

### Administrateur
- **Nom** : admin
- **Mot de passe** : admin123
- **Rôle** : Administrateur complet

### Créer un compte contributeur
1. Aller sur `/register`
2. Remplir le formulaire
3. Se connecter avec ses identifiants

## 📊 Domaines disponibles

- 🏥 **Santé** : Données médicales et sanitaires
- 🎓 **Éducation** : Données scolaires et universitaires
- 🌾 **Agriculture** : Données agricoles et production
- 🌱 **Environnement** : Données environnementales
- 💰 **Économie** : Données économiques et financières
- 🚗 **Transport** : Données de mobilité
- 👥 **Démographie** : Données de population
- 💻 **Technologie** : Données technologiques

## 📁 Formats acceptés

- **CSV** : Données tabulaires
- **XLSX** : Fichiers Excel
- **JSON** : Données structurées
- **XML** : Données formatées
- **SQL** : Scripts de base de données
- **ZIP** : Archives compressées

## 🚨 En cas de problème

### Erreur de base de données
```bash
# Supprimer et recréer la base
del nosdonnees.db
python app.py
```

### Erreur de dépendances
```bash
# Réinstaller les dépendances
pip install -r requirements_flask.txt
```

### Port déjà utilisé
```bash
# Changer le port dans app.py
app.run(debug=True, host='0.0.0.0', port=8001)
```

## 📞 Support

- **Documentation** : `README_FLASK.md`
- **Guide complet** : `GUIDE_UTILISATION.md`
- **Résumé projet** : `RESUME_PROJET.md`

---

**🎉 Votre application Nosdonnées est prête !** 