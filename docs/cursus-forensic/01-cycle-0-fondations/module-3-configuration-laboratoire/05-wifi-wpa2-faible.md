---
description: "Configuration du Wi-Fi WPA2 avec passphrase volontairement faible pour exercices de capture de handshake et cassage offline avec hashcat. Réalisme pédagogique."
icon: lucide/wifi
tags: ["WI-FI", "WPA2", "PENTEST", "HASHCAT"]
---

# Wi-Fi WPA2-PSK volontairement faible

<div
  class="omny-meta"
  data-level="🔴 Avancé"
  data-version="Modèle 2026"
  data-time="1 heure">
</div>

!!! note "**Livrables :** _Réseau Wi-Fi vulnérable diffusé par le routeur_"
!!! note "**Auto-explication :** _5 minutes_"

<br>

---

<br>

!!! quote "L'analogie du coffre-fort avec le code sous le clavier"

    Imaginez installer le coffre-fort le plus blindé du monde, mais laisser le code inscrit sur un post-it juste en dessous. La sécurité de la technologie WPA2 repose sur la complexité de son mot de passe (Passphrase). Si ce mot de passe est prévisible ou lié au contexte de l'entreprise, le WPA2 tombe en quelques secondes face à une attaque par dictionnaire moderne. Dans ce chapitre, nous allons intentionnellement créer ce scénario "post-it" pour préparer le module d'attaque Wi-Fi.

## Objectifs pédagogiques

!!! tip "À la fin de ce chapitre, vous serez capable de :"

    - Configurer un réseau Wi-Fi d'entreprise réaliste (SSID et mot de passe contextuel).
    - Comprendre l'illusion de sécurité apportée par la longueur du mot de passe si sa structure est prévisible.
    - Activer un réseau 2.4 GHz vulnérable sous OpenWrt pour les futurs TPs de capture de Handshake (WPA).

<br>

---

<br>

## Pourquoi un Wi-Fi délibérément faible ?

L'apprentissage par l'attaque exige des cibles **réalistes**. Bien que nous soyons en 2026, de nombreuses PME utilisent encore des configurations Wi-Fi dépassées ou mal pensées :

- Utilisation de **WPA2-PSK** au lieu du standard WPA3 (qui résiste mieux aux attaques par dictionnaire).
- Des passphrases de longueur modeste (8 à 16 caractères).
- **Pire encore :** Des mots de passe basés sur la raison sociale de l'entreprise suivie de l'année en cours (Ex: `NomEntreprise2026!`).

!!! warning "C'est exactement ce modèle de "**négligence**" que nous allons reproduire dans notre PME fictive ARTECH, pour ensuite vous entraîner à le craquer."

<br>

---

<br>

## Configuration sous OpenWrt

!!! quote "Nous allons créer notre réseau Wi-Fi cible (`ARTECH-WIFI`) directement en éditant les fichiers de configuration de notre routeur."

### Déploiement du réseau Wi-Fi cible

!!! abstract "On crée le réseau Wi-Fi de manière native sous OpenWrt en modifiant le fichier de configuration `/etc/config/wireless`. L'objectif est de créer un réseau visible par tous les appareils environnants (portables, smartphones) avec un nom (SSID) facilement identifiable et un mot de passe faible que nous allons volontairement créer de manière contextuelle (lié à l'entreprise). Cette méthode est préférée à l'utilisation de l'interface graphique LuCI pour garantir la reproductibilité et la précision des configurations nécessaires à nos exercices ultérieurs."

```bash title="Commandes Linux - Configuration Wireless OpenWrt"
# Édition du fichier de configuration Wi-Fi
vi /etc/config/wireless
```

!!! note "**Note:** Dans l'éditeur Vi, utilisez les touches suivantes :"

    - `i` pour insérer du texte (Passer en mode INSERT).
    - `Échap` pour quitter le mode INSERT.
    - `:wq` pour sauvegarder et quitter (Write & Quit).
    - `:q!` pour quitter sans sauvegarder (Forcer la sortie).

