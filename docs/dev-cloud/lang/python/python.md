---
description: "Python Core 01 — Fondamentaux du langage : types, variables, structures de contrôle, fonctions, OOP, exceptions et modules."
icon: lucide/book-open-check
tags: ["PYTHON", "FONDAMENTAUX", "OOP", "EXCEPTIONS", "FONCTIONS", "TYPES"]
---

# Python

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Python 3.12+"
  data-time="4 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — La Grammaire avant la Littérature"
    Avant d'écrire un roman, il faut maîtriser la grammaire : les noms (variables), les verbes (fonctions), la ponctuation (syntaxe). Python est une langue avec une grammaire particulièrement claire — pas de point-virgule obligatoire, l'indentation **est** la structure. Ce module est votre cours de grammaire Python : une fois ces bases maîtrisées, Django, Flask et toutes les bibliothèques deviennent accessibles.

<br>

---

## 1. Types & Variables

```python title="Python — Types de base et annotations de type"
# ─── Types primitifs ──────────────────────────────────────────────────────────
nom:    str   = "Alice"
age:    int   = 30
taille: float = 1.75
actif:  bool  = True

# ─── Inférence (Python devine le type) ───────────────────────────────────────
ville = "Paris"       # str
score = 42            # int
ratio = 3.14          # float

# ─── None (absence de valeur) ────────────────────────────────────────────────
resultat: str | None = None    # Union type Python 3.10+

# ─── Chaînes de caractères ───────────────────────────────────────────────────
prenom  = "Alice"
message = f"Bonjour, {prenom} ! Tu as {age} ans."   # f-string (recommandé)
multi   = """Texte
sur plusieurs
lignes."""

# Méthodes utiles
print("  hello  ".strip())          # "hello"
print("hello world".split())        # ["hello", "world"]
print("MAJUSCLE".lower())           # "majuscle"
print("Alice".startswith("A"))      # True
print(", ".join(["a", "b", "c"]))  # "a, b, c"

# ─── Nombres ─────────────────────────────────────────────────────────────────
print(10 // 3)     # 3     (division entière)
print(10 % 3)      # 1     (modulo)
print(2 ** 8)      # 256   (puissance)
print(round(3.14159, 2))  # 3.14
```

```python title="Python — Collections : list, dict, tuple, set"
# ─── LIST (ordonnée, mutable) ─────────────────────────────────────────────────
fruits = ["pomme", "banane", "orange"]
fruits.append("kiwi")          # Ajouter en fin
fruits.insert(0, "fraise")     # Insérer à l'index 0
fruits.remove("banane")        # Supprimer par valeur
popped = fruits.pop()          # Retirer le dernier élément
print(fruits[0])               # Premier élément
print(fruits[-1])              # Dernier élément
print(fruits[1:3])             # Slice (index 1 et 2)
print(len(fruits))             # Longueur

# List comprehension (expression compacte)
carrés = [x ** 2 for x in range(1, 6)]         # [1, 4, 9, 16, 25]
pairs   = [x for x in range(10) if x % 2 == 0] # [0, 2, 4, 6, 8]

# ─── DICT (clé-valeur, ordonné Python 3.7+) ──────────────────────────────────
utilisateur = {
    "nom":   "Alice",
    "age":   30,
    "roles": ["admin", "editor"],
}

print(utilisateur["nom"])               # "Alice"
print(utilisateur.get("email", "N/A")) # "N/A" (sans KeyError)
utilisateur["email"] = "alice@example.com"  # Ajout
del utilisateur["age"]                  # Suppression

for cle, valeur in utilisateur.items():
    print(f"{cle}: {valeur}")

# Dict comprehension
doubles = {k: v * 2 for k, v in {"a": 1, "b": 2}.items()}  # {"a": 2, "b": 4}

# ─── TUPLE (ordonné, immuable) ────────────────────────────────────────────────
coordonnees = (48.8566, 2.3522)   # (lat, lng)
lat, lng    = coordonnees          # Déstructuration
point = (1,)                       # Tuple à 1 élément — virgule obligatoire

# ─── SET (non ordonné, unique) ────────────────────────────────────────────────
tags = {"python", "web", "python"}  # {"python", "web"} — doublons supprimés
tags.add("django")
tags.discard("web")
print("python" in tags)             # True
intersection = {1, 2, 3} & {2, 3, 4}   # {2, 3}
```

<br>

---

## 2. Structures de Contrôle

