---
description: "Flask 01 — Fondamentaux : installation, routes, templates Jinja2, SQLAlchemy, blueprints et API REST."
icon: lucide/book-open-check
tags: ["FLASK", "PYTHON", "ROUTES", "JINJA2", "SQLALCHEMY", "BLUEPRINTS", "API"]
---

# Fondamentaux

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Flask 3.x / Python 3.11+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — L'Atelier Modulaire"
    Un guitariste débutant achète une guitare complète. Un luthier expert part du bois brut et assemble chaque pièce lui-même. Flask est l'atelier du luthier : vous obtenez le corps (routeur HTTP + Jinja2), mais vous choisissez les cordes (SQLAlchemy), le vernis (Flask-Login), l'étui (Flask-Migrate). Résultat : une application parfaitement adaptée à votre besoin, sans rien en trop.

Flask repose sur deux bibliothèques clés :
- **Werkzeug** — routeur HTTP et utilitaires WSGI
- **Jinja2** — moteur de templates (partagé avec Django)

<br>

---

## 1. Installation & Première Application

```bash title="Bash — Installer Flask et créer le projet"
# Activer l'environnement virtuel
python -m venv venv && source venv/bin/activate

# Installer Flask + extensions essentielles
pip install flask flask-sqlalchemy flask-migrate flask-login

# Structure de projet recommandée (Application Factory)
mkdir -p myapp/{templates,static,models,routes}
touch myapp/__init__.py myapp/config.py run.py
```

```python title="Python — run.py : point d'entrée de l'application"
from myapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

```python title="Python — myapp/__init__.py : Application Factory Pattern"
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instances globales (sans app liée)
db       = SQLAlchemy()
migrate  = Migrate()
login    = LoginManager()


def create_app(config_name: str = 'development') -> Flask:
    """Factory : crée et configure l'application Flask."""
    app = Flask(__name__)

    # Configuration
    from myapp.config import config
    app.config.from_object(config[config_name])

    # Initialiser extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth.login'   # Redirection si non connecté

    # Enregistrer les blueprints
    from myapp.routes.main import main_bp
    from myapp.routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
```

```python title="Python — myapp/config.py : configuration par environnement"
import os

class Config:
    SECRET_KEY        = os.environ.get('SECRET_KEY', 'dev-secret-key-CHANGE-ME')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG             = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class ProductionConfig(Config):
    DEBUG             = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:pass@localhost/mydb')

config = {
    'development': DevelopmentConfig,
    'production':  ProductionConfig,
}
```

<br>

---

## 2. Routes & Vues

```python title="Python — myapp/routes/main.py : routes avec Blueprint"
from flask import Blueprint, render_template, request, redirect, url_for, flash
from myapp.models.article import Article
from myapp import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Page d'accueil — liste des articles."""
    articles = Article.query.order_by(Article.created_at.desc()).limit(10).all()
    return render_template('main/index.html', articles=articles)


@main_bp.route('/article/<int:article_id>')
def article_detail(article_id: int):
    """Détail d'un article — 404 si inexistant."""
    article = Article.query.get_or_404(article_id)
    return render_template('main/article_detail.html', article=article)


@main_bp.route('/article/creer', methods=['GET', 'POST'])
def article_create():
    """Créer un nouvel article."""
    if request.method == 'POST':
        title   = request.form['title']
        content = request.form['content']

        if not title or not content:
            flash('Le titre et le contenu sont obligatoires.', 'error')
            return redirect(url_for('main.article_create'))

        article = Article(title=title, content=content)
        db.session.add(article)
        db.session.commit()

        flash('Article créé avec succès !', 'success')
        return redirect(url_for('main.article_detail', article_id=article.id))

    return render_template('main/article_form.html')


# ─── API REST (retourne JSON) ──────────────────────────────────────────────────
@main_bp.route('/api/articles')
def api_articles():
    """API : liste des articles en JSON."""
    from flask import jsonify
    articles = Article.query.all()
    return jsonify([a.to_dict() for a in articles])
```

_Les **Blueprints** Flask sont l'équivalent des modules Laravel : ils groupent routes, templates et logique par fonctionnalité, permettant de diviser une grande application en composants indépendants._

<br>

---

## 3. Modèles SQLAlchemy

```python title="Python — myapp/models/article.py : modèle SQLAlchemy"
from datetime import datetime
from myapp import db

