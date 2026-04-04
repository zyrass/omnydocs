---
description: "Traduire un Modèle Physique de Données (MPD) en scripts SQL DDL pour différents SGBD"
icon: lucide/book-open-check
tags: ["MERISE", "MPD", "SQL", "DDL", "SGBD"]
---

# MPD → SQL

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="25-40 minutes">
</div>

## Introduction

Le chapitre précédent a posé les bases du **Modèle Physique de Données (MPD)** :  
tables, types, contraintes, clés primaires et étrangères, nullabilité, index.

Ce module va un cran plus loin : on prend ce MPD et on le **traduit en scripts SQL DDL concrets**, prêts à être exécutés dans différents SGBD :

- **générique** (ANSI SQL)
- **PostgreSQL**
- **MySQL/MariaDB**
- **SQLite 3**

L’idée est simple :

> À partir d’un même **MPD générique**, produire des scripts **CREATE TABLE** adaptés à chaque moteur, tout en conservant la même structure métier.

---

## Rappel : MPD de référence (cas “commandes”)

On repart du MPD générique suivant (défini dans la page **MPD**) :

- `CLIENT(id_client PK, nom, email)`
- `COMMANDE(id_commande PK, date_commande, statut, id_client FK → CLIENT)`
- `PRODUIT(id_produit PK, libelle, prix)`
- `LIGNE_COMMANDE(id_commande FK, id_produit FK, quantite, prix_unitaire, PK = id_commande + id_produit)`

Les types du MPD :

- `id_xxx` : `INTEGER`
- `nom`, `statut`, `lieu`, etc. : `VARCHAR(...)`
- dates : `DATE`
- montants : `NUMERIC(10,2)` ou équivalent (`DECIMAL`, `REAL`…)

Ce module ne redéfinit pas le MPD : il montre **comment le matérialiser** en SQL dans chaque SGBD.

---

## 1. Implémentation SQL du MPD “commandes”

Dans cette section, on part de la **spécification MPD** “commandes/clients/produits” et on la décline par SGBD.

!!! tip
    Le **MPD** reste une représentation physique abstraite.  
    Le SQL ci-dessous est une **traduction directe** exploitable en scripts de création (`CREATE TABLE`).

### 1.1. Scripts DDL par SGBD

=== ":lucide-database: generique"

    ```sql
    CREATE TABLE CLIENT (
        id_client    INTEGER       PRIMARY KEY,
        nom          VARCHAR(100)  NOT NULL,
        email        VARCHAR(255)  NOT NULL
        -- CONSTRAINT uq_client_email UNIQUE (email)
    );

    CREATE TABLE COMMANDE (
        id_commande   INTEGER       PRIMARY KEY,
        date_commande DATE          NOT NULL,
        statut        VARCHAR(30)   NOT NULL,
        id_client     INTEGER       NOT NULL,
        CONSTRAINT fk_commande_client
          FOREIGN KEY (id_client) REFERENCES CLIENT(id_client)
    );

    CREATE TABLE PRODUIT (
        id_produit  INTEGER       PRIMARY KEY,
        libelle     VARCHAR(150)  NOT NULL,
        prix        NUMERIC(10,2) NOT NULL,
        CONSTRAINT ck_produit_prix_non_negatif CHECK (prix >= 0)
    );

    CREATE TABLE LIGNE_COMMANDE (
        id_commande   INTEGER       NOT NULL,
        id_produit    INTEGER       NOT NULL,
        quantite      INTEGER       NOT NULL,
        prix_unitaire NUMERIC(10,2) NOT NULL,
        PRIMARY KEY (id_commande, id_produit),
        CONSTRAINT ck_ligne_quantite_positive CHECK (quantite > 0),
        CONSTRAINT ck_ligne_prix_non_negatif CHECK (prix_unitaire >= 0),
        CONSTRAINT fk_ligne_commande
          FOREIGN KEY (id_commande) REFERENCES COMMANDE(id_commande),
        CONSTRAINT fk_ligne_produit
          FOREIGN KEY (id_produit) REFERENCES PRODUIT(id_produit)
    );
    ```