```text title="Fichier /etc/config/wireless - Activation du 2.4 GHz"
# Définition de l'interface radio (Matérielle)
config wifi-device 'radio0'
    option type 'mac80211'
    option path 'pci0000:00/0000:00:00.0'
    option channel '6'                 # Canal fixe recommandé pour les tests
    option band '2g'                   # Bande 2.4 GHz uniquement
    option htmode 'HT20'
    option country 'FR'                # Conformité fréquences
    option txpower '20'
    option disabled '0'                # Active l'interface radio

# Définition du réseau logique (SSID)
config wifi-iface 'default_radio0'
    option device 'radio0'
    option network 'lan'
    option mode 'ap'                   # Mode Access Point (Point d'accès)
    option ssid 'ARTECH-WIFI'
    option encryption 'psk2'           # Mode de chiffrement WPA2-PSK
    option key 'ArtechMedical2020!'    # Le mot de passe (vulnérable)
    option ieee80211w '0'              # Désactive la protection des trames de gestion
```

!!! warning "Désactivation des protections"
    L'option `option ieee80211w '0'` est cruciale. Elle désactive le "Management Frame Protection" (MFP). Sans cette désactivation, il serait impossible d'envoyer les trames de désauthentification nécessaires pour capturer le WPA Handshake dans nos futurs exercices.

<br>

### Application et Vérification


#### Redémarrage des services radio"

```bash title="Commandes Linux - Application de la configuration Wi-Fi"
# Appliquer les modifications au système Wi-Fi
wifi reload

# Vérifier l'état de la carte Wi-Fi (Doit afficher le SSID)
iw dev wlan0 info
```

<br>

---

<br>

## Autopsie d'un mauvais mot de passe

Analysons la clé que nous venons de configurer : `ArtechMedical2020!`

En apparence, elle semble forte :

- Elle compte **18 caractères**.
- Elle mélange des **majuscules** et des **minuscules**.
- Elle inclut des **chiffres** (`2020`).
- Elle se termine par un **caractère spécial** (`!`).

!!! danger "L'illusion de la complexité"
    Malgré ses 18 caractères, cette clé est **extrêmement faible**. Sa structure est totalement **prévisible** : `NomDeLentreprise` + `SecteurDactivite` + `Annee` + `Ponctuation`.
    Les générateurs de dictionnaires modernes (associés à des listes comme `rockyou.txt` et des générateurs de règles via *Hashcat*) sont spécifiquement conçus pour détecter ces schémas cognitifs humains. Ils la casseront en quelques minutes.

<br>

---

<br>

## Test de validation depuis votre poste

Avant de clore ce chapitre, assurez-vous que le réseau est bien diffusé et fonctionnel.

### Commandes de détection Wi-Fi

```bash title="Commandes Linux - Scan et connexion depuis le poste d'attaque"
# Vérifier que le SSID 'ARTECH-WIFI' est détecté par votre carte Wi-Fi
iwlist wlan0 scan | grep -A 3 ARTECH
    
# Ou via NetworkManager (Plus lisible)
nmcli dev wifi list | grep ARTECH
    
# Tenter la connexion avec le mot de passe (Facultatif)
nmcli dev wifi connect ARTECH-WIFI password 'ArtechMedical2020!'
```

### Description des commandes saisies

```bash title="Commande : iwlist wlan0 scan | grep -A 3 ARTECH"

# `iwlist wlan0 scan` : Liste les réseaux Wi-Fi détectés par l'interface `wlan0`.

# `grep -A 3 ARTECH` : Filtre les résultats pour afficher uniquement les lignes contenant `ARTECH` ainsi que les 3 lignes suivantes (détails du réseau).
```

```bash title="Commande : nmcli dev wifi list | grep ARTECH"

# `nmcli dev wifi list` : Liste les réseaux Wi-Fi détectés via NetworkManager de manière lisible.

# `grep -A 3 ARTECH` : Filtre les résultats pour afficher uniquement les lignes contenant `ARTECH` ainsi que les 3 lignes suivantes (détails du réseau).
```

```bash title="Commande : nmcli dev wifi connect ARTECH-WIFI password 'ArtechMedical2020!'"

# `nmcli dev wifi connect` : Connecte l'appareil au réseau Wi-Fi spécifié.
# `ARTECH-WIFI` : Nom du réseau (SSID).
# `password 'ArtechMedical2020!'` : Mot de passe du réseau.
```

<br>

---

<br>

## Conclusion

!!! quote "Ce qu'il faut retenir"
    Vous avez maintenant une cible réseau Wi-Fi active et vulnérable au sein de votre laboratoire. Ce réseau, représentatif des mauvaises pratiques corporatives (Mot de passe contextuel et WPA2 vieillissant), servira de terrain de jeu principal pour les attaques de capture de "Handshake" et de cassage hors-ligne.

> [Chapitre suivant : 3.6 Installation Debian 12 serveur →](06-debian-serveur.md)
>
> [Retour à l'index →](./index.md)

<br>
