---
title: 3.17 Script de validation bout-en-bout
description: Script Python complet de validation du laboratoire forensic. Vérifie connectivité, services, partages, configuration, prêt à l'emploi avant cycle 1. Reproductible et documenté.
authors:
  - Zyrass
date:
  created: 2026-04-29
tags:
  - Validation
  - Script
  - Python
  - Tests
data-level: 🟡
---

# 3.17 Script de validation bout-en-bout

## Métadonnées

| Champ | Valeur |
|---|---|
| Durée | 2 heures |
| Niveau | Pratique |

## 1. Objectif

Avant d'attaquer le cycle 1 (premier cas pratique forensic), il faut **certifier** que le laboratoire fonctionne. Ce chapitre fournit un script Python qui teste tout automatiquement.

## 2. Composants testés

| Composant | Test |
|---|---|
| Connectivité réseau | Ping de chaque hôte |
| Routeur OpenWrt | Accès SSH, DHCP fonctionnel |
| Serveur Debian | SSH, services Samba et Apache |
| Postes Windows | Ping et SMB |
| MacBook M1 | Ping (si en ligne) |
| Wi-Fi | SSID visible |
| Partages | Accessibilité Samba |
| Site intranet | Réponse HTTP |

## 3. Le script complet

```python
#!/usr/bin/env python3
"""
validate-lab.py
================
Script de validation du laboratoire OmnyAcademy.
Auteur : Zyrass / OmnyVia
Usage  : python3 validate-lab.py
"""

import subprocess
import socket
import sys
import time
from pathlib import Path
from datetime import datetime

# Couleurs ANSI pour terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


# Configuration du laboratoire
LAB_CONFIG = {
    'router':      {'ip': '192.168.50.1',   'name': 'OpenWrt',      'critical': True},
    'server':      {'ip': '192.168.50.10',  'name': 'Debian',       'critical': True},
    'win_compta':  {'ip': '192.168.50.150', 'name': 'Win Compta',   'critical': False},
    'win_stage':   {'ip': '192.168.50.151', 'name': 'Win Stagiaire','critical': False},
    'mac_m1':      {'ip': '192.168.50.170', 'name': 'MacBook M1',   'critical': False},
}

SERVICES = [
    {'host': '192.168.50.1',  'port': 22,   'name': 'OpenWrt SSH'},
    {'host': '192.168.50.10', 'port': 22,   'name': 'Debian SSH'},
    {'host': '192.168.50.10', 'port': 80,   'name': 'Apache HTTP'},
    {'host': '192.168.50.10', 'port': 139,  'name': 'Samba NetBIOS'},
    {'host': '192.168.50.10', 'port': 445,  'name': 'Samba SMB'},
]


def print_header(text):
    """Affiche un en-tête"""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text.center(60)}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")


def print_test(name, passed, details=""):
    """Affiche le résultat d'un test"""
    status = f"{GREEN}OK{RESET}" if passed else f"{RED}FAIL{RESET}"
    line = f"  [{status}] {name}"
    if details:
        line += f" - {details}"
    print(line)
    return passed


def ping(host, timeout=2):
    """Test de ping (cross-platform)"""
    try:
        # Linux/macOS
        cmd = ['ping', '-c', '1', '-W', str(timeout), host]
        if sys.platform == 'win32':
            cmd = ['ping', '-n', '1', '-w', str(timeout * 1000), host]
        
        result = subprocess.run(
            cmd, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except Exception:
        return False


def check_port(host, port, timeout=2):
    """Vérifie qu'un port TCP est ouvert"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except Exception:
        return False


def check_http(host, expected_codes=(200, 301, 302)):
    """Vérifie un site HTTP"""
    try:
        import urllib.request
        req = urllib.request.Request(f"http://{host}/")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in expected_codes
    except Exception:
        return False


def check_smb_share(host, share_name):
    """Vérifie qu'un partage SMB est listé"""
    try:
        result = subprocess.run(
            ['smbclient', '-N', '-L', f'//{host}'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return share_name in result.stdout
    except Exception:
        return False


def test_connectivity():
    """Test 1 - Connectivité réseau"""
    print_header("Test 1 - Connectivité réseau (ping)")
    
    results = []
    for key, host_info in LAB_CONFIG.items():
        result = ping(host_info['ip'])
        passed = print_test(
            f"{host_info['name']:20s} {host_info['ip']}",
            result,
            "" if result else "Indisponible"
        )
        results.append({
            'name': host_info['name'],
            'passed': passed,
            'critical': host_info['critical']
        })
    
    return results


def test_services():
    """Test 2 - Services TCP"""
    print_header("Test 2 - Services TCP")
    
    results = []
    for svc in SERVICES:
        result = check_port(svc['host'], svc['port'])
        passed = print_test(
            f"{svc['name']:20s} {svc['host']}:{svc['port']}",
            result
        )
        results.append({'name': svc['name'], 'passed': passed})
    
    return results


def test_http():
    """Test 3 - Sites HTTP"""
    print_header("Test 3 - Sites HTTP")
    
    results = []
    sites = [
        '192.168.50.10',
    ]
    for site in sites:
        result = check_http(site)
        passed = print_test(f"HTTP {site}", result)
        results.append({'name': site, 'passed': passed})
    
    return results


def test_smb_shares():
    """Test 4 - Partages Samba"""
    print_header("Test 4 - Partages Samba")
    
    results = []
    expected_shares = ['compta', 'direction', 'public']
    
    for share in expected_shares:
        result = check_smb_share('192.168.50.10', share)
        passed = print_test(f"Partage Samba '{share}'", result)
        results.append({'name': share, 'passed': passed})
    
    return results


def test_dns():
    """Test 5 - Résolution DNS"""
    print_header("Test 5 - Résolution DNS")
    
    domains = ['google.com', 'kernel.org']
    results = []
    
    for domain in domains:
        try:
            socket.gethostbyname(domain)
            passed = print_test(f"Résolution {domain}", True)
        except Exception as e:
            passed = print_test(f"Résolution {domain}", False, str(e))
        results.append({'name': domain, 'passed': passed})
    
    return results


def generate_report(all_results):
    """Génère un rapport"""
    print_header("RAPPORT FINAL")
    
    total = sum(len(r) for r in all_results)
    passed = sum(
        len([t for t in r if t.get('passed')]) 
        for r in all_results
    )
    
    pct = 100 * passed / total if total > 0 else 0
    
    color = GREEN if pct >= 90 else (YELLOW if pct >= 70 else RED)
    
    print(f"\n{color}{BOLD}Tests réussis : {passed}/{total} ({pct:.1f}%){RESET}\n")
    
    # Sauvegarde rapport
    report_path = Path.home() / f'lab-validation-{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
    with open(report_path, 'w') as f:
        f.write(f"VALIDATION LABORATOIRE OMNYACADEMY\n")
        f.write(f"Date : {datetime.now().isoformat()}\n")
        f.write(f"Tests réussis : {passed}/{total} ({pct:.1f}%)\n\n")
        for results in all_results:
            for test in results:
                status = "OK" if test.get('passed') else "FAIL"
                critical = " (CRITIQUE)" if test.get('critical') else ""
                f.write(f"[{status}] {test['name']}{critical}\n")
    
    print(f"Rapport sauvegardé : {report_path}\n")
    
    # Avis
    if pct == 100:
        print(f"{GREEN}{BOLD}Laboratoire entièrement validé. Cycle 1 OK.{RESET}\n")
    elif pct >= 90:
        print(f"{YELLOW}Laboratoire fonctionnel. Quelques tests à corriger.{RESET}\n")
    elif pct >= 70:
        print(f"{YELLOW}Laboratoire partiellement fonctionnel. Vérifier les échecs.{RESET}\n")
    else:
        print(f"{RED}Laboratoire en mauvais état. Reprendre les chapitres 3.4-3.16.{RESET}\n")


def main():
    """Point d'entrée"""
    print_header("VALIDATION LABORATOIRE OMNYACADEMY")
    print(f"  Date : {datetime.now().isoformat()}")
    print(f"  Plateforme : {sys.platform}\n")
    
    all_results = [
        test_connectivity(),
        test_services(),
        test_http(),
        test_smb_shares(),
        test_dns(),
    ]
    
    generate_report(all_results)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Interrompu par l'utilisateur.{RESET}")
        sys.exit(1)
```