=== ":lucide-database: postgresql"

    ```sql
    CREATE TABLE client (
        id_client    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nom          VARCHAR(100)  NOT NULL,
        email        VARCHAR(255)  NOT NULL UNIQUE
    );

    CREATE TABLE commande (
        id_commande   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        date_commande DATE          NOT NULL,
        statut        VARCHAR(30)   NOT NULL,
        id_client     INTEGER       NOT NULL,
        CONSTRAINT fk_commande_client
          FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT
    );

    CREATE TABLE produit (
        id_produit  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        libelle     VARCHAR(150)  NOT NULL,
        prix        NUMERIC(10,2) NOT NULL,
        CONSTRAINT ck_produit_prix_non_negatif CHECK (prix >= 0)
    );

    CREATE TABLE ligne_commande (
        id_commande   INTEGER       NOT NULL,
        id_produit    INTEGER       NOT NULL,
        quantite      INTEGER       NOT NULL,
        prix_unitaire NUMERIC(10,2) NOT NULL,
        PRIMARY KEY (id_commande, id_produit),
        CONSTRAINT ck_ligne_quantite_positive CHECK (quantite > 0),
        CONSTRAINT ck_ligne_prix_non_negatif CHECK (prix_unitaire >= 0),
        CONSTRAINT fk_ligne_commande
          FOREIGN KEY (id_commande)
          REFERENCES commande(id_commande)
          ON DELETE CASCADE,
        CONSTRAINT fk_ligne_produit
          FOREIGN KEY (id_produit)
          REFERENCES produit(id_produit)
    );

    CREATE INDEX idx_commande_id_client ON commande(id_client);
    CREATE INDEX idx_ligne_commande_id_produit ON ligne_commande(id_produit);
    ```

=== ":lucide-database: mysql/maria db"

    ```sql
    CREATE TABLE client (
        id_client    INT           NOT NULL AUTO_INCREMENT,
        nom          VARCHAR(100)  NOT NULL,
        email        VARCHAR(255)  NOT NULL,
        PRIMARY KEY (id_client),
        UNIQUE KEY uq_client_email (email)
    ) ENGINE=InnoDB;

    CREATE TABLE commande (
        id_commande   INT           NOT NULL AUTO_INCREMENT,
        date_commande DATE          NOT NULL,
        statut        VARCHAR(30)   NOT NULL,
        id_client     INT           NOT NULL,
        PRIMARY KEY (id_commande),
        CONSTRAINT fk_commande_client
          FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT
    ) ENGINE=InnoDB;

    CREATE TABLE produit (
        id_produit  INT            NOT NULL AUTO_INCREMENT,
        libelle     VARCHAR(150)   NOT NULL,
        prix        DECIMAL(10,2)  NOT NULL,
        PRIMARY KEY (id_produit),
        CONSTRAINT ck_produit_prix_non_negatif CHECK (prix >= 0)
    ) ENGINE=InnoDB;

    CREATE TABLE ligne_commande (
        id_commande   INT            NOT NULL,
        id_produit    INT            NOT NULL,
        quantite      INT            NOT NULL,
        prix_unitaire DECIMAL(10,2)  NOT NULL,
        PRIMARY KEY (id_commande, id_produit),
        CONSTRAINT ck_ligne_quantite_positive CHECK (quantite > 0),
        CONSTRAINT ck_ligne_prix_non_negatif CHECK (prix_unitaire >= 0),
        CONSTRAINT fk_ligne_commande
          FOREIGN KEY (id_commande)
          REFERENCES commande(id_commande)
          ON DELETE CASCADE,
        CONSTRAINT fk_ligne_produit
          FOREIGN KEY (id_produit)
          REFERENCES produit(id_produit)
    ) ENGINE=InnoDB;

    CREATE INDEX idx_commande_id_client ON commande(id_client);
    CREATE INDEX idx_ligne_commande_id_produit ON ligne_commande(id_produit);
    ```

