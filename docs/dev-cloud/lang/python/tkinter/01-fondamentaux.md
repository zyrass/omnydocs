---
description: "Tkinter 01 — Fondamentaux : fenêtre principale, widgets essentiels, géométrie (pack/grid), événements et Canvas."
icon: lucide/book-open-check
tags: ["TKINTER", "PYTHON", "GUI", "WIDGETS", "CANVAS", "EVENTS"]
---

# Fondamentaux

<div
  class="omny-meta"
  data-level="🟢 Débutant"
  data-version="Tkinter (Python 3.11+)"
  data-time="3 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Tableau d'Affichage"
    Imaginez un tableau d'affichage en liège. La fenêtre Tkinter (`Tk()`) est le cadre du tableau. Les widgets (boutons, labels, champs texte) sont les feuilles que vous épinglez. Les gestionnaires de layout (pack, grid) décident où vous placez chaque feuille. Les événements (`command`, `bind`) sont les réactions quand quelqu'un interagit avec vos feuilles — comme retirer ou déplacer une épingle.

**Tkinter** est inclus dans la bibliothèque standard Python — aucune installation supplémentaire. Une application Tkinter s'articule autour de trois concepts :

| Concept | Description |
|---|---|
| **Widget** | Élément graphique (Button, Label, Entry, Canvas...) |
| **Géométrie** | Position des widgets (pack, grid, place) |
| **Événement** | Réaction aux actions utilisateur (clic, touche, survol) |

<br>

---

## 1. Fenêtre de Base

```python title="Python — Application Tkinter minimale"
import tkinter as tk
from tkinter import ttk  # Widgets thémés (style plus moderne)

# ─── Fenêtre principale ────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Mon Application")
root.geometry("800x600")      # Largeur x Hauteur
root.minsize(400, 300)         # Taille minimale
root.resizable(True, True)     # Redimensionnable (True/True)

# ─── Style ttk ────────────────────────────────────────────────────────────────
style = ttk.Style()
style.theme_use('clam')        # Thèmes : 'clam', 'alt', 'default', 'classic'

# ─── Boucle principale ────────────────────────────────────────────────────────
# NE JAMAIS oublier mainloop() — c'est la boucle événementielle
root.mainloop()
```

<br>

---

## 2. Widgets Essentiels

```python title="Python — Widgets de base : Label, Button, Entry, Text"
import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("Widgets Essentiels")

# ─── Label ────────────────────────────────────────────────────────────────────
label = ttk.Label(
    root,
    text  = "Bonjour, Tkinter !",
    font  = ('Helvetica', 14, 'bold'),
)

# ─── Button ───────────────────────────────────────────────────────────────────
def on_click():
    messagebox.showinfo("Action", "Bouton cliqué !")

btn = ttk.Button(root, text="Cliquer", command=on_click)

# ─── Entry (champ texte une ligne) ────────────────────────────────────────────
nom_var = tk.StringVar()    # Variable liée (lecture/écriture réactives)
entry   = ttk.Entry(root, textvariable=nom_var, width=30)

def afficher_nom():
    nom = nom_var.get()
    label.config(text=f"Bonjour, {nom} !")

btn_nom = ttk.Button(root, text="Valider", command=afficher_nom)

# ─── Text (zone de texte multi-lignes) ────────────────────────────────────────
text_zone = tk.Text(root, width=50, height=10, wrap=tk.WORD)
# Lire le contenu :  text_zone.get("1.0", tk.END)
# Insérer du texte :  text_zone.insert(tk.END, "Hello")
# Vider :  text_zone.delete("1.0", tk.END)

# ─── Combobox (liste déroulante) ──────────────────────────────────────────────
choix_var = tk.StringVar()
combo = ttk.Combobox(root, textvariable=choix_var, values=['Python', 'JavaScript', 'PHP'])
combo.current(0)   # Sélectionner le premier élément

# ─── Checkbutton ──────────────────────────────────────────────────────────────
actif_var = tk.BooleanVar()
check = ttk.Checkbutton(root, text="Activer la fonctionnalité", variable=actif_var)

# ─── Radiobutton ──────────────────────────────────────────────────────────────
theme_var = tk.StringVar(value='clair')
radio_clair = ttk.Radiobutton(root, text="Thème clair", variable=theme_var, value='clair')
radio_sombre = ttk.Radiobutton(root, text="Thème sombre", variable=theme_var, value='sombre')

# ─── Placement ────────────────────────────────────────────────────────────────
label.pack(pady=10)
entry.pack(pady=5)
btn_nom.pack(pady=5)
btn.pack(pady=5)
text_zone.pack(pady=10)
combo.pack(pady=5)
check.pack(pady=5)
radio_clair.pack()
radio_sombre.pack()

root.mainloop()
```

