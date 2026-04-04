---
description: "Django 01 — Fondamentaux : installation, architecture MVT, vues, templates, ORM et migrations."
icon: lucide/book-open-check
tags: ["DJANGO", "PYTHON", "MVT", "ORM", "TEMPLATES", "MIGRATIONS"]
---

# Module 01 — Fondamentaux Django

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Django 5.x / Python 3.11+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Cuisine Professionnelle"
    Ouvrir un restaurant depuis zéro demande des mois de travail : plomberie, électricité, équipements, certifications. Django, c'est la cuisine déjà construite et certifiée : vous entrez, vous cuisinez. L'ORM est le plan de travail, les templates sont les assiettes, l'admin est le caissier automatique. Vous vous concentrez sur votre recette (la logique métier), pas sur l'infrastructure.

Django suit le pattern **MVT** (Model – View – Template), une variante de MVC adaptée au web :

| Couche | Responsabilité | Analogie |
|---|---|---|
| **Model** | Données + logique métier (ORM) | Ingrédients & recettes |
| **View** | Traitement requête → réponse | Chef cuisinier |
| **Template** | Présentation HTML | Dressage de l'assiette |

<br>

---

## 1. Installation & Création de Projet

```bash title="Bash — Installer Django dans un environnement virtuel"
# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate          # macOS/Linux
venv\Scripts\activate             # Windows

# Installer Django
pip install django

# Vérifier la version
python -m django --version
# 5.x.x
```

```bash title="Bash — Créer un projet Django et une application"
# Créer le projet (génère la structure de base)
django-admin startproject monprojet .
# Le . crée les fichiers dans le dossier courant

# Créer une application métier
python manage.py startapp blog

# Lancer le serveur de développement
python manage.py runserver
# http://127.0.0.1:8000/
```

```
Structure générée :
monprojet/
├── manage.py              ← CLI Django (commandes artisan-like)
├── monprojet/
│   ├── settings.py        ← Configuration globale
│   ├── urls.py            ← Routeur principal
│   └── wsgi.py            ← Interface serveur WSGI
└── blog/
    ├── models.py           ← Modèles (ORM)
    ├── views.py            ← Vues (contrôleurs)
    ├── urls.py             ← Routes de l'app (à créer)
    └── templates/          ← Templates HTML (à créer)
```

<br>

---

## 2. Configuration Essentielle

```python title="Python — settings.py : déclarer l'application et configurer la BDD"
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',                   # ← Déclarer notre application ici
]

# Base de données (SQLite par défaut — parfait pour le dev)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Pour PostgreSQL en production :
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydb',
#         'USER': 'myuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
```

<br>

---

## 3. Models — L'ORM Django

```python title="Python — blog/models.py : définir les modèles de données"
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Catégorie d'articles."""
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)        # URL-friendly (ex: python-tips)

    class Meta:
        verbose_name_plural = 'catégories'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    """Article de blog."""

    STATUS_CHOICES = [
        ('draft',     'Brouillon'),
        ('published', 'Publié'),
    ]

    title      = models.CharField(max_length=200)
    slug       = models.SlugField(unique=True)
    content    = models.TextField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)  # Défini à la création
    updated_at = models.DateTimeField(auto_now=True)       # Mis à jour automatiquement
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags       = models.ManyToManyField('Tag', blank=True)

    class Meta:
        ordering = ['-created_at']   # Plus récents en premier

    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    """Tag pour classifier les articles."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
```

```bash title="Bash — Générer et appliquer les migrations"
# Générer le fichier de migration depuis les modèles
python manage.py makemigrations blog
# Migrations for 'blog':
#   blog/migrations/0001_initial.py
#     - Create model Category
#     - Create model Tag
#     - Create model Article

# Appliquer les migrations (créer les tables)
python manage.py migrate

# Voir l'état des migrations
python manage.py showmigrations
```

<br>

---

## 4. QuerySet API — Requêtes ORM

```python title="Python — Requêtes ORM (équivalent SQL en Python)"
from blog.models import Article, Category

# ─── Créer ────────────────────────────────────────────────────────────────────
cat = Category.objects.create(name='Python', slug='python')

article = Article.objects.create(
    title   = 'Introduction à Django',
    slug    = 'intro-django',
    content = 'Django est un framework web Python...',
    author  = user,           # Instance User
    category = cat,
    status  = 'published',
)

# ─── Lire ─────────────────────────────────────────────────────────────────────
# Tous les articles
articles = Article.objects.all()

# Filtrer (WHERE)
published = Article.objects.filter(status='published')
drafts    = Article.objects.filter(status='draft')

# Filtres avancés
recent    = Article.objects.filter(created_at__gte='2025-01-01')
by_author = Article.objects.filter(author__username='alice')

# Objet unique (lève DoesNotExist ou MultipleObjectsReturned)
article = Article.objects.get(slug='intro-django')

# Eviter les exceptions avec get_or_404 dans les vues :
# from django.shortcuts import get_object_or_404
# article = get_object_or_404(Article, slug=slug)

# Trier et limiter
top5 = Article.objects.order_by('-created_at')[:5]

# Exclure
non_draft = Article.objects.exclude(status='draft')

# ─── Modifier ─────────────────────────────────────────────────────────────────
article.title = 'Introduction à Django 5'
article.save()

# Mise à jour en masse (1 seule requête SQL)
Article.objects.filter(status='draft').update(status='published')

# ─── Supprimer ────────────────────────────────────────────────────────────────
Article.objects.filter(status='draft').delete()

# ─── Relations ────────────────────────────────────────────────────────────────
# ForeignKey : articles d'un auteur (related_name='articles')
articles_alice = user.articles.all()

# ManyToMany : tags d'un article
article.tags.add(tag1, tag2)
article.tags.all()
article.tags.remove(tag1)

# select_related (JOIN SQL → évite N+1 problem)
articles = Article.objects.select_related('author', 'category').all()

# prefetch_related (ManyToMany)
articles = Article.objects.prefetch_related('tags').all()
```

