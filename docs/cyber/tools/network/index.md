# Pentest Réseau & Services

    # -------------------------------------------------------------------------
    # Pentest Réseau & Services
    # Découverte réseau, énumération de services, exploitation de protocoles,
    # pivoting, attaques Active Directory, Man-in-the-Middle.
    # -------------------------------------------------------------------------
    
      Nmap (NSE)            - Scanner de ports et énumération de services (scripts NSE)
      
      # --- Outils DNS ---
      # Suite d'outils pour interroger les serveurs DNS et effectuer de la
      # reconnaissance sur les infrastructures réseau.
      DNS Tools
        
        dig                 - Outil DNS flexible et complet (BIND)
        dog                 - Alternative moderne à dig, écrite en Rust (colorisation, JSON)
        nslookup            - Outil DNS legacy, multiplateforme (Windows/Linux)
        host                - Outil DNS simple pour résolutions A/AAAA/MX/TXT
      
      ping                  - Test de connectivité ICMP
      Scapy                 - Manipulation de paquets réseau (Python)
      Impacket              - Suite d'outils Python pour protocoles Windows (SMB, LDAP, Kerberos)
      CrackMapExec          - Exploitation et énumération multi-protocoles (SMB, WinRM, LDAP, MSSQL)
      Responder             - Poisoning LLMNR/NBT-NS pour capture de hashes
      BloodHound (AD)       - Cartographie et exploitation Active Directory (chemins d'escalade)
      
      # NOTE : Les outils ci-dessous sont également référencés dans "Systèmes & Réseaux".
      # Ils sont listés ici car utilisés dans un contexte offensif (Red Team).
      # À terme, tu pourras choisir de :
      # - Conserver cette duplication avec un focus offensif ici
      # - Rediriger vers sys-reseau avec un lien explicite
      
      # OpenVPN              - VPN open-source (usage : tunneling, pivoting)
      # HAProxy              - Load balancer / reverse proxy (usage : infrastructure Red Team)
      # pfSense              - Firewall/routeur open-source (usage : lab sécurisé)
    