=== ":lucide-database: sqlite3"

    ```sql
    PRAGMA foreign_keys = ON;

    CREATE TABLE client (
        id_client    INTEGER       PRIMARY KEY AUTOINCREMENT,
        nom          TEXT          NOT NULL,
        email        TEXT          NOT NULL UNIQUE
    );

    CREATE TABLE commande (
        id_commande   INTEGER       PRIMARY KEY AUTOINCREMENT,
        date_commande TEXT          NOT NULL, -- ISO 8601 (YYYY-MM-DD)
        statut        TEXT          NOT NULL,
        id_client     INTEGER       NOT NULL,
        FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT
    );

    CREATE TABLE produit (
        id_produit  INTEGER       PRIMARY KEY AUTOINCREMENT,
        libelle     TEXT          NOT NULL,
        prix        REAL          NOT NULL
        -- On peut simuler des CHECK mais SQLite est tolérant
    );

    CREATE TABLE ligne_commande (
        id_commande   INTEGER       NOT NULL,
        id_produit    INTEGER       NOT NULL,
        quantite      INTEGER       NOT NULL,
        prix_unitaire REAL          NOT NULL,
        PRIMARY KEY (id_commande, id_produit),
        FOREIGN KEY (id_commande)
          REFERENCES commande(id_commande)
          ON DELETE CASCADE,
        FOREIGN KEY (id_produit)
          REFERENCES produit(id_produit)
    );

    CREATE INDEX idx_commande_id_client ON commande(id_client);
    CREATE INDEX idx_ligne_commande_id_produit ON ligne_commande(id_produit);
    ```

---

## 2. Exemple complet n°1 : gestion de formation

On reprend maintenant le MPD **“formation / sessions / stagiaires”** présenté dans la page MPD, et on le décline lui aussi en SQL.

Rappel MPD :

* `FORMATION(id_formation PK, titre, niveau)`
* `FORMATEUR(id_formateur PK, nom, expertise)`
* `STAGIAIRE(id_stagiaire PK, nom, email)`
* `SESSION(id_session PK, date_debut, date_fin, lieu, id_formation FK, id_formateur FK)`
* `INSCRIPTION(id_stagiaire FK, id_session FK, date_inscription, statut, PK = id_stagiaire + id_session)`

### 2.1. Implémentation SQL par SGBD

=== ":lucide-database: generique"

    ```sql
    CREATE TABLE FORMATION (
        id_formation  INTEGER       PRIMARY KEY,
        titre         VARCHAR(150)  NOT NULL,
        niveau        VARCHAR(50)   NOT NULL
    );

    CREATE TABLE FORMATEUR (
        id_formateur  INTEGER       PRIMARY KEY,
        nom           VARCHAR(100)  NOT NULL,
        expertise     VARCHAR(150)  NOT NULL
    );

    CREATE TABLE STAGIAIRE (
        id_stagiaire  INTEGER       PRIMARY KEY,
        nom           VARCHAR(100)  NOT NULL,
        email         VARCHAR(255)  NOT NULL
        -- CONSTRAINT uq_stagiaire_email UNIQUE (email)
    );

    CREATE TABLE SESSION (
        id_session    INTEGER       PRIMARY KEY,
        date_debut    DATE          NOT NULL,
        date_fin      DATE          NOT NULL,
        lieu          VARCHAR(150)  NOT NULL,
        id_formation  INTEGER       NOT NULL,
        id_formateur  INTEGER       NOT NULL,
        CONSTRAINT fk_session_formation
          FOREIGN KEY (id_formation) REFERENCES FORMATION(id_formation),
        CONSTRAINT fk_session_formateur
          FOREIGN KEY (id_formateur) REFERENCES FORMATEUR(id_formateur)
    );

    CREATE TABLE INSCRIPTION (
        id_stagiaire     INTEGER       NOT NULL,
        id_session       INTEGER       NOT NULL,
        date_inscription DATE          NOT NULL,
        statut           VARCHAR(30)   NOT NULL,
        PRIMARY KEY (id_stagiaire, id_session),
        CONSTRAINT fk_inscription_stagiaire
          FOREIGN KEY (id_stagiaire) REFERENCES STAGIAIRE(id_stagiaire),
        CONSTRAINT fk_inscription_session
          FOREIGN KEY (id_session) REFERENCES SESSION(id_session)
    );
    ```

