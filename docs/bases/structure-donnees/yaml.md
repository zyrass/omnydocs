---
description: "Maîtriser le format YAML pour la configuration et l'infrastructure as code"
icon: lucide/book-open-check
tags: ["YAML", "DONNÉES", "CONFIGURATION", "DEVOPS", "INFRASTRUCTURE"]
---

# YAML - YAML Ain't Markup Language

## Introduction

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.1"
  data-time="50-55 minutes">
</div>

!!! quote "Analogie pédagogique"
    _Imaginez un **document de configuration** écrit comme vous écririez une liste de courses ou un plan d'action : **indenté naturellement**, avec des **tirets pour les listes**, des **deux-points pour les propriétés**, et des **commentaires** pour expliquer vos choix. **YAML fonctionne exactement ainsi** : c'est un format qui privilégie la **lisibilité humaine** avant tout, rendant les fichiers de configuration aussi clairs qu'un document texte bien structuré._

> **YAML (YAML Ain't Markup Language)** est un format de **sérialisation de données** conçu pour être **extrêmement lisible** par les humains. Contrairement à JSON qui privilégie la machine, YAML privilégie l'**humain** en utilisant une syntaxe basée sur l'**indentation** plutôt que les accolades, rendant les configurations complexes plus faciles à lire et maintenir.

YAML est devenu le **standard de facto** pour la **configuration d'infrastructure** (Kubernetes, Docker Compose, Ansible), les **pipelines CI/CD** (GitHub Actions, GitLab CI, CircleCI), et les **fichiers de configuration** d'applications modernes. Sa lisibilité en fait le choix privilégié pour tout ce qui sera lu et modifié fréquemment par des humains.

!!! info "Pourquoi c'est important ?"
    YAML permet la **configuration d'infrastructure as code**, les **manifestes Kubernetes**, les **playbooks Ansible**, les **pipelines CI/CD**, les **configurations Docker Compose**, et constitue le langage standard pour **DevOps** et **automatisation**.

## Structure YAML

### Syntaxe de base

**Document YAML simple :**
```yaml
# Commentaire : ceci est un utilisateur
nom: Dupont
prenom: Alice
age: 28
actif: true
roles:
  - admin
  - user
```

**Équivalent JSON :**
```json
{
  "nom": "Dupont",
  "prenom": "Alice",
  "age": 28,
  "actif": true,
  "roles": ["admin", "user"]
}
```

### Règles d'indentation

!!! danger "Règle CRITIQUE : ESPACES uniquement"
    YAML utilise **UNIQUEMENT des espaces** pour l'indentation, **JAMAIS de tabulations**.
    
    - ✅ 2 espaces (recommandé)
    - ✅ 4 espaces (acceptable)
    - ❌ Tabulations (INVALIDE)
    - ❌ Mélange espaces/tabs (INVALIDE)

```yaml
# ✅ CORRECT - 2 espaces
utilisateur:
  nom: Alice
  adresse:
    rue: 12 rue des Fleurs
    ville: Paris
    
# ❌ INCORRECT - tabulation
utilisateur:
→nom: Alice  # Tab = ERREUR
```

### Types de données

**Scalaires (valeurs simples) :**
```yaml
# Chaînes de caractères
chaine_simple: Hello World
chaine_avec_guillemets: "Hello World"
chaine_apostrophes: 'Hello World'
chaine_multiligne: |
  Ceci est une chaîne
  sur plusieurs lignes.
  Les retours à la ligne sont préservés.
  
chaine_pliee: >
  Ceci est une chaîne pliée.
  Les retours à la ligne deviennent des espaces.
  Utile pour longues descriptions.

# Nombres
entier: 42
decimal: 3.14159
scientifique: 1.5e+3
octal: 0o14
hexadecimal: 0xC

# Booléens (multiples syntaxes)
booleen_vrai: true
booleen_yes: yes
booleen_on: on
booleen_faux: false
booleen_no: no
booleen_off: off

# Null (valeur nulle)
valeur_nulle: null
valeur_tilde: ~
valeur_vide:

# Date et heure (ISO 8601)
date: 2025-11-15
datetime: 2025-11-15T10:30:45Z
datetime_tz: 2025-11-15T10:30:45+02:00
```

**Listes (tableaux) :**
```yaml
# Style bloc (recommandé)
langages:
  - Python
  - JavaScript
  - Go
  - Rust

# Style flux (compact)
langages_flux: [Python, JavaScript, Go, Rust]

# Listes imbriquées
equipes:
  - nom: DevOps
    membres:
      - Alice
      - Bob
  - nom: Security
    membres:
      - Charlie
      - David
```

**Dictionnaires (objets) :**
```yaml
# Style bloc
utilisateur:
  nom: Dupont
  prenom: Alice
  age: 28
  actif: true

# Style flux
utilisateur_flux: {nom: Dupont, prenom: Alice, age: 28}

# Imbrication profonde
entreprise:
  nom: TechCorp
  departements:
    IT:
      responsable: Alice
      budget: 500000
      equipes:
        - DevOps
        - Security
    RH:
      responsable: Bob
      budget: 200000
```

### Ancres et références

Les **ancres** (`&`) et **références** (`*`) permettent de réutiliser des blocs de configuration.

```yaml
# Définir une ancre
defaults: &defaults
  timeout: 30
  retry: 3
  log_level: info

# Référencer l'ancre
production:
  <<: *defaults
  environment: production
  log_level: warn  # Override

staging:
  <<: *defaults
  environment: staging

# Résultat équivalent :
# production:
#   timeout: 30
#   retry: 3
#   log_level: warn
#   environment: production
```

**Ancres pour listes :**
```yaml
.commun: &roles_commun
  - read
  - write

admin:
  roles:
    - *roles_commun
    - admin
    - delete

user:
  roles: *roles_commun
```

### Documents multiples

YAML peut contenir **plusieurs documents** dans un seul fichier, séparés par `---`.

```yaml
---
# Document 1 : Configuration dev
environment: development
database:
  host: localhost
  port: 5432

---
# Document 2 : Configuration prod
environment: production
database:
  host: db.production.com
  port: 5432
  ssl: true
```

### Commentaires

```yaml
# Commentaire sur une ligne

utilisateur:
  nom: Alice      # Commentaire en fin de ligne
  # prenom: Bob   # Ligne commentée (désactivée)
  age: 28
  
  # Bloc de commentaire expliquant
  # la structure des permissions
  # sur plusieurs lignes
  permissions:
    - read
    - write
```

## Cas d'usage en cybersécurité

!!! danger "Attention - prenez ces exemples de contenu avec ce que l'on peut obtenir. Il n'est pas question de l'analyser ici."

### Exemple 1 : Configuration SIEM (règles de détection)

!!! example "Exemple n°1 - Règles Sigma pour SIEM"

    ```yaml
    ---
    title: Brute Force SSH Detection
    id: rule-001
    status: stable
    description: Détecte les tentatives de brute force SSH
    author: Security Team
    date: 2025-11-15
    modified: 2025-11-15
    
    logsource:
      product: linux
      service: sshd
    
    detection:
      selection:
        EventID: 4625
        LogonType: 10
        SourceNetworkAddress: '*'
      
      timeframe: 5m
      
      condition: selection | count(SourceIP) > 5
    
    falsepositives:
      - Legitimate users with wrong password
      - Automated monitoring systems
    
    level: high
    
    tags:
      - attack.credential_access
      - attack.t1110.001  # Brute Force: Password Guessing
    
    ---
    title: Privilege Escalation via Sudo
    id: rule-002
    status: experimental
    description: Détecte les tentatives d'escalade de privilèges
    
    logsource:
      product: linux
      service: auditd
    
    detection:
      selection:
        type: EXECVE
        a0: sudo
        a1:
          - su
          - passwd
          - usermod
      
      filter_admins:
        uid:
          - 0
          - 1000  # Admin user
      
      condition: selection and not filter_admins
    
    level: critical
    
    tags:
      - attack.privilege_escalation
      - attack.t1548.003  # Sudo and Sudo Caching
    ```

### Exemple 2 : Docker Compose sécurisé

!!! example "Exemple n°2 - Stack de sécurité avec Docker Compose"

    ```yaml
    version: '3.8'
    
    # Réseaux isolés
    networks:
      frontend:
        driver: bridge
      backend:
        driver: bridge
        internal: true  # Pas d'accès internet
    
    # Volumes persistants
    volumes:
      db_data:
        driver: local
      logs:
        driver: local
    
    services:
      # Serveur web avec reverse proxy
      nginx:
        image: nginx:alpine
        container_name: nginx_proxy
        restart: unless-stopped
        
        ports:
          - "80:80"
          - "443:443"
        
        networks:
          - frontend
        
        volumes:
          - ./nginx/conf.d:/etc/nginx/conf.d:ro
          - ./nginx/ssl:/etc/nginx/ssl:ro
          - logs:/var/log/nginx
        
        environment:
          - TZ=Europe/Paris
        
        security_opt:
          - no-new-privileges:true
        
        cap_drop:
          - ALL
        cap_add:
          - CHOWN
          - SETGID
          - SETUID
        
        healthcheck:
          test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost"]
          interval: 30s
          timeout: 10s
          retries: 3
          start_period: 40s
      
      # Application web
      webapp:
        image: webapp:latest
        container_name: webapp
        restart: unless-stopped
        
        networks:
          - frontend
          - backend
        
        environment:
          - NODE_ENV=production
          - DB_HOST=postgres
          - DB_PORT=5432
          - DB_NAME=${DB_NAME}
          - DB_USER=${DB_USER}
          - DB_PASSWORD=${DB_PASSWORD}
        
        depends_on:
          postgres:
            condition: service_healthy
        
        security_opt:
          - no-new-privileges:true
        
        read_only: true
        
        tmpfs:
          - /tmp
          - /var/run
      
      # Base de données PostgreSQL
      postgres:
        image: postgres:15-alpine
        container_name: postgres_db
        restart: unless-stopped
        
        networks:
          - backend
        
        volumes:
          - db_data:/var/lib/postgresql/data
        
        environment:
          - POSTGRES_DB=${DB_NAME}
          - POSTGRES_USER=${DB_USER}
          - POSTGRES_PASSWORD=${DB_PASSWORD}
        
        security_opt:
          - no-new-privileges:true
        
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
          interval: 10s
          timeout: 5s
          retries: 5
      
      # Fail2ban pour protection
      fail2ban:
        image: crazymax/fail2ban:latest
        container_name: fail2ban
        restart: unless-stopped
        
        network_mode: host
        
        volumes:
          - ./fail2ban:/etc/fail2ban:ro
          - logs:/var/log:ro
        
        cap_add:
          - NET_ADMIN
          - NET_RAW
        
        security_opt:
          - no-new-privileges:true
    ```

### Exemple 3 : Kubernetes Security Policy

!!! example "Exemple n°3 - Network Policy Kubernetes"

    ```yaml
    ---
    # Isolation réseau par défaut - tout bloquer
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: default-deny-all
      namespace: production
    spec:
      podSelector: {}
      policyTypes:
        - Ingress
        - Egress
    
    ---
    # Autoriser trafic frontend -> backend
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-frontend-to-backend
      namespace: production
    spec:
      podSelector:
        matchLabels:
          app: backend
          tier: api
      
      policyTypes:
        - Ingress
      
      ingress:
        - from:
            - podSelector:
                matchLabels:
                  app: frontend
                  tier: web
          ports:
            - protocol: TCP
              port: 8080
    
    ---
    # Autoriser backend -> database
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-backend-to-db
      namespace: production
    spec:
      podSelector:
        matchLabels:
          app: postgres
          tier: database
      
      policyTypes:
        - Ingress
      
      ingress:
        - from:
            - podSelector:
                matchLabels:
                  app: backend
                  tier: api
          ports:
            - protocol: TCP
              port: 5432
    
    ---
    # Autoriser sortie DNS et HTTPS
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: allow-dns-https-egress
      namespace: production
    spec:
      podSelector:
        matchLabels:
          tier: api
      
      policyTypes:
        - Egress
      
      egress:
        # DNS
        - to:
            - namespaceSelector:
                matchLabels:
                  name: kube-system
            - podSelector:
                matchLabels:
                  k8s-app: kube-dns
          ports:
            - protocol: UDP
              port: 53
        
        # HTTPS externe
        - to:
            - namespaceSelector: {}
          ports:
            - protocol: TCP
              port: 443
    ```

### Exemple 4 : Pipeline CI/CD GitHub Actions

!!! example "Exemple n°4 - Security Scanning Pipeline"

    ```yaml
    name: Security Scan Pipeline
    
    on:
      push:
        branches:
          - main
          - develop
      pull_request:
        branches:
          - main
      schedule:
        # Scan quotidien à 2h du matin
        - cron: '0 2 * * *'
    
    env:
      DOCKER_REGISTRY: ghcr.io
      IMAGE_NAME: ${{ github.repository }}
    
    jobs:
      # Analyse statique du code (SAST)
      sast-scan:
        name: Static Application Security Testing
        runs-on: ubuntu-latest
        
        permissions:
          security-events: write
          contents: read
        
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          
          - name: Run Semgrep
            uses: returntocorp/semgrep-action@v1
            with:
              config: >-
                p/security-audit
                p/secrets
                p/owasp-top-ten
          
          - name: Run Trivy vulnerability scanner
            uses: aquasecurity/trivy-action@master
            with:
              scan-type: 'fs'
              scan-ref: '.'
              format: 'sarif'
              output: 'trivy-results.sarif'
          
          - name: Upload Trivy results to GitHub Security
            uses: github/codeql-action/upload-sarif@v3
            with:
              sarif_file: 'trivy-results.sarif'
      
      # Scan des dépendances
      dependency-scan:
        name: Dependency Vulnerability Scan
        runs-on: ubuntu-latest
        
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          
          - name: Run Snyk to check for vulnerabilities
            uses: snyk/actions/node@master
            env:
              SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
            with:
              args: --severity-threshold=high
          
          - name: OWASP Dependency Check
            uses: dependency-check/Dependency-Check_Action@main
            with:
              project: 'myapp'
              path: '.'
              format: 'HTML'
          
          - name: Upload Dependency Check results
            uses: actions/upload-artifact@v4
            with:
              name: dependency-check-report
              path: 'reports/'
      
      # Build et scan de l'image Docker
      docker-scan:
        name: Docker Image Security Scan
        runs-on: ubuntu-latest
        needs: [sast-scan, dependency-scan]
        
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          
          - name: Set up Docker Buildx
            uses: docker/setup-buildx-action@v3
          
          - name: Build Docker image
            uses: docker/build-push-action@v5
            with:
              context: .
              push: false
              tags: ${{ env.IMAGE_NAME }}:${{ github.sha }}
              cache-from: type=gha
              cache-to: type=gha,mode=max
          
          - name: Scan Docker image with Trivy
            uses: aquasecurity/trivy-action@master
            with:
              image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
              format: 'table'
              exit-code: '1'
              severity: 'CRITICAL,HIGH'
          
          - name: Scan with Grype
            uses: anchore/scan-action@v3
            with:
              image: ${{ env.IMAGE_NAME }}:${{ github.sha }}
              fail-build: true
              severity-cutoff: high
      
      # Analyse de configuration IaC
      iac-scan:
        name: Infrastructure as Code Security
        runs-on: ubuntu-latest
        
        steps:
          - name: Checkout code
            uses: actions/checkout@v4
          
          - name: Run Checkov
            uses: bridgecrewio/checkov-action@master
            with:
              directory: .
              framework: dockerfile,kubernetes
              output_format: sarif
              output_file_path: checkov-results.sarif
          
          - name: Upload Checkov results
            uses: github/codeql-action/upload-sarif@v3
            with:
              sarif_file: checkov-results.sarif
      
      # Notification des résultats
      notify:
        name: Send Security Report
        runs-on: ubuntu-latest
        needs: [sast-scan, dependency-scan, docker-scan, iac-scan]
        if: always()
        
        steps:
          - name: Send Slack notification
            uses: 8398a7/action-slack@v3
            with:
              status: ${{ job.status }}
              text: 'Security scan completed'
              webhook_url: ${{ secrets.SLACK_WEBHOOK }}
            if: always()
    ```

### Exemple 5 : Configuration Ansible (Hardening serveur)

!!! example "Exemple n°5 - Playbook Ansible de sécurisation"

    ```yaml
    ---
    - name: Linux Server Hardening
      hosts: all
      become: yes
      
      vars:
        ssh_port: 2222
        allowed_users:
          - alice
          - bob
        firewall_allowed_ports:
          - 22
          - 80
          - 443
        
        sysctl_config:
          # Protection IPv4
          net.ipv4.conf.all.rp_filter: 1
          net.ipv4.conf.default.rp_filter: 1
          net.ipv4.icmp_echo_ignore_broadcasts: 1
          net.ipv4.conf.all.accept_source_route: 0
          net.ipv4.conf.default.accept_source_route: 0
          net.ipv4.tcp_syncookies: 1
          
          # Protection IPv6
          net.ipv6.conf.all.accept_ra: 0
          net.ipv6.conf.default.accept_ra: 0
          net.ipv6.conf.all.accept_redirects: 0
          net.ipv6.conf.default.accept_redirects: 0
      
      tasks:
        # Mise à jour système
        - name: Update all packages
          apt:
            update_cache: yes
            upgrade: dist
            autoremove: yes
            autoclean: yes
          when: ansible_os_family == "Debian"
        
        # Configuration SSH sécurisée
        - name: Configure SSH daemon
          lineinfile:
            path: /etc/ssh/sshd_config
            regexp: "{{ item.regexp }}"
            line: "{{ item.line }}"
            state: present
          loop:
            - { regexp: '^Port', line: 'Port {{ ssh_port }}' }
            - { regexp: '^PermitRootLogin', line: 'PermitRootLogin no' }
            - { regexp: '^PasswordAuthentication', line: 'PasswordAuthentication no' }
            - { regexp: '^PubkeyAuthentication', line: 'PubkeyAuthentication yes' }
            - { regexp: '^X11Forwarding', line: 'X11Forwarding no' }
            - { regexp: '^MaxAuthTries', line: 'MaxAuthTries 3' }
            - { regexp: '^ClientAliveInterval', line: 'ClientAliveInterval 300' }
            - { regexp: '^ClientAliveCountMax', line: 'ClientAliveCountMax 2' }
          notify: restart sshd
        
        # Firewall UFW
        - name: Install UFW
          apt:
            name: ufw
            state: present
        
        - name: Configure UFW defaults
          ufw:
            direction: "{{ item.direction }}"
            policy: "{{ item.policy }}"
          loop:
            - { direction: 'incoming', policy: 'deny' }
            - { direction: 'outgoing', policy: 'allow' }
        
        - name: Allow SSH on custom port
          ufw:
            rule: allow
            port: "{{ ssh_port }}"
            proto: tcp
        
        - name: Allow specified ports
          ufw:
            rule: allow
            port: "{{ item }}"
            proto: tcp
          loop: "{{ firewall_allowed_ports }}"
        
        - name: Enable UFW
          ufw:
            state: enabled
        
        # Fail2ban
        - name: Install Fail2ban
          apt:
            name: fail2ban
            state: present
        
        - name: Configure Fail2ban jail
          template:
            src: jail.local.j2
            dest: /etc/fail2ban/jail.local
          notify: restart fail2ban
        
        # Sysctl hardening
        - name: Apply sysctl hardening
          sysctl:
            name: "{{ item.key }}"
            value: "{{ item.value }}"
            state: present
            reload: yes
          loop: "{{ sysctl_config | dict2items }}"
        
        # Audit avec auditd
        - name: Install auditd
          apt:
            name: auditd
            state: present
        
        - name: Configure audit rules
          copy:
            dest: /etc/audit/rules.d/hardening.rules
            content: |
              # Monitor authentication
              -w /var/log/auth.log -p wa -k auth
              -w /etc/passwd -p wa -k identity
              -w /etc/group -p wa -k identity
              -w /etc/shadow -p wa -k identity
              
              # Monitor network config
              -a always,exit -F arch=b64 -S sethostname -S setdomainname -k network_modifications
              
              # Monitor sudo usage
              -w /etc/sudoers -p wa -k sudoers_changes
              -w /var/log/sudo.log -p wa -k sudo_log
          notify: restart auditd
        
        # Désactiver services inutiles
        - name: Disable unnecessary services
          service:
            name: "{{ item }}"
            state: stopped
            enabled: no
          loop:
            - avahi-daemon
            - cups
            - bluetooth
          ignore_errors: yes
      
      handlers:
        - name: restart sshd
          service:
            name: sshd
            state: restarted
        
        - name: restart fail2ban
          service:
            name: fail2ban
            state: restarted
        
        - name: restart auditd
          service:
            name: auditd
            state: restarted
    ```

## Manipulation YAML par langage

### :fontawesome-brands-python: Python

**Lecture YAML (PyYAML) :**
```python
import yaml

# Lecture fichier YAML
with open('config.yaml', 'r', encoding='utf-8') as fichier:
    config = yaml.safe_load(fichier)

# Accès aux données
print(f"Nom: {config['nom']}")
print(f"Âge: {config['age']}")

# Navigation imbriquée
if 'adresse' in config:
    print(f"Ville: {config['adresse']['ville']}")

# Listes
for role in config.get('roles', []):
    print(f"  - {role}")
```

**Lecture de documents multiples :**
```python
import yaml

with open('multi_config.yaml', 'r', encoding='utf-8') as fichier:
    # load_all retourne un générateur
    documents = yaml.safe_load_all(fichier)
    
    for i, doc in enumerate(documents):
        print(f"\n=== Document {i+1} ===")
        print(f"Environment: {doc['environment']}")
        print(f"Database: {doc['database']['host']}")
```

**Écriture YAML :**
```python
import yaml

config = {
    'application': {
        'name': 'MyApp',
        'version': '1.0.0',
        'debug': False
    },
    'database': {
        'host': 'localhost',
        'port': 5432,
        'credentials': {
            'username': 'dbuser',
            'password': 'secret'  # À ne jamais faire en prod !
        }
    },
    'features': ['auth', 'api', 'admin']
}

# Écrire avec formatage par défaut
with open('output.yaml', 'w', encoding='utf-8') as fichier:
    yaml.dump(config, fichier, default_flow_style=False, allow_unicode=True)

# Personnaliser le formatage
with open('output_custom.yaml', 'w', encoding='utf-8') as fichier:
    yaml.dump(
        config, 
        fichier,
        default_flow_style=False,  # Style bloc (pas flux)
        sort_keys=False,            # Garder l'ordre
        allow_unicode=True,         # Caractères Unicode
        indent=2,                   # Indentation 2 espaces
        width=80                    # Largeur max ligne
    )
```

**Parser configuration Kubernetes :**
```python
import yaml

def analyser_network_policy(fichier_yaml):
    """Analyse les NetworkPolicy Kubernetes"""
    
    with open(fichier_yaml, 'r') as f:
        policies = yaml.safe_load_all(f)
        
        for policy in policies:
            if policy['kind'] != 'NetworkPolicy':
                continue
            
            name = policy['metadata']['name']
            namespace = policy['metadata']['namespace']
            
            print(f"\n📋 Policy: {name} (namespace: {namespace})")
            
            # Analyser ingress
            if 'ingress' in policy['spec']:
                print("  Ingress autorisé depuis:")
                for rule in policy['spec']['ingress']:
                    if 'from' in rule:
                        for source in rule['from']:
                            if 'podSelector' in source:
                                labels = source['podSelector'].get('matchLabels', {})
                                print(f"    - Pods: {labels}")
                    
                    if 'ports' in rule:
                        for port in rule['ports']:
                            print(f"      Port: {port['port']}/{port['protocol']}")
            
            # Analyser egress
            if 'egress' in policy['spec']:
                print("  Egress autorisé vers:")
                for rule in policy['spec']['egress']:
                    if 'to' in rule:
                        for dest in rule['to']:
                            print(f"    - {dest}")
                    if 'ports' in rule:
                        for port in rule['ports']:
                            print(f"      Port: {port.get('port', 'any')}/{port['protocol']}")

# Utilisation
analyser_network_policy('k8s_network_policies.yaml')
```

**Valider schéma YAML :**
```python
import yaml
from jsonschema import validate, ValidationError

# Schéma de validation
schema = {
    "type": "object",
    "required": ["nom", "prenom", "age"],
    "properties": {
        "nom": {"type": "string"},
        "prenom": {"type": "string"},
        "age": {"type": "integer", "minimum": 0, "maximum": 120},
        "email": {"type": "string", "format": "email"}
    }
}

def valider_yaml(fichier_yaml):
    with open(fichier_yaml, 'r') as f:
        data = yaml.safe_load(f)
    
    try:
        validate(instance=data, schema=schema)
        print("✅ YAML valide")
        return True
    except ValidationError as e:
        print(f"❌ Erreur de validation: {e.message}")
        return False

# Utilisation
valider_yaml('utilisateur.yaml')
```

### :fontawesome-brands-js: JavaScript (Node.js)

**Lecture YAML (js-yaml) :**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

// Installation : npm install js-yaml

// Lecture fichier YAML
try {
    const config = yaml.load(fs.readFileSync('config.yaml', 'utf8'));
    
    console.log(`Nom: ${config.nom}`);
    console.log(`Âge: ${config.age}`);
    
    // Listes
    if (config.roles) {
        config.roles.forEach(role => {
            console.log(`  - ${role}`);
        });
    }
} catch (err) {
    console.error('❌ Erreur YAML:', err);
}
```

**Lecture de documents multiples :**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

const fileContents = fs.readFileSync('multi_config.yaml', 'utf8');

// loadAll retourne un tableau
const documents = yaml.loadAll(fileContents);

documents.forEach((doc, index) => {
    console.log(`\n=== Document ${index + 1} ===`);
    console.log(`Environment: ${doc.environment}`);
    console.log(`Database: ${doc.database.host}`);
});
```

**Écriture YAML :**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

const config = {
    application: {
        name: 'MyApp',
        version: '1.0.0',
        debug: false
    },
    database: {
        host: 'localhost',
        port: 5432,
        credentials: {
            username: 'dbuser',
            password: 'secret'
        }
    },
    features: ['auth', 'api', 'admin']
};

// Convertir en YAML
const yamlStr = yaml.dump(config, {
    indent: 2,
    lineWidth: 80,
    noRefs: true,  // Pas d'ancres/références
    sortKeys: false
});

// Écrire fichier
fs.writeFileSync('output.yaml', yamlStr, 'utf8');
console.log('✅ Fichier YAML créé');
```

**Parser Docker Compose :**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

function analyserDockerCompose(fichierYaml) {
    const doc = yaml.load(fs.readFileSync(fichierYaml, 'utf8'));
    
    console.log('=== Services Docker Compose ===\n');
    
    Object.entries(doc.services).forEach(([name, service]) => {
        console.log(`📦 Service: ${name}`);
        console.log(`   Image: ${service.image || 'build local'}`);
        
        if (service.ports) {
            console.log(`   Ports exposés:`);
            service.ports.forEach(port => {
                console.log(`     - ${port}`);
            });
        }
        
        if (service.networks) {
            console.log(`   Réseaux: ${service.networks.join(', ')}`);
        }
        
        if (service.security_opt) {
            console.log(`   🔒 Options sécurité:`);
            service.security_opt.forEach(opt => {
                console.log(`     - ${opt}`);
            });
        }
        
        console.log('');
    });
}

// Utilisation
analyserDockerCompose('docker-compose.yaml');
```

**Validation avec schéma :**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');
const Ajv = require('ajv');

const ajv = new Ajv();

const schema = {
    type: 'object',
    required: ['nom', 'prenom', 'age'],
    properties: {
        nom: { type: 'string' },
        prenom: { type: 'string' },
        age: { type: 'integer', minimum: 0, maximum: 120 }
    }
};

function validerYaml(fichierYaml) {
    const data = yaml.load(fs.readFileSync(fichierYaml, 'utf8'));
    
    const validate = ajv.compile(schema);
    const valid = validate(data);
    
    if (valid) {
        console.log('✅ YAML valide');
        return true;
    } else {
        console.log('❌ Erreurs de validation:');
        validate.errors.forEach(err => {
            console.log(`  - ${err.instancePath} ${err.message}`);
        });
        return false;
    }
}

// Utilisation
validerYaml('utilisateur.yaml');
```

### :fontawesome-brands-php: PHP

**Lecture YAML (symfony/yaml) :**
```php
<?php
// Installation : composer require symfony/yaml

use Symfony\Component\Yaml\Yaml;

// Lecture fichier YAML
$config = Yaml::parseFile('config.yaml');

echo "Nom: " . $config['nom'] . "\n";
echo "Âge: " . $config['age'] . "\n";

// Listes
if (isset($config['roles'])) {
    foreach ($config['roles'] as $role) {
        echo "  - $role\n";
    }
}
?>
```

**Écriture YAML :**
```php
<?php
use Symfony\Component\Yaml\Yaml;

$config = [
    'application' => [
        'name' => 'MyApp',
        'version' => '1.0.0',
        'debug' => false
    ],
    'database' => [
        'host' => 'localhost',
        'port' => 5432,
        'credentials' => [
            'username' => 'dbuser',
            'password' => 'secret'
        ]
    ],
    'features' => ['auth', 'api', 'admin']
];

// Convertir en YAML
$yaml = Yaml::dump($config, 4, 2);

// Sauvegarder
file_put_contents('output.yaml', $yaml);
echo "✅ Fichier YAML créé\n";
?>
```

**Parser configuration CI/CD :**
```php
<?php
use Symfony\Component\Yaml\Yaml;

function analyserGitHubActions($fichierYaml) {
    $workflow = Yaml::parseFile($fichierYaml);
    
    echo "=== Workflow: {$workflow['name']} ===\n\n";
    
    // Analyser jobs
    foreach ($workflow['jobs'] as $jobName => $jobConfig) {
        echo "🔧 Job: $jobName\n";
        echo "   Runs on: {$jobConfig['runs-on']}\n";
        
        if (isset($jobConfig['steps'])) {
            echo "   Steps:\n";
            foreach ($jobConfig['steps'] as $step) {
                $name = $step['name'] ?? 'Unnamed step';
                echo "     - $name\n";
            }
        }
        
        echo "\n";
    }
}

// Utilisation
analyserGitHubActions('.github/workflows/security.yaml');
?>
```

### :fontawesome-brands-golang: Go (Golang)

**Lecture YAML (gopkg.in/yaml.v3) :**
```go
package main

import (
    "fmt"
    "os"
    
    "gopkg.in/yaml.v3"
)

type Config struct {
    Nom    string   `yaml:"nom"`
    Prenom string   `yaml:"prenom"`
    Age    int      `yaml:"age"`
    Actif  bool     `yaml:"actif"`
    Roles  []string `yaml:"roles"`
}

func main() {
    // Lire fichier
    data, err := os.ReadFile("config.yaml")
    if err != nil {
        panic(err)
    }
    
    // Parser YAML
    var config Config
    err = yaml.Unmarshal(data, &config)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Nom: %s\n", config.Nom)
    fmt.Printf("Âge: %d\n", config.Age)
    
    fmt.Println("Rôles:")
    for _, role := range config.Roles {
        fmt.Printf("  - %s\n", role)
    }
}
```

**Structures imbriquées complexes :**
```go
package main

import (
    "fmt"
    "os"
    
    "gopkg.in/yaml.v3"
)

type DockerCompose struct {
    Version  string             `yaml:"version"`
    Services map[string]Service `yaml:"services"`
    Networks map[string]Network `yaml:"networks"`
}

type Service struct {
    Image       string            `yaml:"image"`
    ContainerName string          `yaml:"container_name"`
    Ports       []string          `yaml:"ports"`
    Networks    []string          `yaml:"networks"`
    Environment map[string]string `yaml:"environment"`
    SecurityOpt []string          `yaml:"security_opt"`
}

type Network struct {
    Driver   string `yaml:"driver"`
    Internal bool   `yaml:"internal"`
}

func main() {
    data, _ := os.ReadFile("docker-compose.yaml")
    
    var compose DockerCompose
    yaml.Unmarshal(data, &compose)
    
    fmt.Println("=== Services Docker Compose ===\n")
    
    for name, service := range compose.Services {
        fmt.Printf("📦 Service: %s\n", name)
        fmt.Printf("   Image: %s\n", service.Image)
        
        if len(service.Ports) > 0 {
            fmt.Println("   Ports exposés:")
            for _, port := range service.Ports {
                fmt.Printf("     - %s\n", port)
            }
        }
        
        if len(service.SecurityOpt) > 0 {
            fmt.Println("   🔒 Options sécurité:")
            for _, opt := range service.SecurityOpt {
                fmt.Printf("     - %s\n", opt)
            }
        }
        
        fmt.Println()
    }
}
```

**Écriture YAML :**
```go
package main

import (
    "os"
    
    "gopkg.in/yaml.v3"
)

type Config struct {
    Application struct {
        Name    string `yaml:"name"`
        Version string `yaml:"version"`
        Debug   bool   `yaml:"debug"`
    } `yaml:"application"`
    Database struct {
        Host string `yaml:"host"`
        Port int    `yaml:"port"`
    } `yaml:"database"`
    Features []string `yaml:"features"`
}

func main() {
    config := Config{}
    config.Application.Name = "MyApp"
    config.Application.Version = "1.0.0"
    config.Application.Debug = false
    config.Database.Host = "localhost"
    config.Database.Port = 5432
    config.Features = []string{"auth", "api", "admin"}
    
    // Marshaler en YAML
    yamlData, err := yaml.Marshal(&config)
    if err != nil {
        panic(err)
    }
    
    // Écrire fichier
    err = os.WriteFile("output.yaml", yamlData, 0644)
    if err != nil {
        panic(err)
    }
    
    fmt.Println("✅ Fichier YAML créé")
}
```

### :fontawesome-brands-rust: Rust

**Lecture YAML (serde_yaml) :**
```rust
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Deserialize)]
struct Config {
    nom: String,
    prenom: String,
    age: u32,
    actif: bool,
    roles: Vec<String>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Lire fichier
    let data = fs::read_to_string("config.yaml")?;
    