```python title="Python — if/elif/else, for, while, match"
# ─── Conditions ──────────────────────────────────────────────────────────────
age = 20

if age >= 18:
    print("Majeur")
elif age >= 15:
    print("Adolescent")
else:
    print("Enfant")

# Ternaire
statut = "majeur" if age >= 18 else "mineur"

# ─── Boucle for ──────────────────────────────────────────────────────────────
fruits = ["pomme", "banane", "kiwi"]

for fruit in fruits:
    print(fruit)

# Avec index : enumerate
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")

# Itérer sur un dict
config = {"host": "localhost", "port": 5432}
for cle, valeur in config.items():
    print(f"{cle} = {valeur}")

# range
for i in range(5):          # 0 à 4
    print(i)

for i in range(0, 10, 2):  # 0, 2, 4, 6, 8 (step=2)
    print(i)

# ─── Boucle while ─────────────────────────────────────────────────────────────
compteur = 0
while compteur < 5:
    print(compteur)
    compteur += 1

# break, continue
for i in range(10):
    if i == 3: continue    # Sauter l'itération
    if i == 7: break       # Arrêter la boucle
    print(i)

# ─── match/case (Python 3.10+) ────────────────────────────────────────────────
commande = "quit"

match commande:
    case "start":  print("Démarrage...")
    case "stop":   print("Arrêt...")
    case "quit":   print("Au revoir !")
    case _:        print(f"Commande inconnue : {commande}")
```

<br>

---

## 3. Fonctions

```python title="Python — Fonctions : paramètres, *args, **kwargs, décorateurs"
# ─── Définition de base ──────────────────────────────────────────────────────
def saluer(nom: str, titre: str = "M.") -> str:
    """Retourne une salutation formelle."""
    return f"Bonjour, {titre} {nom} !"

print(saluer("Dupont"))          # "Bonjour, M. Dupont !"
print(saluer("Martin", "Dr"))   # "Bonjour, Dr Martin !"

# ─── *args (arguments positionnels variables) ─────────────────────────────────
def somme(*nombres: int) -> int:
    return sum(nombres)

print(somme(1, 2, 3, 4, 5))   # 15

# ─── **kwargs (arguments nommés variables) ────────────────────────────────────
def afficher(**infos: str) -> None:
    for cle, valeur in infos.items():
        print(f"{cle}: {valeur}")

afficher(nom="Alice", role="admin", ville="Paris")

# ─── Fonctions lambda (anonymes) ──────────────────────────────────────────────
doubler = lambda x: x * 2
print(doubler(5))   # 10

nombres = [3, 1, 4, 1, 5, 9]
tries   = sorted(nombres, key=lambda x: -x)   # Tri décroissant

# ─── Fonctions d'ordre supérieur ──────────────────────────────────────────────
noms    = ["alice", "bob", "charlie"]
majusc  = list(map(str.capitalize, noms))        # ["Alice", "Bob", "Charlie"]
longs   = list(filter(lambda n: len(n) > 3, noms))  # ["alice", "charlie"]

# ─── Décorateurs ─────────────────────────────────────────────────────────────
import functools
import time

def chronometre(func):
    @functools.wraps(func)    # Préserve le nom et la docstring de la fonction
    def wrapper(*args, **kwargs):
        debut = time.monotonic()
        resultat = func(*args, **kwargs)
        duree = time.monotonic() - debut
        print(f"{func.__name__} a pris {duree:.4f}s")
        return resultat
    return wrapper

@chronometre
def calcul_lent(n: int) -> int:
    return sum(range(n))

# ─── Générateurs ─────────────────────────────────────────────────────────────
def fibonacci(n: int):
    """Générateur infini de Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(list(fibonacci(10)))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

<br>

---

## 4. Programmation Orientée Objet

```python title="Python — Classes : encapsulation, héritage, méthodes spéciales"
from dataclasses import dataclass, field
from typing import ClassVar

class Animal:
    """Classe de base."""

    # Variable de classe (partagée par toutes les instances)
    especes_connues: ClassVar[list[str]] = []

    def __init__(self, nom: str, age: int) -> None:
        self.nom  = nom    # Attribut public
        self._age = age    # Attribut protégé (convention)
        Animal.especes_connues.append(self.__class__.__name__)

    # Propriété (getter encapsulé)
    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, valeur: int) -> None:
        if valeur < 0:
            raise ValueError("L'âge ne peut pas être négatif")
        self._age = valeur

    # Méthodes spéciales (dunder)
    def __str__(self) -> str:
        return f"{self.nom} ({self._age} ans)"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(nom={self.nom!r}, age={self._age})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Animal):
            return NotImplemented
        return self.nom == other.nom and self._age == other._age

    # Méthode d'instance
    def parler(self) -> str:
        return "..."

    # Méthode de classe (factory)
    @classmethod
    def depuis_dict(cls, data: dict) -> "Animal":
        return cls(data["nom"], data["age"])

    # Méthode statique (utilitaire)
    @staticmethod
    def valider_age(age: int) -> bool:
        return 0 <= age <= 150