=== ":lucide-database: postgresql"

    ```sql
    CREATE TABLE formation (
        id_formation  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        titre         VARCHAR(150)  NOT NULL,
        niveau        VARCHAR(50)   NOT NULL
    );

    CREATE TABLE formateur (
        id_formateur  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nom           VARCHAR(100)  NOT NULL,
        expertise     VARCHAR(150)  NOT NULL
    );

    CREATE TABLE stagiaire (
        id_stagiaire  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nom           VARCHAR(100)  NOT NULL,
        email         VARCHAR(255)  NOT NULL UNIQUE
    );

    CREATE TABLE session (
        id_session    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        date_debut    DATE          NOT NULL,
        date_fin      DATE          NOT NULL,
        lieu          VARCHAR(150)  NOT NULL,
        id_formation  INTEGER       NOT NULL,
        id_formateur  INTEGER       NOT NULL,
        CONSTRAINT fk_session_formation
          FOREIGN KEY (id_formation)
          REFERENCES formation(id_formation)
          ON DELETE RESTRICT,
        CONSTRAINT fk_session_formateur
          FOREIGN KEY (id_formateur)
          REFERENCES formateur(id_formateur)
          ON DELETE RESTRICT
    );

    CREATE TABLE inscription (
        id_stagiaire     INTEGER       NOT NULL,
        id_session       INTEGER       NOT NULL,
        date_inscription DATE          NOT NULL,
        statut           VARCHAR(30)   NOT NULL,
        PRIMARY KEY (id_stagiaire, id_session),
        CONSTRAINT fk_inscription_stagiaire
          FOREIGN KEY (id_stagiaire)
          REFERENCES stagiaire(id_stagiaire)
          ON DELETE CASCADE,
        CONSTRAINT fk_inscription_session
          FOREIGN KEY (id_session)
          REFERENCES session(id_session)
          ON DELETE CASCADE
    );

    CREATE INDEX idx_session_id_formation ON session(id_formation);
    CREATE INDEX idx_session_id_formateur ON session(id_formateur);
    CREATE INDEX idx_inscription_id_stagiaire ON inscription(id_stagiaire);
    ```

=== ":lucide-database: mysql/maria db"

    ```sql
    CREATE TABLE formation (
        id_formation  INT            NOT NULL AUTO_INCREMENT,
        titre         VARCHAR(150)   NOT NULL,
        niveau        VARCHAR(50)    NOT NULL,
        PRIMARY KEY (id_formation)
    ) ENGINE=InnoDB;

    CREATE TABLE formateur (
        id_formateur  INT            NOT NULL AUTO_INCREMENT,
        nom           VARCHAR(100)   NOT NULL,
        expertise     VARCHAR(150)   NOT NULL,
        PRIMARY KEY (id_formateur)
    ) ENGINE=InnoDB;

    CREATE TABLE stagiaire (
        id_stagiaire  INT            NOT NULL AUTO_INCREMENT,
        nom           VARCHAR(100)   NOT NULL,
        email         VARCHAR(255)   NOT NULL,
        PRIMARY KEY (id_stagiaire),
        UNIQUE KEY uq_stagiaire_email (email)
    ) ENGINE=InnoDB;

    CREATE TABLE session (
        id_session    INT            NOT NULL AUTO_INCREMENT,
        date_debut    DATE           NOT NULL,
        date_fin      DATE           NOT NULL,
        lieu          VARCHAR(150)   NOT NULL,
        id_formation  INT            NOT NULL,
        id_formateur  INT            NOT NULL,
        PRIMARY KEY (id_session),
        CONSTRAINT fk_session_formation
          FOREIGN KEY (id_formation)
          REFERENCES formation(id_formation)
          ON DELETE RESTRICT,
        CONSTRAINT fk_session_formateur
          FOREIGN KEY (id_formateur)
          REFERENCES formateur(id_formateur)
          ON DELETE RESTRICT
    ) ENGINE=InnoDB;

    CREATE TABLE inscription (
        id_stagiaire     INT            NOT NULL,
        id_session       INT            NOT NULL,
        date_inscription DATE           NOT NULL,
        statut           VARCHAR(30)    NOT NULL,
        PRIMARY KEY (id_stagiaire, id_session),
        CONSTRAINT fk_inscription_stagiaire
          FOREIGN KEY (id_stagiaire)
          REFERENCES stagiaire(id_stagiaire)
          ON DELETE CASCADE,
        CONSTRAINT fk_inscription_session
          FOREIGN KEY (id_session)
          REFERENCES session(id_session)
          ON DELETE CASCADE
    ) ENGINE=InnoDB;

    CREATE INDEX idx_session_id_formation ON session(id_formation);
    CREATE INDEX idx_session_id_formateur ON session(id_formateur);
    CREATE INDEX idx_inscription_id_stagiaire ON inscription(id_stagiaire);
    ```