<br>

---

## 3. Géométrie : pack, grid, place

```python title="Python — pack : disposition linéaire"
# pack : empile les widgets verticalement ou horizontalement
label.pack(side=tk.TOP,    fill=tk.X,    pady=5)   # Étire horizontalement
btn.pack(  side=tk.BOTTOM, anchor=tk.W,  padx=10)  # Aligné à gauche en bas
frame.pack(side=tk.LEFT,   fill=tk.BOTH, expand=True)  # Prend tout l'espace
```

```python title="Python — grid : disposition en tableau (recommandé)"
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Formulaire de Connexion")

# grid : position par ligne/colonne
ttk.Label(root, text="Nom d'utilisateur :").grid(row=0, column=0, sticky='e', padx=5, pady=5)
ttk.Label(root, text="Mot de passe :").grid(    row=1, column=0, sticky='e', padx=5, pady=5)

user_entry = ttk.Entry(root, width=25)
pass_entry = ttk.Entry(root, width=25, show='*')   # show='*' masque le texte

user_entry.grid(row=0, column=1, padx=5, pady=5)
pass_entry.grid(row=1, column=1, padx=5, pady=5)

# columnspan : un widget sur plusieurs colonnes
ttk.Button(root, text="Connexion").grid(row=2, column=0, columnspan=2, pady=10)

# Configurer le poids des colonnes (redimensionnement)
root.columnconfigure(1, weight=1)

root.mainloop()
```

_`sticky` fonctionne comme les ancres CSS : `'n'` (haut), `'s'` (bas), `'e'` (droite), `'w'` (gauche), `'nsew'` (étire dans toutes les directions)._

<br>

---

## 4. Événements

```python title="Python — Événements : command, bind(), protocoles"
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# ─── command= : événement simple (clic bouton) ────────────────────────────────
def on_btn_click():
    print("Bouton cliqué")

btn = ttk.Button(root, text="Cliquer", command=on_btn_click)
btn.pack()

# ─── bind() : événements clavier et souris ────────────────────────────────────
entry = ttk.Entry(root)
entry.pack()

def on_key_press(event):
    print(f"Touche pressée : {event.char} (keysym: {event.keysym})")

def on_enter_key(event):
    print(f"Entrée validée : {entry.get()}")

def on_mouse_click(event):
    print(f"Clic souris à ({event.x}, {event.y})")

entry.bind('<Key>',      on_key_press)      # Toute touche
entry.bind('<Return>',   on_enter_key)      # Touche Entrée
root.bind('<Button-1>',  on_mouse_click)    # Clic gauche souris
root.bind('<Control-s>', lambda e: print("Ctrl+S pressé"))

# ─── Protocole fermeture fenêtre ──────────────────────────────────────────────
def on_close():
    from tkinter import messagebox
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
```

<br>

---

## 5. Canvas — Dessin & Graphiques

```python title="Python — Canvas : dessiner des formes et animer"
import tkinter as tk
import math

root = tk.Tk()
root.title("Canvas — Dessin")

canvas = tk.Canvas(root, width=600, height=400, bg='white')
canvas.pack()

# ─── Formes de base ───────────────────────────────────────────────────────────
# Rectangle
rect_id = canvas.create_rectangle(50, 50, 200, 150,
    fill='lightblue', outline='navy', width=2)

# Ovale / Cercle
canvas.create_oval(250, 50, 400, 200,
    fill='lightgreen', outline='darkgreen')

# Ligne
canvas.create_line(50, 250, 550, 350,
    fill='red', width=3, dash=(10, 5))   # Ligne pointillée

# Texte
canvas.create_text(300, 30,
    text='Dessin Tkinter', font=('Arial', 18, 'bold'), fill='purple')

# Polygone
canvas.create_polygon(450, 50, 500, 150, 400, 150,
    fill='yellow', outline='orange', width=2)

# ─── Animation : déplacer un cercle ───────────────────────────────────────────
ball_id = canvas.create_oval(10, 10, 50, 50, fill='red')
dx, dy  = 3, 2

def animate():
    canvas.move(ball_id, dx, dy)
    pos = canvas.coords(ball_id)

    global dx, dy
    if pos[2] >= 600 or pos[0] <= 0:  dx = -dx   # Rebond horizontal
    if pos[3] >= 400 or pos[1] <= 0:  dy = -dy   # Rebond vertical

    root.after(16, animate)   # ~60 FPS (16ms entre chaque frame)

animate()

# ─── Interactivité : clic pour déplacer un objet ─────────────────────────────
def on_canvas_click(event):
    canvas.coords(rect_id,
        event.x - 75, event.y - 50,
        event.x + 75, event.y + 50)

canvas.bind('<Button-1>', on_canvas_click)

root.mainloop()
```

