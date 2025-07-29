# 🚀 Guide d'utilisation - Nosdonnées

## 📋 Vue d'ensemble

**Nosdonnées** est une plateforme web de partage et de téléchargement de bases de données dans divers domaines (santé, éducation, agriculture, environnement, économie, etc.).

## 🎯 Fonctionnalités principales

### 👥 Rôles utilisateurs
- **Visiteur** : Consulte et télécharge les bases de données
- **Contributeur** : Propose de nouvelles bases de données
- **Administrateur** : Valide les contributions et gère la plateforme

### 🔍 Fonctionnalités
- 📂 Catalogue filtrable des bases de données
- 🔍 Moteur de recherche textuel
- 📝 Pages détaillées pour chaque base de données
- ⬆️ Système d'upload de fichiers
- ✅ Interface d'administration pour validation
- 📈 Statistiques d'usage
- 💬 Système de commentaires et notations

## 🚀 Démarrage rapide

### 1. Installation
```bash
# Cloner le projet
git clone <repository-url>
cd nosdonnees

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements_flask.txt
```

### 2. Lancement
```bash
python app.py
```

### 3. Accès
- **Application** : http://localhost:8000
- **Compte admin** : admin / admin123

## 👤 Utilisation par rôle

### 🔍 Visiteur

#### Navigation
1. **Page d'accueil** : Vue d'ensemble avec statistiques
2. **Catalogue** : Parcourir toutes les bases de données
3. **Recherche** : Utiliser les filtres par domaine, format, etc.
4. **Détail** : Consulter les informations complètes d'une base

#### Actions disponibles
- ✅ Consulter les métadonnées
- ✅ Télécharger les bases validées
- ✅ Laisser des commentaires (après inscription)
- ✅ Noter les bases de données

### 📤 Contributeur

#### Inscription
1. Aller sur `/register`
2. Remplir le formulaire d'inscription
3. Se connecter avec ses identifiants

#### Proposer une base de données
1. Se connecter à son compte
2. Aller sur `/upload`
3. Remplir le formulaire :
   - **Titre** : Nom de la base de données
   - **Description** : Explication détaillée
   - **Domaine** : Catégorie (santé, éducation, etc.)
   - **Source** : URL de la source (optionnel)
   - **Mots-clés** : Tags séparés par des virgules
   - **Fichier** : CSV, XLSX, JSON, XML, SQL, ZIP (max 100MB)
   - **Documentation** : Instructions d'utilisation (optionnel)

#### Suivi des propositions
1. Aller sur `/dashboard`
2. Voir le statut de validation
3. Modifier ou supprimer si nécessaire

### 🔧 Administrateur

#### Validation des contributions
1. Se connecter avec le compte admin
2. Aller sur `/dashboard`
3. Onglet "En attente de validation"
4. Consulter les détails de chaque proposition
5. Valider ou rejeter avec un commentaire

#### Gestion de la plateforme
- 📊 **Statistiques** : Voir les métriques d'usage
- 👥 **Utilisateurs** : Gérer les comptes
- 🏷️ **Domaines** : Ajouter/modifier les catégories
- 📈 **Rapports** : Analyser l'activité

## 📊 Interface utilisateur

### 🏠 Page d'accueil
- **Hero section** : Présentation de la plateforme
- **Statistiques** : Nombre de bases, téléchargements, utilisateurs
- **Bases populaires** : Les plus téléchargées
- **Domaines actifs** : Catégories les plus utilisées

### 📂 Catalogue des bases
- **Filtres** : Domaine, format, année, pays
- **Recherche** : Mots-clés dans le titre et description
- **Tri** : Par date, popularité, note
- **Pagination** : Navigation entre les pages

### 📝 Page de détail
- **Informations complètes** : Titre, description, source, auteur
- **Métadonnées** : Date, taille, format, domaine
- **Statistiques** : Téléchargements, vues, note moyenne
- **Téléchargement** : Bouton pour récupérer le fichier
- **Commentaires** : Avis et notations des utilisateurs
- **Bases similaires** : Suggestions de contenus liés