=== ":lucide-database: sqlite3"

    ```sql
    PRAGMA foreign_keys = ON;

    CREATE TABLE formation (
        id_formation  INTEGER       PRIMARY KEY AUTOINCREMENT,
        titre         TEXT          NOT NULL,
        niveau        TEXT          NOT NULL
    );

    CREATE TABLE formateur (
        id_formateur  INTEGER       PRIMARY KEY AUTOINCREMENT,
        nom           TEXT          NOT NULL,
        expertise     TEXT          NOT NULL
    );

    CREATE TABLE stagiaire (
        id_stagiaire  INTEGER       PRIMARY KEY AUTOINCREMENT,
        nom           TEXT          NOT NULL,
        email         TEXT          NOT NULL UNIQUE
    );

    CREATE TABLE session (
        id_session    INTEGER       PRIMARY KEY AUTOINCREMENT,
        date_debut    TEXT          NOT NULL, -- YYYY-MM-DD
        date_fin      TEXT          NOT NULL,
        lieu          TEXT          NOT NULL,
        id_formation  INTEGER       NOT NULL,
        id_formateur  INTEGER       NOT NULL,
        FOREIGN KEY (id_formation)
          REFERENCES formation(id_formation)
          ON DELETE RESTRICT,
        FOREIGN KEY (id_formateur)
          REFERENCES formateur(id_formateur)
          ON DELETE RESTRICT
    );

    CREATE TABLE inscription (
        id_stagiaire     INTEGER       NOT NULL,
        id_session       INTEGER       NOT NULL,
        date_inscription TEXT          NOT NULL,
        statut           TEXT          NOT NULL,
        PRIMARY KEY (id_stagiaire, id_session),
        FOREIGN KEY (id_stagiaire)
          REFERENCES stagiaire(id_stagiaire)
          ON DELETE CASCADE,
        FOREIGN KEY (id_session)
          REFERENCES session(id_session)
          ON DELETE CASCADE
    );

    CREATE INDEX idx_session_id_formation ON session(id_formation);
    CREATE INDEX idx_session_id_formateur ON session(id_formateur);
    CREATE INDEX idx_inscription_id_stagiaire ON inscription(id_stagiaire);
    ```

---

## 3. Exemple complet n°2 : support client (tickets)

Dernier cas : un schéma de **support client / helpdesk**.

Rappel MPD :

* `CLIENT(id_client PK, nom, email)`
* `AGENT(id_agent PK, nom, equipe)`
* `TICKET(id_ticket PK, date_ouverture, statut, priorite, sujet, id_client FK, id_agent FK)`