<br>

---

## 6. Application Complète — Gestionnaire de Tâches

```python title="Python — Application TodoList Tkinter complète"
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TodoApp:
    """Application de gestion de tâches avec Tkinter."""

    def __init__(self, root: tk.Tk):
        self.root  = root
        self.tasks = []

        self._build_ui()

    def _build_ui(self) -> None:
        """Construire l'interface."""
        self.root.title("TodoList Tkinter")
        self.root.geometry("600x500")

        # ─── Zone de saisie ───────────────────────────────────────────────────
        frame_input = ttk.Frame(self.root, padding=10)
        frame_input.pack(fill=tk.X)

        self.task_var = tk.StringVar()
        ttk.Label(frame_input, text="Nouvelle tâche :").pack(side=tk.LEFT)
        ttk.Entry(frame_input, textvariable=self.task_var, width=35).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_input, text="Ajouter", command=self.add_task).pack(side=tk.LEFT)

        # ─── Liste des tâches ─────────────────────────────────────────────────
        frame_list = ttk.Frame(self.root, padding=10)
        frame_list.pack(fill=tk.BOTH, expand=True)

        columns = ('task', 'date', 'done')
        self.tree = ttk.Treeview(frame_list, columns=columns, show='headings')
        self.tree.heading('task', text='Tâche')
        self.tree.heading('date', text='Ajoutée le')
        self.tree.heading('done', text='Statut')
        self.tree.column('done', width=80)

        scrollbar = ttk.Scrollbar(frame_list, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ─── Boutons d'action ─────────────────────────────────────────────────
        frame_actions = ttk.Frame(self.root, padding=10)
        frame_actions.pack(fill=tk.X)

        ttk.Button(frame_actions, text="✅ Terminer", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_actions, text="🗑️ Supprimer", command=self.delete_task).pack(side=tk.LEFT)

    def add_task(self) -> None:
        """Ajouter une tâche à la liste."""
        text = self.task_var.get().strip()
        if not text:
            messagebox.showwarning("Attention", "La tâche ne peut pas être vide.")
            return

        now = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.tree.insert('', tk.END, values=(text, now, '⏳ En cours'))
        self.task_var.set('')    # Vider le champ

    def complete_task(self) -> None:
        """Marquer la tâche sélectionnée comme terminée."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Sélectionnez une tâche.")
            return
        for item in selected:
            values = list(self.tree.item(item, 'values'))
            values[2] = '✅ Terminée'
            self.tree.item(item, values=values)

    def delete_task(self) -> None:
        """Supprimer la tâche sélectionnée."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Sélectionnez une tâche.")
            return
        for item in selected:
            self.tree.delete(item)


if __name__ == '__main__':
    root = tk.Tk()
    app  = TodoApp(root)
    root.mainloop()
```

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Chaque application Tkinter suit le même cycle : créer la fenêtre (`Tk()`), ajouter les **widgets**, les positionner avec **pack/grid**, lier des **événements**, démarrer `mainloop()`. L'architecture **classe** (TodoApp hérite de rien, encapsule `root`) est le pattern recommandé pour les applications non triviales. Le **Canvas** permet animations, graphiques et interfaces personnalisées. Les **variables tk** (`StringVar`, `BooleanVar`, `IntVar`) lient automatiquement widgets et données — c'est le data-binding de Tkinter.

> Tkinter est parfait pour les outils internes et les scripts avec interface. Pour des interfaces plus modernes, explorez **CustomTkinter** (surcouche moderne de Tkinter) ou **PyQt6**.

<br>
