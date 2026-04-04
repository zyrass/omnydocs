---
description: "Django 02 — Authentification : système auth Django, AbstractUser, vues LoginView/LogoutView, décorateur login_required, groupes et permissions."
icon: lucide/book-open-check
tags: ["DJANGO", "PYTHON", "AUTH", "ABSTRACTUSER", "PERMISSIONS", "GROUPES"]
---

# Module 02 — Authentification Django

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="Django 5.x / Python 3.11+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Carte d'Accès d'un Bâtiment"
    Dans un grand bâtiment, tout le monde passe par l'accueil pour obtenir son badge. Ce badge détermine quelles portes vous pouvez ouvrir : un visiteur accède au hall, un employé à son bureau, un directeur à la salle des serveurs. Django Auth fonctionne pareil : `LoginView` est l'accueil, le badge est la session, et les **permissions** sont les portes. La beauté du système Django : tout ceci est fourni prêt à l'emploi.

<br>

---

## 1. Le Système d'Authentification Django

```
django.contrib.auth fournit out-of-the-box :
├── User model            → Modèle utilisateur avec username/email/password
├── LoginView             → Vue de connexion (formulaire + session)
├── LogoutView            → Vue de déconnexion
├── PasswordChangeView    → Changement de mot de passe
├── PasswordResetView     → Réinitialisation par email
├── login_required        → Décorateur de protection des vues
├── Permission system     → Permissions par modèle (add/change/delete/view)
└── Groups                → Rôles (groupes de permissions)
```

```python title="Python — settings.py : configuration de l'authentification"
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',          # ← Le module auth
    'django.contrib.contenttypes',  # ← Requis par auth
    'django.contrib.sessions',      # ← Requis pour les sessions
    # ...
    'accounts',                     # Notre app d'authentification
]

# URL de redirection après connexion (défaut : /accounts/profile/)
LOGIN_REDIRECT_URL  = '/dashboard/'

# URL de redirection après déconnexion (défaut : None)
LOGOUT_REDIRECT_URL = '/login/'

# URL de la page de connexion (utilisée par login_required)
LOGIN_URL = '/login/'

# Modèle utilisateur personnalisé (DOIT être défini avant la première migration)
AUTH_USER_MODEL = 'accounts.CustomUser'
```

<br>

---

## 2. Modèle Utilisateur Personnalisé (AbstractUser)

!!! warning "À faire avant la première migration"
    La définition d'un `AUTH_USER_MODEL` personnalisé doit impérativement être faite **avant** de lancer `python manage.py migrate` pour la première fois. Si vous l'ajoutez après, vous devrez supprimer la base de données et recommencer.

```python title="Python — accounts/models.py : étendre le modèle User"
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé.
    AbstractUser conserve tous les champs Django par défaut :
    username, first_name, last_name, email, password,
    is_staff, is_active, is_superuser, date_joined, last_login.
    """

    # Champs supplémentaires
    bio          = models.TextField(blank=True)
    avatar       = models.ImageField(upload_to='avatars/', blank=True, null=True)
    organisation = models.CharField(max_length=100, blank=True)

    # Unicité de l'email (non imposé par défaut dans AbstractUser)
    email = models.EmailField(unique=True)

    # Champ "username" en login alternatif : utiliser l'email
    USERNAME_FIELD  = 'email'   # Connexion par email
    REQUIRED_FIELDS = ['username']  # Requis pour createsuperuser

    class Meta:
        verbose_name        = 'utilisateur'
        verbose_name_plural = 'utilisateurs'

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.username
```

```bash title="Bash — Générer et appliquer les migrations du modèle custom"
# Créer l'application accounts
python manage.py startapp accounts

# Générer les migrations (après avoir défini AUTH_USER_MODEL dans settings.py)
python manage.py makemigrations accounts
python manage.py migrate

# Créer un superuser (utilise EMAIL comme identifiant si USERNAME_FIELD='email')
python manage.py createsuperuser
```

```python title="Python — accounts/admin.py : enregistrer CustomUser dans l'admin"
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Ajouter les nouveaux champs aux sections de l'admin
    fieldsets = UserAdmin.fieldsets + (
        ('Profil', {
            'fields': ('bio', 'avatar', 'organisation'),
        }),
    )

    # Champs affichés dans la liste
    list_display = ['email', 'username', 'organisation', 'is_staff', 'is_active']
    list_filter  = ['is_staff', 'is_active', 'organisation']
    search_fields = ['email', 'username', 'organisation']
```

<br>

---

## 3. Vues d'Authentification

```python title="Python — accounts/urls.py : routing des vues d'authentification"
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # ─── Connexion / Déconnexion (vues génériques Django) ─────────────────────
    path('login/',
         auth_views.LoginView.as_view(template_name='accounts/login.html'),
         name='login'),

    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),

    # ─── Inscription (vue custom) ─────────────────────────────────────────────
    path('register/', views.RegisterView.as_view(), name='register'),

    # ─── Profil (protégé) ─────────────────────────────────────────────────────
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # ─── Changement de mot de passe (vues génériques Django) ──────────────────
    path('password/change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url='/accounts/profile/'
         ),
         name='password_change'),

    # ─── Réinitialisation de mot de passe (flux complet) ──────────────────────
    path('password/reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/emails/password_reset.txt',
         ),
         name='password_reset'),

    path('password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
```

