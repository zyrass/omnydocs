# Cyber : Outils & Red Team

    # ============================================================================
    # 6 — CYBERSÉCURITÉ : OUTILS & RED TEAM
    # ============================================================================
    # Cette section couvre l’arsenal technique offensif ainsi que les
    # méthodologies de tests d’intrusion et d’opérations Red Team.
    #
    # Elle traite notamment :
    # - la reconnaissance et l’OSINT
    # - le pentest applicatif Web/API
    # - le pentest réseau et Active Directory
    # - l’exploitation et la post-exploitation
    # - les attaques sur les mots de passe
    # - l’ingénierie sociale
    # - les scanners de vulnérabilités
    # - les frameworks méthodologiques offensifs
    #
    # Contrairement à la section Défense (SOC/DFIR), cette partie est orientée
    # simulation d’attaques, reproduction de scénarios adverses et audit offensif.
    #
    # PUBLIC CIBLE :
    # - Pentesters
    # - Red Teamers
    # - Ethical Hackers
    # - Consultants en sécurité offensive
    # ============================================================================

    {"Cyber : Attaque" = [
        "cyber/tools/index.md",

        # ========================================================================
        # 6.1 — OSINT & Reconnaissance
        # ========================================================================
        # Phase de collecte d’informations publiques (reconnaissance passive).
        #
        # Objectifs :
        # - cartographier la surface d’attaque externe
        # - identifier les actifs exposés
        # - collecter des informations sur la cible
        #
        # Cette phase précède toute interaction intrusive.
        # ========================================================================
        {"OSINT & Reconnaissance" = [
        "cyber/tools/osint/index.md",
        # {"theHarvester" = "cyber/tools/osint/theharvester.md"},
        # {"Maltego"      = "cyber/tools/osint/maltego.md"},
        # {"SpiderFoot"   = "cyber/tools/osint/spiderfoot.md"},
        # {"Amass"        = "cyber/tools/osint/amass.md"},
        # {"Shodan"       = "cyber/tools/osint/shodan-censys.md"},
        ]},

        # ========================================================================
        # 6.2 — Pentest Web & API
        # ========================================================================
        # Tests d’intrusion applicatifs visant les applications Web et API.
        #
        # Couvre notamment :
        # - OWASP Top 10
        # - fuzzing de paramètres
        # - énumération de contenus
        # - analyse de logique métier
        #
        # Domaine critique pour les environnements exposés Internet.
        # ========================================================================
        {"Pentest Web & API" = [
        "cyber/tools/web/index.md",
        # {"Burp Suite" = "cyber/tools/web/burp.md"},
        # {"OWASP ZAP"  = "cyber/tools/web/zap.md"},
        # {"Nikto"      = "cyber/tools/web/nikto.md"},
        # {"ffuf"       = "cyber/tools/web/ffuf.md"},
        # {"Gobuster"   = "cyber/tools/web/gobuster.md"},
        ]},

        # ========================================================================
        # 6.3 — Pentest Réseau & Services
        # ========================================================================
        # Reconnaissance active et exploitation des services réseau.
        #
        # Objectifs :
        # - découverte d’hôtes
        # - énumération de services
        # - attaques de protocoles
        # - pivoting réseau
        # - attaques Active Directory
        # ========================================================================
        {"Pentest Réseau & Services" = [
        "cyber/tools/network/index.md",

        # ---------------------------------------------------------------------
        # DNS — Outils d’interrogation
        # ---------------------------------------------------------------------
        # Utilisés pour la reconnaissance d’infrastructure.
        {"DNS" = [
            "cyber/tools/network/dns/index.md",
            {"dig"      = "cyber/tools/network/dns/dig.md"},
            {"nslookup" = "cyber/tools/network/dns/nslookup.md"},
            {"host"     = "cyber/tools/network/dns/host.md"},
        ]},

        # ---------------------------------------------------------------------
        # Connectivité
        # ---------------------------------------------------------------------
        {"ping" = "cyber/tools/network/ping.md"},
        ]},

        # ========================================================================
        # 6.4 — Exploitation & Post-Exploitation
        # ========================================================================
        # Phase d’exploitation après identification d’une vulnérabilité.
        #
        # Couvre :
        # - exploitation initiale
        # - élévation de privilèges
        # - persistance
        # - pivoting
        # - exfiltration
        # ========================================================================
        {"Exploitation & Post-Exploit" = [
        "cyber/tools/exploit/index.md",
        # {"Metasploit" = "cyber/tools/exploit/metasploit.md"},
        # {"Msfvenom"   = "cyber/tools/exploit/msfvenom.md"},
        # {"LinPEAS"    = "cyber/tools/exploit/peas.md"},
        ]},

        # ========================================================================
        # 6.5 — Password Attacks
        # ========================================================================
        # Techniques d’attaque contre les mécanismes d’authentification.
        #
        # Inclut :
        # - bruteforce en ligne
        # - cracking hors ligne
        # - attaques par dictionnaire
        # - génération de wordlists
        # ========================================================================
        {"Password Attacks" = [
        "cyber/tools/crack/index.md",
        # {"John the Ripper" = "cyber/tools/crack/john.md"},
        # {"Hashcat"         = "cyber/tools/crack/hashcat.md"},
        # {"Hydra"           = "cyber/tools/crack/hydra.md"},
        # {"Medusa"          = "cyber/tools/crack/medusa.md"},
        # {"CeWL"            = "cyber/tools/crack/cewl.md"},
        ]},

        # ========================================================================
        # 6.6 — Social Engineering
        # ========================================================================
        # Techniques de manipulation humaine visant à contourner
        # les contrôles techniques.
        #
        # Inclut :
        # - phishing / spear-phishing
        # - pretexting
        # - campagnes de sensibilisation simulées
        # ========================================================================
        {"Social Engineering" = [
        "cyber/tools/se/index.md",
        # {"SET"     = "cyber/tools/se/set.md"},
        # {"GoPhish" = "cyber/tools/se/gophish.md"},
        ]},

        # ========================================================================
        # 6.7 — Scan de Vulnérabilités
        # ========================================================================
        # Outils automatisés d’identification de vulnérabilités.
        #
        # NOTE :
        # - utilisés en phase d’audit technique
        # - à corréler avec la gestion des vulnérabilités côté GRC
        # ========================================================================
        {"Scan de Vulnérabilités" = [
        "cyber/tools/scan/index.md",
        # {"OpenVAS" = "cyber/tools/scan/openvas.md"},
        # {"Nessus"  = "cyber/tools/scan/nessus.md"},
        # {"Nuclei"  = "cyber/tools/scan/nuclei.md"},
        ]},

        # ========================================================================
        # 6.8 — Méthodologies Red Team
        # ========================================================================
        # Cadres méthodologiques des opérations offensives.
        #
        # Objectifs :
        # - structurer les campagnes Red Team
        # - aligner sur MITRE ATT&CK
        # - formaliser les phases de pentest
        # - intégrer les notions d’OpSec
        # ========================================================================
        {"Méthodologies Red Team" = [
        "cyber/tools/methodology/index.md",
        # {"MITRE ATT&CK" = "cyber/tools/methodology/mitre-attack.md"},
        # {"OpSec"        = "cyber/tools/methodology/opsec-tor.md"},
        # {"C2"           = "cyber/tools/methodology/c2-frameworks.md"},
        ]}
    ]},

<br />