### 📊 Dashboard
- **Statistiques personnelles** : Bases proposées, téléchargements
- **Mes bases** : Liste des contributions avec statut
- **Actions** : Modifier, supprimer, voir les détails
- **Profil** : Informations personnelles et paramètres

## 🔧 Configuration avancée

### Variables d'environnement
```bash
# Clé secrète pour les sessions
SECRET_KEY=your-secret-key

# Configuration de la base de données
DATABASE_URL=sqlite:///nosdonnees.db

# Dossier d'upload
UPLOAD_FOLDER=uploads

# Taille maximale des fichiers (en bytes)
MAX_CONTENT_LENGTH=104857600  # 100MB
```

### Production
```python
# app.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
```

## 🛠️ Développement

### Structure du projet
```
nosdonnees/
├── app.py                 # Application Flask principale
├── requirements_flask.txt # Dépendances Python
├── templates/            # Templates HTML
│   ├── base.html        # Template de base
│   ├── home.html        # Page d'accueil
│   ├── login.html       # Connexion
│   ├── register.html    # Inscription
│   ├── dataset_list.html # Catalogue
│   ├── dataset_detail.html # Détail
│   ├── dataset_upload.html # Upload
│   └── dashboard.html   # Dashboard
├── static/              # Fichiers statiques
│   ├── css/style.css   # Styles CSS
│   └── js/main.js      # JavaScript
└── uploads/            # Fichiers uploadés
```

### Modèles de données
- **User** : Utilisateurs avec rôles
- **Domain** : Domaines de données
- **Dataset** : Bases de données
- **DownloadLog** : Historique des téléchargements
- **Comment** : Commentaires et notations

### API REST
- `GET /api/search?q=query` : Recherche de bases
- `GET /api/stats` : Statistiques (admin uniquement)

## 🔒 Sécurité

### Authentification
- Sessions sécurisées avec Flask-Login
- Hachage des mots de passe avec Werkzeug
- Protection CSRF intégrée

### Validation des fichiers
- Types autorisés : CSV, XLSX, JSON, XML, SQL, ZIP
- Taille maximale : 100MB
- Vérification des extensions

### Permissions
- **Visiteur** : Lecture seule
- **Contributeur** : Lecture + écriture (propositions)
- **Admin** : Toutes les permissions

## 📈 Statistiques et métriques

### Métriques utilisateur
- Nombre de bases proposées
- Nombre de bases validées
- Total des téléchargements
- Note moyenne reçue

### Métriques globales
- Total des bases de données
- Total des téléchargements
- Nombre d'utilisateurs
- Bases les plus populaires
- Domaines les plus actifs

## 🚀 Déploiement

### Heroku
```bash
# Procfile
web: gunicorn app:app

# requirements.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
gunicorn==20.1.0
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_flask.txt .
RUN pip install -r requirements_flask.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

## 🐛 Dépannage

### Problèmes courants
1. **Erreur de base de données** : Supprimer `nosdonnees.db` et relancer
2. **Fichiers non trouvés** : Vérifier le dossier `uploads/`
3. **Erreur de permissions** : Vérifier les droits d'écriture

### Logs
```bash
# Activer le mode debug
export FLASK_ENV=development
python app.py
```

## 📞 Support

### Documentation
- **README_FLASK.md** : Documentation technique
- **GUIDE_UTILISATION.md** : Ce guide
- **Code source** : Commentaires dans le code

### Contact
- **Issues GitHub** : Signaler les bugs
- **Pull Requests** : Proposer des améliorations
- **Email** : support@nosdonnees.fr

---

**Nosdonnées** - Partagez vos données, enrichissez la communauté ! 🚀

*Version 1.0 - Flask* 