<br>

---

## 5. Vues (Views)

```python title="Python — blog/views.py : vues fonctionnelles et génériques"
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Article

# ─── Vue fonctionnelle (function-based view) ───────────────────────────────────
def article_list(request):
    """Liste des articles publiés."""
    articles = Article.objects.filter(status='published').select_related('author', 'category')
    return render(request, 'blog/article_list.html', {'articles': articles})


def article_detail(request, slug: str):
    """Détail d'un article."""
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'blog/article_detail.html', {'article': article})


# ─── Vues génériques (class-based views) ──────────────────────────────────────
class ArticleListView(ListView):
    """Vue générique : liste paginée."""
    model               = Article
    template_name       = 'blog/article_list.html'
    context_object_name = 'articles'
    paginate_by         = 10

    def get_queryset(self):
        return Article.objects.filter(status='published').select_related('author')


class ArticleDetailView(DetailView):
    """Vue générique : détail."""
    model               = Article
    template_name       = 'blog/article_detail.html'
    context_object_name = 'article'
    slug_field          = 'slug'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Vue générique : création (nécessite connexion)."""
    model         = Article
    fields        = ['title', 'slug', 'content', 'category', 'tags', 'status']
    template_name = 'blog/article_form.html'
    success_url   = reverse_lazy('blog:article_list')

    def form_valid(self, form):
        form.instance.author = self.request.user   # Assigner l'auteur courant
        return super().form_valid(form)
```

<br>

---

## 6. URLs

```python title="Python — blog/urls.py : routes de l'application"
from django.urls import path
from . import views

app_name = 'blog'   # Namespace pour {% url 'blog:article_list' %}

urlpatterns = [
    path('',              views.ArticleListView.as_view(),   name='article_list'),
    path('<slug:slug>/',  views.ArticleDetailView.as_view(), name='article_detail'),
    path('creer/',        views.ArticleCreateView.as_view(), name='article_create'),
]
```

```python title="Python — monprojet/urls.py : inclure les routes de blog"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',  admin.site.urls),
    path('blog/',   include('blog.urls', namespace='blog')),
]
```

<br>

---

## 7. Templates

```html title="HTML — templates/blog/article_list.html : liste des articles"
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Blog Django</title>
</head>
<body>

<h1>Articles</h1>

{% for article in articles %}
    <article>
        <h2>
            <a href="{% url 'blog:article_detail' article.slug %}">
                {{ article.title }}
            </a>
        </h2>
        <p>Par {{ article.author.get_full_name }} — {{ article.created_at|date:"d/m/Y" }}</p>
        <p>{{ article.content|truncatewords:30 }}</p>
    </article>
{% empty %}
    <p>Aucun article publié pour le moment.</p>
{% endfor %}

{# Pagination #}
{% if page_obj.has_other_pages %}
<nav>
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">← Précédent</a>
    {% endif %}
    <span>Page {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Suivant →</a>
    {% endif %}
</nav>
{% endif %}

</body>
</html>
```

_Les **filtres de template** Django (`|date`, `|truncatewords`, `|upper`) transforment les valeurs directement dans le HTML sans logique dans la vue._

<br>

---

## 8. Admin Django

```python title="Python — blog/admin.py : déclarer les modèles dans l'admin"
from django.contrib import admin
from .models import Article, Category, Tag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display    = ['title', 'author', 'status', 'created_at']
    list_filter     = ['status', 'created_at', 'category']
    search_fields   = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}  # Auto-génère le slug depuis le titre
    date_hierarchy  = 'created_at'
    ordering        = ['-created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag)
```

```bash title="Bash — Créer un superutilisateur et accéder à l'admin"
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: ****

# Accéder à l'interface admin : http://127.0.0.1:8000/admin/
```

<br>

---

## Exercices

!!! note "À vous de jouer"

**Exercice 1 — Blog complet**

```python title="Python — Exercice 1 : construire un blog de zéro"
# 1. Créer un projet Django "myblog" avec une app "articles"
# 2. Modèle Article (title, content, published_at, author)
# 3. Modèle Comment (article ForeignKey, author str, content, created_at)
# 4. Vues : liste articles, détail article, ajout commentaire (POST)
# 5. Templates Jinja2 avec héritage (base.html → article_list.html)
# 6. Admin : afficher les commentaires dans l'article (inline admin)
# 7. Pagination : 5 articles par page
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Django suit **MVT** : Model (données ORM), View (traitement requête), Template (présentation HTML). Les **migrations** versionne le schéma de base de données. Le **QuerySet API** génère du SQL optimisé depuis Python. Les **vues génériques** (ListView, DetailView, CreateView) réduisent drastiquement le code répétitif. L'**admin Django** est auto-généré depuis les modèles — un gain de temps considérable pour les backoffices.

> Module suivant : [Admin & Authentification →](./02-admin-et-authentification.md) — gestion des utilisateurs, permissions et groupes.

<br>