```python title="Python — accounts/views.py : inscription et profil"
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import CustomUser


class RegisterView(CreateView):
    """Inscription d'un nouvel utilisateur."""
    model         = CustomUser
    form_class    = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url   = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Connecter l'utilisateur directement après l'inscription
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, UpdateView):
    """Page de profil — protégée par login."""
    model         = CustomUser
    form_class    = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url   = reverse_lazy('accounts:profile')

    def get_object(self):
        # L'utilisateur ne peut modifier que SON profil
        return self.request.user
```

```python title="Python — accounts/forms.py : formulaires d'inscription et de profil"
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Formulaire d'inscription avec email."""
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model  = CustomUser
        fields = ['email', 'username', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour du profil."""
    class Meta:
        model  = CustomUser
        fields = ['first_name', 'last_name', 'bio', 'avatar', 'organisation']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
```

<br>

---

## 4. Protéger les Vues

```python title="Python — Protéger les vues avec login_required et LoginRequiredMixin"
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render

# ─── Fonction-based view : @login_required ────────────────────────────────────
@login_required
def tableau_de_bord(request):
    """Accès réservé aux utilisateurs connectés."""
    return render(request, 'dashboard/index.html', {
        'user': request.user,
    })

# ─── Avec permission requise ──────────────────────────────────────────────────
@login_required
@permission_required('blog.add_article', raise_exception=True)
def creer_article(request):
    """Requiert la permission blog.add_article."""
    ...

# ─── Class-based view : LoginRequiredMixin ────────────────────────────────────
class MonProfilView(LoginRequiredMixin, UpdateView):
    login_url    = '/login/'    # Surcharger l'URL de redirection si besoin
    redirect_field_name = 'next'
    ...

# ─── PermissionRequiredMixin ──────────────────────────────────────────────────
class PublierArticleView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_article'
    raise_exception     = True   # 403 au lieu de redirection vers login
    ...

# ─── Vérifications dans les templates ────────────────────────────────────────
# {% if user.is_authenticated %}
#     Bonjour, {{ user.full_name }} !
# {% endif %}
#
# {% if user.has_perm('blog.add_article') %}
#     <a href="{% url 'blog:article_create' %}">Nouvel article</a>
# {% endif %}
```

<br>

---

## 5. Permissions & Groupes

```python title="Python — Gestion des permissions et des groupes"
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser

# ─── Permissions auto-générées par Django pour chaque modèle ──────────────────
# Pour le modèle Article, Django crée automatiquement :
# blog.add_article    → Peut créer un article
# blog.change_article → Peut modifier un article
# blog.delete_article → Peut supprimer un article
# blog.view_article   → Peut voir un article

# ─── Permissions personnalisées (dans Meta du modèle) ────────────────────────
# class Article(models.Model):
#     class Meta:
#         permissions = [
#             ("publish_article",  "Peut publier un article"),
#             ("moderate_article", "Peut modérer les commentaires"),
#         ]

# ─── Assigner des permissions à un utilisateur ────────────────────────────────
user = CustomUser.objects.get(email='alice@example.com')

# Récupérer une permission
perm_publish = Permission.objects.get(codename='publish_article')

# Assigner / Retirer
user.user_permissions.add(perm_publish)
user.user_permissions.remove(perm_publish)

# Vérifier
user.has_perm('blog.publish_article')   # True / False
user.has_perms(['blog.add_article', 'blog.change_article'])

# ─── Groupes (rôles) ──────────────────────────────────────────────────────────
# Créer un groupe "Rédacteurs"
redacteurs, _ = Group.objects.get_or_create(name='Rédacteurs')

# Ajouter des permissions au groupe
redacteurs.permissions.add(
    Permission.objects.get(codename='add_article'),
    Permission.objects.get(codename='change_article'),
    Permission.objects.get(codename='publish_article'),
)

# Assigner l'utilisateur au groupe
user.groups.add(redacteurs)

# L'utilisateur hérite de toutes les permissions du groupe
user.has_perm('blog.publish_article')  # True (via le groupe)

# ─── Créer les groupes via une migration de données ──────────────────────────
# management/commands/seed_groups.py
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Crée les groupes et permissions par défaut'

    def handle(self, *args, **kwargs):
        roles = {
            'Lecteurs':    [],
            'Rédacteurs':  ['add_article', 'change_article', 'publish_article'],
            'Modérateurs': ['add_article', 'change_article', 'delete_article', 'publish_article'],
        }
        for nom, perms in roles.items():
            groupe, created = Group.objects.get_or_create(name=nom)
            for codename in perms:
                perm = Permission.objects.get(codename=codename)
                groupe.permissions.add(perm)
            status = "créé" if created else "existant"
            self.stdout.write(f"Groupe '{nom}' : {status}")
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Django Auth est **prêt à l'emploi** : `LoginView`, `LogoutView`, `PasswordResetView` et leurs templates suffisent pour un MVP. Définissez **toujours** un `CustomUser` (via `AbstractUser`) dès le départ — l'ajouter après la première migration est douloureux. Protégez les vues avec `@login_required` (FBV) ou `LoginRequiredMixin` (CBV). Les **permissions** (`has_perm`) et les **groupes** permettent un RBAC simple sans dépendance externe. Pour un RBAC avancé, `django-guardian` ajoute des permissions par objet.

> Module suivant : [Django REST Framework →](./03-drf.md) — Sérializers, ViewSets, Router, authentification JWT.

<br>
