# Acquisition
    
    # --- Acquisition ---
    # Techniques et outils pour acquérir des preuves numériques
    # sans altérer l'intégrité des données (chaîne de preuve).
    
      # --- Outils de copie bit-à-bit ---
      # dd : outil Unix standard pour la copie de données brutes.
      # dc3dd : fork forensic de dd avec hashing intégré et logging avancé.
      # Usage recommandé :
      #   - dd : copies génériques, backups, clonage système
      #   - dc3dd : acquisitions forensic légales avec vérification d'intégrité
      
      dd / dc3dd          - Copie bit-à-bit (forensic-sound)
      
      LiME (Mémoire)      - Linux Memory Extractor
      Guymager            - Outil GUI pour acquisition forensic
    