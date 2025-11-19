# Architecture SOC

    # -------------------------------------------------------------------------
    # Architecture SOC
    # Composantes techniques d'un SOC moderne : solutions de détection,
    # corrélation d'événements, threat intelligence, monitoring réseau.
    # -------------------------------------------------------------------------
    
      SIEM (Wazuh)           - Security Information and Event Management
      EDR/XDR                - Endpoint Detection & Response / Extended Detection & Response
      NDR (Zeek/Arkime)      - Network Detection & Response
  
      # --- Systèmes de Détection/Prévention d'Intrusion ---
      # IDS/IPS basés sur signatures et anomalies pour détecter et bloquer
      # les activités malveillantes sur le réseau.
      
        Suricata              - IDS/IPS moderne multi-thread (OISF) - recommandé
        Snort                 - IDS/IPS historique (Cisco/Sourcefire) - Snort 2.x et 3.x
      
      TIP (MISP/OpenCTI)      - Threat Intelligence Platform
      ntopng (Monitoring)     - Network Traffic Monitoring