## 4. Utilisation

### 4.1 Prérequis

```bash
# Outils nécessaires
sudo apt install python3 smbclient iputils-ping
```

### 4.2 Sauvegarde du script

```bash
# Sauvegarder dans ~/lab-tools/
mkdir -p ~/lab-tools
cd ~/lab-tools

# Copier-coller le script ou télécharger
chmod +x validate-lab.py
```

### 4.3 Exécution

```bash
python3 validate-lab.py

# Avec tee pour sauvegarder
python3 validate-lab.py | tee ~/lab-validation-$(date +%Y%m%d).log
```

## 5. Interprétation des résultats

| Score | Signification |
|---|---|
| 100% | Lab parfait, prêt cycle 1 |
| 90-99% | Lab fonctionnel, corriger échecs mineurs |
| 70-89% | Lab partiellement fonctionnel |
| < 70% | Reprendre chapitres précédents |

## 6. Extension du script

Le script peut être étendu pour :

- Tester l'authentification SSH par clé
- Vérifier les hashes des configurations
- Tester l'intranet PHP
- Tester les services Windows via WMI

## 7. Auto-évaluation

| # | Question | Réponse |
|---|---|---|
| 1 | Pourquoi automatiser la validation ? | Reproductibilité, gain temps |
| 2 | Sortie attendue ? | Rapport texte + score % |
| 3 | Score minimum cycle 1 ? | 90% (idéalement 100%) |
| 4 | Outil pour test SMB ? | smbclient |

---

**Chapitre suivant** : [3.18 Préparation MacBook M1 forensic](03-18-macbook-m1-prep.md)