    // Parser YAML
    let config: Config = serde_yaml::from_str(&data)?;
    
    println!("Nom: {}", config.nom);
    println!("Âge: {}", config.age);
    
    println!("Rôles:");
    for role in &config.roles {
        println!("  - {}", role);
    }
    
    Ok(())
}
```

**Structures imbriquées :**
```rust
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

#[derive(Debug, Deserialize)]
struct DockerCompose {
    version: String,
    services: HashMap<String, Service>,
    networks: Option<HashMap<String, Network>>,
}

#[derive(Debug, Deserialize)]
struct Service {
    image: Option<String>,
    container_name: Option<String>,
    ports: Option<Vec<String>>,
    networks: Option<Vec<String>>,
    security_opt: Option<Vec<String>>,
}

#[derive(Debug, Deserialize)]
struct Network {
    driver: String,
    internal: Option<bool>,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string("docker-compose.yaml")?;
    let compose: DockerCompose = serde_yaml::from_str(&data)?;
    
    println!("=== Services Docker Compose ===\n");
    
    for (name, service) in &compose.services {
        println!("📦 Service: {}", name);
        
        if let Some(image) = &service.image {
            println!("   Image: {}", image);
        }
        
        if let Some(ports) = &service.ports {
            println!("   Ports exposés:");
            for port in ports {
                println!("     - {}", port);
            }
        }
        
        if let Some(security) = &service.security_opt {
            println!("   🔒 Options sécurité:");
            for opt in security {
                println!("     - {}", opt);
            }
        }
        
        println!();
    }
    