!!! note "Choix métier important"
    Dans cette version, **tout ticket est obligatoirement assigné à un agent**.
    La clé étrangère `id_agent` est donc **NOT NULL** et les contraintes SQL utilisent `ON DELETE RESTRICT`.
    Si tu veux autoriser des tickets non assignés, il faudrait :

    - rendre `id_agent` nullable (`id_agent INTEGER NULL`),
    - passer à `ON DELETE SET NULL` côté SQL.

### 3.1. Implémentation SQL par SGBD

=== ":lucide-database: generique"

    ```sql
    CREATE TABLE CLIENT (
        id_client  INTEGER       PRIMARY KEY,
        nom        VARCHAR(100)  NOT NULL,
        email      VARCHAR(255)  NOT NULL
        -- CONSTRAINT uq_client_email UNIQUE (email)
    );

    CREATE TABLE AGENT (
        id_agent   INTEGER       PRIMARY KEY,
        nom        VARCHAR(100)  NOT NULL,
        equipe     VARCHAR(100)  NOT NULL
    );

    CREATE TABLE TICKET (
        id_ticket      INTEGER       PRIMARY KEY,
        date_ouverture DATE          NOT NULL,
        statut         VARCHAR(30)   NOT NULL,
        priorite       VARCHAR(20)   NOT NULL,
        sujet          VARCHAR(255)  NOT NULL,
        id_client      INTEGER       NOT NULL,
        id_agent       INTEGER       NOT NULL,
        CONSTRAINT fk_ticket_client
          FOREIGN KEY (id_client) REFERENCES CLIENT(id_client),
        CONSTRAINT fk_ticket_agent
          FOREIGN KEY (id_agent) REFERENCES AGENT(id_agent)
    );
    ```

=== ":lucide-database: postgresql"

    ```sql
    CREATE TABLE client (
        id_client  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nom        VARCHAR(100)  NOT NULL,
        email      VARCHAR(255)  NOT NULL UNIQUE
    );

    CREATE TABLE agent (
        id_agent   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        nom        VARCHAR(100)  NOT NULL,
        equipe     VARCHAR(100)  NOT NULL
    );

    CREATE TABLE ticket (
        id_ticket      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        date_ouverture DATE          NOT NULL,
        statut         VARCHAR(30)   NOT NULL,
        priorite       VARCHAR(20)   NOT NULL,
        sujet          VARCHAR(255)  NOT NULL,
        id_client      INTEGER       NOT NULL,
        id_agent       INTEGER       NOT NULL,
        CONSTRAINT fk_ticket_client
          FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT,
        CONSTRAINT fk_ticket_agent
          FOREIGN KEY (id_agent)
          REFERENCES agent(id_agent)
          ON DELETE RESTRICT
    );

    CREATE INDEX idx_ticket_id_client ON ticket(id_client);
    CREATE INDEX idx_ticket_id_agent ON ticket(id_agent);
    ```

=== ":lucide-database: mysql/maria db"

    ```sql
    CREATE TABLE client (
        id_client  INT            NOT NULL AUTO_INCREMENT,
        nom        VARCHAR(100)   NOT NULL,
        email      VARCHAR(255)   NOT NULL,
        PRIMARY KEY (id_client),
        UNIQUE KEY uq_client_email (email)
    ) ENGINE=InnoDB;

    CREATE TABLE agent (
        id_agent   INT            NOT NULL AUTO_INCREMENT,
        nom        VARCHAR(100)   NOT NULL,
        equipe     VARCHAR(100)   NOT NULL,
        PRIMARY KEY (id_agent)
    ) ENGINE=InnoDB;

    CREATE TABLE ticket (
        id_ticket      INT            NOT NULL AUTO_INCREMENT,
        date_ouverture DATE           NOT NULL,
        statut         VARCHAR(30)    NOT NULL,
        priorite       VARCHAR(20)    NOT NULL,
        sujet          VARCHAR(255)   NOT NULL,
        id_client      INT            NOT NULL,
        id_agent       INT            NOT NULL,
        PRIMARY KEY (id_ticket),
        CONSTRAINT fk_ticket_client
          FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT,
        CONSTRAINT fk_ticket_agent
          FOREIGN KEY (id_agent)
          REFERENCES agent(id_agent)
          ON DELETE RESTRICT
    ) ENGINE=InnoDB;

    CREATE INDEX idx_ticket_id_client ON ticket(id_client);
    CREATE INDEX idx_ticket_id_agent ON ticket(id_agent);
    ```

