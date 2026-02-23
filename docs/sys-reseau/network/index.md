# Réseaux

    # ========================================================================
    # Réseaux
    # ========================================================================
    # Mise en œuvre opérationnelle des services réseau et outils de diagnostic.
    # ========================================================================
    {"Réseaux" = [
      "sys-reseau/network/index.md",

      # ---------------------------------------------------------------------
      # Outils d’analyse réseau
      # ---------------------------------------------------------------------
      # Outils de diagnostic, capture et inspection du trafic.
      {"Outils & Analyse" = [
        "sys-reseau/network/outils/index.md",

        {"nslookup" = "sys-reseau/network/outils/nslookup.md"},
        {"netstat"  = "sys-reseau/network/outils/netstat.md"},
        {"tcpdump"  = "sys-reseau/network/outils/tcpdump.md"},
        {"scapy"    = "sys-reseau/network/outils/scapy.md"}
      ]},

      # ---------------------------------------------------------------------
      # Services réseau
      # ---------------------------------------------------------------------
      # Déploiement et administration des services d’infrastructure.
      {"Services réseau" = [
        "sys-reseau/network/services/index.md",

        {"DNS"        = "sys-reseau/network/services/dns.md"},
        {"SSH"        = "sys-reseau/network/services/ssh.md"},
        {"FTP"        = "sys-reseau/network/services/ftp.md"},
        {"Samba"      = "sys-reseau/network/services/samba.md"},
        {"LDAP & PAM" = "sys-reseau/network/services/ldap-pam.md"}
      ]},

      # ---------------------------------------------------------------------
      # Sécurité périmétrique
      # ---------------------------------------------------------------------
      # Protection du périmètre réseau et contrôle des flux.
      {"Sécurité périmétrique" = [
        "sys-reseau/network/security/index.md",

        {"pfSense" = "sys-reseau/network/security/pfsense.md"},
        {"WAF"     = "sys-reseau/network/security/waf.md"},
        {"OpenVPN" = "sys-reseau/network/security/openvpn.md"},
        {"HAProxy" = "sys-reseau/network/security/haproxy.md"}
      ]}
    ]},

<br />