class Chien(Animal):
    """Héritage et spécialisation."""

    def __init__(self, nom: str, age: int, race: str) -> None:
        super().__init__(nom, age)   # Appel du constructeur parent
        self.race = race

    def parler(self) -> str:
        return "Ouaf !"

    def __str__(self) -> str:
        return f"{super().__str__()} — Race: {self.race}"


# ─── Dataclass (alternative moderne, Python 3.7+) ──────────────────────────────
@dataclass
class Point:
    x: float
    y: float
    label: str = ""
    tags: list[str] = field(default_factory=list)   # Valeur par défaut mutable

    def distance(self, autre: "Point") -> float:
        return ((self.x - autre.x)**2 + (self.y - autre.y)**2) ** 0.5

p1 = Point(0, 0, "Origine")
p2 = Point(3, 4)
print(p1.distance(p2))   # 5.0
```

<br>

---

## 5. Gestion des Erreurs

```python title="Python — Exceptions : try/except/else/finally, exceptions custom"
# ─── try / except / else / finally ───────────────────────────────────────────
def diviser(a: float, b: float) -> float:
    try:
        resultat = a / b
    except ZeroDivisionError:
        print("Division par zéro !")
        return 0.0
    except TypeError as e:
        print(f"Type invalide : {e}")
        raise                  # Re-lève l'exception
    else:
        # Exécuté seulement si aucune exception
        print(f"Succès : {a} / {b} = {resultat}")
        return resultat
    finally:
        # TOUJOURS exécuté (même si exception)
        print("Calcul terminé.")

# ─── Capturer plusieurs exceptions ───────────────────────────────────────────
try:
    data = int(input("Entrez un nombre : "))
except (ValueError, EOFError) as e:
    print(f"Saisie invalide : {e}")

# ─── Exceptions personnalisées ────────────────────────────────────────────────
class AppError(Exception):
    """Classe de base pour les erreurs de l'application."""
    def __init__(self, message: str, code: int = 400) -> None:
        super().__init__(message)
        self.code = code

class ValidationError(AppError):
    """Erreur de validation des données."""
    def __init__(self, champ: str, message: str) -> None:
        super().__init__(f"Validation échouée sur '{champ}': {message}", code=422)
        self.champ = champ

class NotFoundError(AppError):
    """Ressource introuvable."""
    def __init__(self, ressource: str, id: int) -> None:
        super().__init__(f"{ressource} #{id} introuvable", code=404)

# Utilisation
try:
    raise ValidationError("email", "format invalide")
except ValidationError as e:
    print(f"[{e.code}] {e}")       # [422] Validation échouée sur 'email': format invalide
    print(f"Champ : {e.champ}")   # email
except AppError as e:
    print(f"[{e.code}] {e}")

# ─── Context Manager (with) ──────────────────────────────────────────────────
# Garantit la fermeture des ressources même en cas d'exception
with open("fichier.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
# f est automatiquement fermé ici
```

<br>

---

## 6. Modules & Imports

```python title="Python — Organiser son code en modules et packages"
# ─── Imports standards ────────────────────────────────────────────────────────
import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Optional, Union, Any

# ─── Import depuis son propre package ────────────────────────────────────────
# Structure recommandée :
# mon_projet/
# ├── __init__.py
# ├── models/
# │   ├── __init__.py
# │   └── article.py
# └── services/
#     ├── __init__.py
#     └── email.py

from mon_projet.models.article import Article
from mon_projet.services import email

# ─── Pathlib (chemins de fichiers) ────────────────────────────────────────────
base = Path(__file__).parent        # Dossier du fichier courant
config = base / "config" / "app.json"

if config.exists():
    with config.open("r") as f:
        data = json.load(f)

# Lister les fichiers Python d'un dossier
fichiers_py = list(base.glob("**/*.py"))

# ─── Variables d'environnement ────────────────────────────────────────────────
import os
from dotenv import load_dotenv   # pip install python-dotenv

load_dotenv()   # Charge le fichier .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
SECRET_KEY   = os.environ["SECRET_KEY"]   # Lève KeyError si absent

# ─── __name__ == "__main__" ───────────────────────────────────────────────────
# Permet d'exécuter du code seulement si le fichier est lancé directement
# (pas importé comme module)
if __name__ == "__main__":
    print("Lancement du script...")
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Python repose sur 6 piliers : les **types** (str, int, float, bool, None et les collections list/dict/tuple/set), les **structures de contrôle** (if/elif/else, for, while, match), les **fonctions** (paramètres nommés, *args/**kwargs, décorateurs, générateurs), la **POO** (classes, héritage, propriétés, dataclasses), la **gestion des erreurs** (try/except/else/finally, exceptions custom) et les **modules** (imports, pathlib, dotenv). Ces fondamentaux sont communs à tous les frameworks : maîtrisez-les avant Django ou Flask.

> Modules suivants : [Django →](../django/index.md) · [Flask →](../flask/index.md) · [Tkinter →](../tkinter/index.md)

<br>