=== ":lucide-database: sqlite3"

    ```sql
    PRAGMA foreign_keys = ON;

    CREATE TABLE client (
        id_client  INTEGER       PRIMARY KEY AUTOINCREMENT,
        nom        TEXT          NOT NULL,
        email      TEXT          NOT NULL UNIQUE
    );

    CREATE TABLE agent (
        id_agent   INTEGER       PRIMARY KEY AUTOINCREMENT,
        nom        TEXT          NOT NULL,
        equipe     TEXT          NOT NULL
    );

    CREATE TABLE ticket (
        id_ticket      INTEGER       PRIMARY KEY AUTOINCREMENT,
        date_ouverture TEXT          NOT NULL, -- YYYY-MM-DD
        statut         TEXT          NOT NULL,
        priorite       TEXT          NOT NULL,
        sujet          TEXT          NOT NULL,
        id_client      INTEGER       NOT NULL,
        id_agent       INTEGER       NOT NULL,
        FOREIGN KEY (id_client)
          REFERENCES client(id_client)
          ON DELETE RESTRICT,
        FOREIGN KEY (id_agent)
          REFERENCES agent(id_agent)
          ON DELETE RESTRICT
    );

    CREATE INDEX idx_ticket_id_client ON ticket(id_client);
    CREATE INDEX idx_ticket_id_agent ON ticket(id_agent);
    ```

---

## Conclusion

Ce module **MPD → SQL** montre comment :

* partir d’un **MPD proprement défini** (types, PK, FK, contraintes),
* décliner ce modèle dans plusieurs SGBD,
* tout en gardant **la même structure métier**.

En pratique, la démarche est toujours la même :

1. Prendre le **MPD** comme référence unique.
2. Choisir les **types natifs** du SGBD cible (PostgreSQL, MySQL, SQLite…).
3. Reproduire fidèlement : `PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `INDEX`.
4. Documenter les choix de comportement (`ON DELETE RESTRICT`, `CASCADE`, `SET NULL`) en lien avec les règles métier.

---

## Le mot de la fin

!!! quote

    La traduction d’un **MPD vers du SQL concret** est l’étape où la théorie rencontre enfin la réalité des SGBD.
    À ce stade, les concepts Merise deviennent des objets techniques tangibles : tables, colonnes, types, contraintes, index et comportements référentiels.

    Un bon script SQL doit toujours refléter trois exigences :

    * **Fidélité** au MPD : aucune clé ni contrainte ne doit disparaître entre la modélisation et l’implémentation.
    * **Cohérence** avec le moteur utilisé : types, comportements (`CASCADE`, `RESTRICT`, `SET NULL`) et options d’index s’adaptent au SGBD, mais la logique métier reste intacte.
    * **Robustesse** : plus les contraintes sont explicitement posées dans le schéma SQL, moins l’application devra compenser par du code fragile.

    Avec cette page, tu possèdes une **chaîne complète et professionnalisante** :
    MCD → MLD → MPD → SQL.

    Tu peux maintenant enrichir ton écosystème avec :

    * des scripts de migration,
    * des vues matérialisées,
    * des politiques d’accès et de sécurité,
    * ou même des comparaisons SGBD pour aider tes étudiants ou clients à choisir la bonne plateforme.

    > Ce chapitre n’est pas une fin : c’est un **point de départ solide** pour l’industrialisation de la donnée dans tes futures architectures, qu’elles soient pédagogiques, professionnelles ou orientées DevSecOps.

<br />