---
description: "Astreintes SOC (On-Call) — Organiser les rotations d'astreinte, prévenir le burn-out, outils d'alerte et meilleures pratiques pour la couverture 24/7."
icon: lucide/book-open-check
tags: ["ON-CALL", "ASTREINTE", "SOC", "PAGERDUST", "BURN-OUT", "ROTATION", "GESTION"]
---

# Astreintes SOC — Organisation On-Call

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="2025"
  data-time="~1-2 heures">
</div>

## Introduction

!!! quote "Analogie pédagogique — Le Médecin de Garde"
    Un hôpital ne ferme pas la nuit. Il y a toujours un médecin de garde disponible — mais ce n'est pas le même médecin 7 jours sur 7. Les **rotations d'astreinte** garantissent la continuité du service sans épuiser les équipes. Un SOC fonctionne de la même manière : les attaques ne respectent pas les horaires de bureau, mais l'équipe, si.

Les **astreintes SOC** (on-call) organisent la disponibilité des analystes en dehors des heures ouvrées pour répondre aux incidents P1 et P2.

<br>

---

## Modèles de couverture SOC

| Modèle | Description | Adapté pour |
|---|---|---|
| **Follow-the-Sun** | 3 équipes dans 3 fuseaux horaires différents | Grandes organisations internationales |
| **SOC 24/7** | Une équipe sur place en permanence (3×8) | Organisations critiques (OIV, banques) |
| **SOC heures ouvrées + Astreinte** | Équipe le jour + analyste on-call la nuit/WE | PME, startups, SOC intermédiaires |
| **SOC managé (MSSP)** | Externalisation partielle ou totale de la surveillance | Organisations sans ressources internes |

<br>

---

## Organisation des rotations

### Principes essentiels

!!! tip "Bonnes pratiques d'astreinte"
    - **Maximum 1 semaine** d'astreinte consécutive par analyste
    - **Délai de prise en charge** : 15 minutes pour les P1 (notifications configurées en cascade)
    - **Compensation claire** : heures supplémentaires, repos compensateur, prime d'astreinte
    - **Procédure d'escalade** : si l'analyste ne répond pas en 5 min → manager → RSSI
    - **Runbook accessible** : les playbooks doivent être accessibles sur mobile

### Calendrier de rotation (exemple trimestriel)

```text title="Rotation d'astreinte — Équipe de 4 analystes"
Semaine 1  : Analyste A (astreinte) + Analyste B (backup)
Semaine 2  : Analyste C (astreinte) + Analyste D (backup)
Semaine 3  : Analyste B (astreinte) + Analyste A (backup)
Semaine 4  : Analyste D (astreinte) + Analyste C (backup)
→ Chaque analyste est d'astreinte 1 semaine sur 4
→ Chaque analyste est backup 1 semaine sur 4
→ 2 semaines "libres" de toute astreinte par mois
```

<br>

---

## Outils d'alerting On-Call

### Grafana OnCall (open-source)

```bash title="Installation Grafana OnCall — Docker"
git clone https://github.com/grafana/oncall
cd oncall

# Configurer les variables d'environnement
cp .env.example .env
nano .env  # Définir SECRET_KEY, GRAFANA_API_URL

# Démarrer
docker compose up -d

# Grafana OnCall s'intègre nativement avec Grafana et permet :
# - Création de calendriers de rotation
# - Escalades configurables (5 min sans réponse → manager)
# - Intégrations : PagerDuty, OpsGenie, Slack, Telegram
```

### Configuration d'escalade

```yaml title="Politique d'escalade — Grafana OnCall"
escalation_policy:
  name: "SOC P1 Critical"
  steps:
    - type: notify_person_next_each_time
      delay: 0          # Notification immédiate
      persons:
        - analyst_on_call

    - type: notify_person_next_each_time
      delay: 5          # Après 5 min sans réponse
      persons:
        - soc_manager

    - type: notify_person_next_each_time
      delay: 10         # Après 10 min sans réponse
      persons:
        - ciso

    - type: notify_all_from_team
      delay: 15         # Mobilisation complète après 15 min
      team: soc_team
```

<br>

---

## Prévenir le burn-out des analystes

Le métier d'analyste SOC a un **taux de burn-out élevé** (jusqu'à 65% selon les études) lié à la pression constante et au volume d'alertes.

!!! warning "Signaux d'alarme à surveiller"
    - Analyste qui ne prend plus de pauses
    - Erreurs de qualification en augmentation
    - Commentaires cyniques sur les alertes
    - Absentéisme en hausse

**Mesures préventives :**

| Mesure | Impact |
|---|---|
| **SOAR** pour réduire les tâches répétitives | Libère le temps cognitif |
| **Rotation régulière** des rôles (triage/investigation/hunting) | Évite la monotonie |
| **Debriefs post-incident** constructifs | Apprentissage sans culpabilisation |
| **Formation continue** | Motivation et montée en compétences |
| **Limite d'alertes par analyste** | < 50 alertes actionables/jour |

<br>

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    L'astreinte est un **service aux analystes autant qu'à l'organisation**. Bien organisée, elle est supportable et maintient la motivation. Mal gérée (surcharge, compensations insuffisantes, outils défaillants), elle détruit les équipes en quelques mois. Investir dans les outils d'alerting et dans la réduction des faux positifs (SOAR) est directement lié à la **santé de l'équipe SOC**.

> Terminez avec **[Communication de Crise →](./crisis-comm.md)** pour apprendre à gérer la communication lors d'un incident majeur.

<br>