    Ok(())
}
```

**Écriture YAML :**
```rust
use serde::{Deserialize, Serialize};
use std::fs;

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    application: Application,
    database: Database,
    features: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Application {
    name: String,
    version: String,
    debug: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct Database {
    host: String,
    port: u16,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = Config {
        application: Application {
            name: "MyApp".to_string(),
            version: "1.0.0".to_string(),
            debug: false,
        },
        database: Database {
            host: "localhost".to_string(),
            port: 5432,
        },
        features: vec![
            "auth".to_string(),
            "api".to_string(),
            "admin".to_string(),
        ],
    };
    
    // Sérialiser en YAML
    let yaml_data = serde_yaml::to_string(&config)?;
    
    // Écrire fichier
    fs::write("output.yaml", yaml_data)?;
    
    println!("✅ Fichier YAML créé");
    
    Ok(())
}
```

## Bonnes pratiques

### Indentation et style

!!! success "Règles d'or"
    - **2 espaces** pour l'indentation (standard DevOps)
    - **JAMAIS de tabulations**
    - **Cohérence** : même indentation dans tout le fichier
    - **Commentaires** explicites pour les valeurs non évidentes
    - **Ancres** (`&`, `*`) pour éviter la duplication

### Sécurité

!!! danger "Secrets et données sensibles"
    - ❌ **Ne JAMAIS** commiter de secrets en clair dans YAML
    - ✅ Utiliser **variables d'environnement** : `${DB_PASSWORD}`
    - ✅ Utiliser **secrets managers** : Vault, AWS Secrets Manager
    - ✅ Chiffrer avec **SOPS**, **git-crypt**, **ansible-vault**
    - ✅ Utiliser **`.gitignore`** pour exclure fichiers sensibles

**Exemple avec variables d'environnement :**
```yaml
database:
  host: ${DB_HOST:-localhost}
  port: ${DB_PORT:-5432}
  username: ${DB_USER}
  password: ${DB_PASSWORD}  # Injecté au runtime
```

### Validation

**Utiliser des linters YAML :**
```bash
# yamllint (Python)
pip install yamllint
yamllint config.yaml

# Configuration .yamllint
---
extends: default

rules:
  line-length:
    max: 120
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

**Valider schémas Kubernetes :**
```bash
# kubeval
kubeval deployment.yaml

# kube-score
kube-score score deployment.yaml
```

### Erreurs courantes

!!! warning "Pièges fréquents"
    - **Tabulations** au lieu d'espaces → ERREUR FATALE
    - **Indentation incohérente** → Parsing échoue
    - **Oublier les deux-points** après clé → Erreur syntaxe
    - **Chaînes multi-lignes** mal formatées (`|` vs `>`)
    - **Ancres mal référencées** → Valeurs manquantes
    - **Types mal interprétés** : `yes` devient `true`, `123` devient nombre

## Le mot de la fin

!!! quote
    **YAML a révolutionné la configuration d'infrastructure** en rendant les fichiers de configuration **lisibles par les humains** sans sacrifier la puissance d'expression. Son adoption massive par **Kubernetes, Docker, Ansible, et les pipelines CI/CD** en a fait le langage universel de l'infrastructure as code.
    
    Chaque langage offre des bibliothèques robustes pour manipuler YAML :
    
    - **Python** avec `PyYAML` pour scripting et automation
    - **JavaScript** avec `js-yaml` pour tooling Node.js
    - **PHP** avec `symfony/yaml` pour applications web
    - **Go** avec `gopkg.in/yaml.v3` pour outils DevOps
    - **Rust** avec `serde_yaml` pour performance et sûreté
    
    Maîtriser YAML c'est comprendre que **l'indentation est sémantique** (contrairement à JSON), que les **commentaires sont essentiels** pour la documentation, et que les **ancres/références** évitent la duplication. Pour la configuration d'infrastructure moderne, YAML est devenu **incontournable**.

---
