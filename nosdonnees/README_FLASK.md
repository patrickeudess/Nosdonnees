# Nosdonnées - Application Flask

## 🎯 Description

**Nosdonnées** est une plateforme web de partage et de téléchargement de bases de données dans divers domaines (santé, éducation, agriculture, environnement, économie, etc.).

## ✨ Fonctionnalités

### 👥 Rôles utilisateurs
- **Visiteur** : Consulte et télécharge les bases de données
- **Contributeur** : Propose de nouvelles bases de données
- **Administrateur** : Valide les contributions et gère la plateforme

### 🔍 Fonctionnalités principales
- 📂 Catalogue filtrable des bases de données
- 🔍 Moteur de recherche textuel
- 📝 Pages détaillées pour chaque base de données
- ⬆️ Système d'upload de fichiers
- ✅ Interface d'administration pour validation
- 📈 Statistiques d'usage
- 💬 Système de commentaires et notations

## 🚀 Installation et démarrage

### Prérequis
- Python 3.8+
- pip

### Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd nosdonnees
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements_flask.txt
```

5. **Lancer l'application**
```bash
python app.py
```

6. **Accéder à l'application**
- Ouvrir votre navigateur
- Aller à `http://localhost:8000`

## 👤 Comptes par défaut

### Administrateur
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin123`
- **Rôle** : Administrateur

## 📁 Structure du projet

```
nosdonnees/
├── app.py                 # Application Flask principale
├── requirements_flask.txt # Dépendances Python
├── templates/            # Templates HTML
│   ├── base.html        # Template de base
│   ├── home.html        # Page d'accueil
│   ├── login.html       # Page de connexion
│   └── register.html    # Page d'inscription
├── static/              # Fichiers statiques
│   ├── css/
│   │   └── style.css   # Styles CSS
│   └── js/
│       └── main.js     # JavaScript
└── uploads/            # Dossier des fichiers uploadés
```

## 🛠️ Technologies utilisées

- **Backend** : Flask, SQLAlchemy, Flask-Login
- **Frontend** : Bootstrap 5, Font Awesome, JavaScript
- **Base de données** : SQLite (développement)
- **Templates** : Jinja2

## 📊 Modèles de données

### User
- Informations utilisateur (nom, email, rôle)
- Gestion des rôles (visiteur, contributeur, admin)

### Domain
- Domaines de données (santé, éducation, etc.)
- Description et icônes

### Dataset
- Bases de données avec métadonnées
- Fichiers uploadés et statistiques
- Système de validation

### DownloadLog
- Historique des téléchargements
- Statistiques d'usage

### Comment
- Système de commentaires
- Notations utilisateurs

## 🔧 Configuration

### Variables d'environnement
```bash
# Clé secrète pour les sessions
SECRET_KEY=your-secret-key

# Configuration de la base de données
DATABASE_URL=sqlite:///nosdonnees.db

# Dossier d'upload
UPLOAD_FOLDER=uploads
```

### Production
Pour la production, modifiez `app.py` :
```python
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
```

## 📈 Fonctionnalités avancées

### API REST
- `/api/search` : Recherche de bases de données
- `/api/stats` : Statistiques (admin uniquement)

### Système de validation
- Les contributeurs proposent des bases
- Les admins valident ou rejettent
- Notifications automatiques

### Statistiques
- Bases les plus téléchargées
- Domaines les plus actifs
- Utilisateurs les plus actifs

## 🎨 Interface utilisateur

### Design responsive
- Compatible mobile et desktop
- Interface moderne avec Bootstrap 5
- Animations et transitions fluides

### Accessibilité
- Navigation au clavier
- Contraste adapté
- Textes alternatifs

## 🔒 Sécurité

- Authentification sécurisée
- Validation des fichiers uploadés
- Protection CSRF
- Sanitisation des données

## 🚀 Déploiement

### Heroku
```bash
# Procfile
web: python app.py

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

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Commiter les changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement

---

**Nosdonnées** - Partagez vos données, enrichissez la communauté ! 🚀 