class Article(db.Model):
    """Article de blog."""
    __tablename__ = 'articles'

    id         = db.Column(db.Integer, primary_key=True)
    title      = db.Column(db.String(200), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    published  = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Clé étrangère vers User
    author_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author     = db.relationship('User', backref='articles', lazy=True)

    def to_dict(self) -> dict:
        """Sérialisation JSON."""
        return {
            'id':         self.id,
            'title':      self.title,
            'published':  self.published,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f'<Article {self.id}: {self.title}>'
```

```bash title="Bash — Gérer les migrations SQLAlchemy avec Flask-Migrate"
# Initialiser le système de migrations (une seule fois)
flask db init

# Générer une migration après modification des modèles
flask db migrate -m "Ajout table articles"

# Appliquer les migrations
flask db upgrade

# Revenir en arrière
flask db downgrade
```

<br>

---

## 4. Templates Jinja2

```html title="HTML — templates/base.html : template parent"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Mon Blog{% endblock %}</title>
</head>
<body>
<nav>
    <a href="{{ url_for('main.index') }}">Accueil</a>
    {% if current_user.is_authenticated %}
        <a href="{{ url_for('auth.logout') }}">Déconnexion ({{ current_user.username }})</a>
    {% else %}
        <a href="{{ url_for('auth.login') }}">Connexion</a>
    {% endif %}
</nav>

{# Afficher les messages flash #}
{% with messages = get_flashed_messages(with_categories=true) %}
    {% for category, message in messages %}
        <div class="alert alert-{{ category }}">{{ message }}</div>
    {% endfor %}
{% endwith %}

<main>
    {% block content %}{% endblock %}
</main>
</body>
</html>
```

```html title="HTML — templates/main/index.html : liste des articles"
{% extends 'base.html' %}

{% block title %}Accueil — Mon Blog{% endblock %}

{% block content %}
<h1>Articles récents</h1>

{% for article in articles %}
<article>
    <h2>
        <a href="{{ url_for('main.article_detail', article_id=article.id) }}">
            {{ article.title }}
        </a>
    </h2>
    <time>{{ article.created_at.strftime('%d/%m/%Y') }}</time>
    <p>{{ article.content[:200] }}…</p>
</article>
{% else %}
<p>Aucun article pour le moment.</p>
{% endfor %}
{% endblock %}
```

<br>

---

## 5. API REST avec Flask

```python title="Python — API REST complète avec Flask (sans DRF)"
from flask import Blueprint, jsonify, request, abort
from myapp.models.article import Article
from myapp import db

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/articles', methods=['GET'])
def get_articles():
    """GET /api/v1/articles — Liste paginée."""
    page     = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated = Article.query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'articles': [a.to_dict() for a in paginated.items],
        'total':    paginated.total,
        'pages':    paginated.pages,
        'page':     paginated.page,
    })


@api_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id: int):
    """GET /api/v1/articles/:id"""
    article = Article.query.get_or_404(article_id)
    return jsonify(article.to_dict())


@api_bp.route('/articles', methods=['POST'])
def create_article():
    """POST /api/v1/articles — Créer un article."""
    data = request.get_json()

    if not data or not data.get('title') or not data.get('content'):
        abort(400, description='title et content sont obligatoires')

    article = Article(
        title   = data['title'],
        content = data['content'],
    )
    db.session.add(article)
    db.session.commit()

    return jsonify(article.to_dict()), 201


@api_bp.route('/articles/<int:article_id>', methods=['PUT', 'PATCH'])
def update_article(article_id: int):
    """PUT /api/v1/articles/:id — Modifier un article."""
    article = Article.query.get_or_404(article_id)
    data    = request.get_json()

    if 'title'   in data: article.title   = data['title']
    if 'content' in data: article.content = data['content']

    db.session.commit()
    return jsonify(article.to_dict())


@api_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id: int):
    """DELETE /api/v1/articles/:id"""
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return '', 204


# ─── Gestion globale des erreurs ───────────────────────────────────────────────
@api_bp.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Ressource introuvable', 'detail': str(e)}), 404

@api_bp.errorhandler(400)
def bad_request(e):
    return jsonify({'error': 'Requête invalide', 'detail': str(e)}), 400
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Flask suit le **principe de simplicité** : le minimum obligatoire (routeur + Jinja2), le reste en extensions choisies. L'**Application Factory** (`create_app()`) permet de configurer l'app dynamiquement selon l'environnement. Les **Blueprints** organisent le code en modules réutilisables. **SQLAlchemy** offre un ORM puissant comparable à Eloquent. Le pattern `db.session.add() → db.session.commit()` rythme toutes les écritures. Flask excelle pour les **APIs REST légères** et les **microservices**.

> Module suivant : [Admin & Authentification →](./02-auth.md) — Flask-Login, hachage bcrypt, protection des routes.

<br>
