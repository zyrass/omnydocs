# DevSecOps

    # ==========================================================================
    # 3.6 — DevSecOps (version minimale)
    # ==========================================================================
    # Rôle :
    # - Automatiser la livraison applicative (build/test/deploy).
    # - Standardiser les environnements (Docker).
    # - Encadrer la gestion des secrets (y compris politiques MDP/entropie).
    #
    # Remarque de périmètre :
    # - La cybersécurité outillage/attaque/défense n’est pas traitée ici.
    {"DevSecOps" = [
        "dev-cloud/devsecops/index.md",

        # ------------------------------------------------------------------------
        # CI/CD
        # ------------------------------------------------------------------------
        # Rôle :
        # - Définir des pipelines reproductibles (stages, artifacts, runners).
        # - Intégrer tests et contrôles qualité dans la chaîne de livraison.
        {"CI/CD" = [
        "dev-cloud/devsecops/cicd/index.md",
        {"GitHub Actions" = "dev-cloud/devsecops/cicd/github-actions.md"},
        {"GitLab CI/CD"   = "dev-cloud/devsecops/cicd/gitlab-cicd.md"},
        ]},

        # ------------------------------------------------------------------------
        # Conteneurisation (Docker)
        # ------------------------------------------------------------------------
        # Rôle :
        # - Packaging et exécution reproductible.
        # - Orchestration simple multi-services via Compose.
        {"Docker" = [
        "dev-cloud/devsecops/containers/index.md",
        {"Docker (Moteur)" = "dev-cloud/devsecops/containers/docker.md"},
        {"Docker Compose"  = "dev-cloud/devsecops/containers/docker_compose.md"},
        ]},

        # ------------------------------------------------------------------------
        # Secrets
        # ------------------------------------------------------------------------
        # Rôle :
        # - Stockage et manipulation de secrets (local, CI, environnements).
        # - Politiques MDP : entropie, robustesse, bonnes pratiques.
        {"Secrets" = [
        "dev-cloud/devsecops/secrets/index.md",

        # Entropie des mots de passe :
        # - Modèles de menace, longueur vs complexité, recommandations.
        {"Entropie des mots de passe" = "dev-cloud/devsecops/secrets/password-entropy.md"},

        # Vault :
        # - Gestion centralisée et rotation des secrets (option d’industrialisation).
        {"Vault (HashiCorp)" = "dev-cloud/devsecops/secrets/vault.md"},
        ]},
    ]},

<br />