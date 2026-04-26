---
description: "Exemples cybersécurité appliqués aux formats JSON, YAML, XML et CSV"
icon: lucide/flask-conical
tags: ["LAB", "FORMATS", "JSON", "YAML", "XML", "CSV", "CYBERSÉCURITÉ"]
---

# Lab — Formats de données appliqués à la cybersécurité

<div
  class="omny-meta"
  data-level="🟡 Intermédiaire"
  data-version="1.0"
  data-time="30-40 minutes">
</div>

!!! quote "Analogie"
    _Comprendre un format de données en lisant sa spécification, c'est apprendre à conduire en lisant le code de la route. Ces exemples sont le volant : des structures réelles, des données fictives, des cas concrets issus d'environnements de sécurité professionnels._

Ce lab complète les fiches théoriques sur les formats de données. Chaque section présente des exemples fictifs mais réalistes, directement applicables en contexte cybersécurité. L'objectif n'est pas d'expliquer les formats — c'est de les voir en action dans des situations concrètes.

!!! warning "Toutes les données présentées sont fictives et à usage pédagogique exclusivement."

!!! note "Prérequis — lire les fiches théoriques avant ce lab : [JSON](../json.md) · [YAML](../yaml.md) · [XML](../xml.md) · [CSV](../csv.md)"

<br />

---

## JSON — Exemples cybersécurité

### Rapport de scan de vulnérabilités

Format de sortie typique des scanners Nessus, OpenVAS ou Nuclei. La structure hiérarchique de JSON permet d'imbriquer les détails de chaque vulnérabilité dans son hôte cible.

```json title="JSON — rapport de scan Nessus/OpenVAS"
{
  "scan_id": "scan_20251115_103045",
  "timestamp": "2025-11-15T10:30:45Z",
  "target": "192.168.1.0/24",
  "vulnerabilities": [
    {
      "host": "192.168.1.10",
      "port": 22,
      "service": "SSH",
      "vulnerability": {
        "name": "Weak SSH Encryption Algorithms",
        "severity": "MEDIUM",
        "cvss_score": 5.3,
        "cve": ["CVE-2016-6210"],
        "description": "Server supports weak encryption algorithms",
        "recommendation": "Disable weak ciphers in sshd_config"
      }
    },
    {
      "host": "192.168.1.15",
      "port": 3306,
      "service": "MySQL",
      "vulnerability": {
        "name": "SQL Injection",
        "severity": "HIGH",
        "cvss_score": 8.1,
        "cve": ["CVE-2019-2614"],
        "description": "MySQL version vulnerable to SQL injection",
        "recommendation": "Upgrade to MySQL 5.7.26 or later"
      }
    },
    {
      "host": "192.168.1.20",
      "port": 445,
      "service": "SMB",
      "vulnerability": {
        "name": "EternalBlue",
        "severity": "CRITICAL",
        "cvss_score": 9.8,
        "cve": ["CVE-2017-0144"],
        "description": "SMBv1 vulnerable to remote code execution",
        "recommendation": "Disable SMBv1 immediately and patch system"
      }
    }
  ],
  "statistics": {
    "total_hosts": 256,
    "hosts_scanned": 45,
    "vulnerabilities_found": 3,
    "severity_breakdown": {
      "critical": 1,
      "high": 1,
      "medium": 1,
      "low": 0
    }
  }
}
```

### Logs de firewall structurés

Les firewalls modernes (pfSense, Fortinet, Palo Alto) peuvent exporter leurs événements en JSON pour ingestion dans un SIEM ou une stack ELK.

```json title="JSON — événements firewall"
{
  "events": [
    {
      "timestamp": "2025-11-15T10:23:45.123Z",
      "event_id": "fw_001",
      "action": "BLOCK",
      "source": {
        "ip": "203.0.113.50",
        "port": 54321,
        "country": "CN",
        "asn": "AS4134"
      },
      "destination": {
        "ip": "192.168.1.100",
        "port": 22,
        "service": "SSH"
      },
      "protocol": "TCP",
      "reason": "Blacklisted IP",
      "rule_id": "blacklist_001"
    },
    {
      "timestamp": "2025-11-15T10:24:12.456Z",
      "event_id": "fw_002",
      "action": "ALLOW",
      "source": {
        "ip": "192.168.1.50",
        "port": 45678,
        "country": "FR",
        "asn": "AS3215"
      },
      "destination": {
        "ip": "8.8.8.8",
        "port": 53,
        "service": "DNS"
      },
      "protocol": "UDP",
      "reason": "Legitimate DNS query",
      "rule_id": "allow_dns"
    }
  ]
}
```

### Règles de détection SIEM

Les SIEM comme Splunk, Elastic SIEM ou Wazuh utilisent des règles de détection structurées. JSON permet de définir des conditions complexes avec seuils, délais et actions chaînées.

```json title="JSON — règles de détection SIEM"
{
  "rules": [
    {
      "id": "rule_001",
      "name": "Brute Force SSH Detection",
      "enabled": true,
      "severity": "HIGH",
      "conditions": {
        "event_type": "authentication",
        "service": "ssh",
        "result": "failed",
        "threshold": {
          "count": 5,
          "timeframe": "5m",
          "group_by": "source_ip"
        }
      },
      "actions": [
        {
          "type": "alert",
          "channels": ["email", "slack"]
        },
        {
          "type": "block",
          "duration": "1h",
          "target": "source_ip"
        }
      ]
    },
    {
      "id": "rule_002",
      "name": "Privilege Escalation Attempt",
      "enabled": true,
      "severity": "CRITICAL",
      "conditions": {
        "event_type": "command_execution",
        "command_contains": ["sudo", "su", "chmod 777"],
        "user_not_in_group": "admins"
      },
      "actions": [
        {
          "type": "alert",
          "priority": "P1",
          "channels": ["pagerduty", "email"]
        },
        {
          "type": "log",
          "retention": "90d"
        }
      ]
    }
  ]
}
```

### Réponse API threat intelligence

Les APIs de threat intelligence (AbuseIPDB, VirusTotal, Shodan) retournent systématiquement du JSON. Savoir naviguer dans ces structures est indispensable pour l'enrichissement automatisé d'alertes.

```json title="JSON — enrichissement IP via API threat intelligence"
{
  "query": {
    "ip": "203.0.113.50",
    "timestamp": "2025-11-15T10:30:00Z"
  },
  "result": {
    "threat_score": 85,
    "classification": "malicious",
    "categories": ["botnet", "brute_force", "port_scanner"],
    "geolocation": {
      "country": "CN",
      "city": "Beijing",
      "latitude": 39.9042,
      "longitude": 116.4074,
      "timezone": "Asia/Shanghai"
    },
    "network": {
      "asn": 4134,
      "organization": "Chinanet",
      "isp": "China Telecom"
    },
    "reputation": {
      "blacklists": [
        {
          "name": "Spamhaus",
          "listed": true,
          "listing_date": "2025-11-10"
        },
        {
          "name": "AbuseIPDB",
          "listed": true,
          "abuse_confidence": 92
        }
      ]
    },
    "recent_activity": [
      {
        "date": "2025-11-14",
        "type": "port_scan",
        "targets": 1247
      },
      {
        "date": "2025-11-13",
        "type": "ssh_bruteforce",
        "attempts": 5632
      }
    ]
  }
}
```

<br />

---

## YAML — Exemples cybersécurité

### Configuration de pipeline CI/CD sécurisé

Les pipelines CI/CD (GitHub Actions, GitLab CI) sont définis en YAML. Ce pipeline intègre des étapes de sécurité : analyse de dépendances, scan SAST, scan de conteneur.

```yaml title="YAML — pipeline CI/CD avec étapes de sécurité"
name: Pipeline CI/CD Sécurisé

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  analyse-dependances:
    name: Analyse des dépendances
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Audit npm
        run: npm audit --audit-level=high

      - name: OWASP Dependency-Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: "mon-application"
          path: "."
          format: "HTML"
          failBuildOnCVSS: 7

  sast:
    name: Analyse statique (SAST)
    runs-on: ubuntu-latest
    needs: analyse-dependances
    steps:
      - uses: actions/checkout@v4

      - name: Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
          auditOn: push

  scan-conteneur:
    name: Scan image Docker
    runs-on: ubuntu-latest
    needs: sast
    steps:
      - name: Build image
        run: docker build -t $IMAGE_NAME:${{ github.sha }} .

      - name: Trivy — scan vulnérabilités
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: sarif
          severity: CRITICAL,HIGH
          exit-code: 1
```

### Configuration Ansible — durcissement serveur

Ansible utilise YAML pour ses playbooks. Ce playbook applique des mesures de durcissement CIS sur un serveur Ubuntu.

```yaml title="YAML — playbook Ansible durcissement CIS"
---
- name: Durcissement CIS Ubuntu 22.04
  hosts: serveurs_production
  become: true
  vars:
    ssh_port: 2222
    max_auth_tries: 3
    password_auth: "no"
    permit_root_login: "no"

  tasks:
    - name: Désactiver les protocoles réseau non utilisés
      modprobe:
        name: "{{ item }}"
        state: absent
      loop:
        - dccp
        - sctp
        - rds
        - tipc

    - name: Configurer SSH — désactiver root et auth par mot de passe
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: "{{ item.regexp }}"
        line: "{{ item.line }}"
        state: present
      loop:
        - { regexp: '^PermitRootLogin', line: 'PermitRootLogin {{ permit_root_login }}' }
        - { regexp: '^PasswordAuthentication', line: 'PasswordAuthentication {{ password_auth }}' }
        - { regexp: '^Port', line: 'Port {{ ssh_port }}' }
        - { regexp: '^MaxAuthTries', line: 'MaxAuthTries {{ max_auth_tries }}' }
      notify: Redémarrer SSH

    - name: Activer et configurer le pare-feu UFW
      ufw:
        rule: allow
        port: "{{ ssh_port }}"
        proto: tcp

    - name: Activer UFW
      ufw:
        state: enabled
        policy: deny

    - name: Configurer auditd — surveillance des accès sensibles
      copy:
        dest: /etc/audit/rules.d/security.rules
        content: |
          -w /etc/passwd -p wa -k identity
          -w /etc/shadow -p wa -k identity
          -w /etc/sudoers -p wa -k sudoers
          -a always,exit -F arch=b64 -S execve -k exec

  handlers:
    - name: Redémarrer SSH
      service:
        name: sshd
        state: restarted
```

### Règles de détection Sigma

Sigma est un format standard de règles de détection SIEM, écrit en YAML. Ces règles peuvent être converties automatiquement pour Splunk, Elastic, QRadar ou Wazuh.

```yaml title="YAML — règles de détection Sigma"
title: Détection brute force SSH
id: a7c3e8f2-1b4d-4e9a-8c6f-2d5b3a7e9f1c
status: stable
description: Détecte des tentatives répétées d'authentification SSH échouées depuis une même IP
references:
  - https://attack.mitre.org/techniques/T1110/
author: OmnyDocs
date: 2025-11-15
tags:
  - attack.credential_access
  - attack.t1110.001
logsource:
  product: linux
  service: auth
detection:
  selection:
    type: sshd
    message|contains: "Failed password"
  timeframe: 5m
  condition: selection | count() by src_ip > 5
falsepositives:
  - Utilisateurs légitimes ayant oublié leur mot de passe
  - Scripts d'automatisation mal configurés
level: high
---
title: Escalade de privilèges via sudo
id: b9d2f4a1-3c7e-4f8b-9d2a-5e8c1b4f7d3a
status: experimental
description: Détecte une utilisation suspecte de sudo par un compte non administrateur
tags:
  - attack.privilege_escalation
  - attack.t1548.003
logsource:
  product: linux
  service: auth
detection:
  selection:
    type: sudo
    message|contains: "COMMAND"
  filter:
    user|in:
      - root
      - admin
      - ansible
  condition: selection and not filter
level: critical
```

<br />

---

## XML — Exemples cybersécurité

### Rapport XCCDF — résultat d'audit de conformité

XCCDF (eXtensible Configuration Checklist Description Format) est le standard NIST pour les audits de conformité. OpenSCAP produit ce type de rapport.

```xml title="XML — rapport XCCDF OpenSCAP"
<?xml version="1.0" encoding="UTF-8"?>
<TestResult
  xmlns="http://checklists.nist.gov/xccdf/1.2"
  id="xccdf_org.open-scap_testresult_xccdf_org.ssg.content_profile_cis"
  start-time="2025-11-15T10:00:00"
  end-time="2025-11-15T10:15:32">

  <benchmark href="/usr/share/xml/scap/ssg/content/ssg-ubuntu2204-xccdf.xml"
             id="xccdf_org.ssgproject.content_benchmark_UBUNTU-22-04"/>

  <title>Résultat audit CIS Ubuntu 22.04</title>

  <identity authenticated="true" privileged="true">root</identity>

  <target>serveur-web-01.example.com</target>
  <target-address>192.168.1.10</target-address>

  <rule-result idref="xccdf_org.ssgproject.content_rule_sshd_disable_root_login"
               time="2025-11-15T10:02:15" severity="high">
    <result>pass</result>
    <message>PermitRootLogin est défini à no dans /etc/ssh/sshd_config</message>
  </rule-result>

  <rule-result idref="xccdf_org.ssgproject.content_rule_sshd_disable_password_auth"
               time="2025-11-15T10:02:18" severity="high">
    <result>fail</result>
    <message>PasswordAuthentication n'est pas désactivé — valeur actuelle : yes</message>
    <fix system="urn:xccdf:fix:script:sh">
      sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
      systemctl restart sshd
    </fix>
  </rule-result>

  <rule-result idref="xccdf_org.ssgproject.content_rule_ufw_enabled"
               time="2025-11-15T10:03:45" severity="medium">
    <result>pass</result>
    <message>UFW est actif et configuré</message>
  </rule-result>

  <score system="urn:xccdf:scoring:default" maximum="100">73.5</score>

</TestResult>
```

### Format STIX — indicateurs de compromission

STIX (Structured Threat Information eXpression) est le standard international pour le partage de renseignements sur les menaces. Utilisé par les CERT, SOC et plateformes MISP.

```xml title="XML — indicateurs STIX"
<?xml version="1.0" encoding="UTF-8"?>
<STIX_Package
  xmlns="http://stix.mitre.org/stix"
  xmlns:indicator="http://stix.mitre.org/Indicator"
  xmlns:ttp="http://stix.mitre.org/TTP"
  id="example:Package-8fab937e-b694-11e3-b71c-0800271e87d2"
  timestamp="2025-11-15T10:30:00Z"
  version="1.2">

  <STIX_Header>
    <Title>Campagne de brute force SSH — Botnet Mirai</Title>
    <Description>IOCs liés à une campagne active de brute force SSH</Description>
    <Package_Intent>Indicators</Package_Intent>
  </STIX_Header>

  <Indicators>
    <Indicator id="example:Indicator-IP-001" timestamp="2025-11-15T10:00:00Z">
      <Title>IP malveillante — brute force SSH confirmé</Title>
      <Type>IP Watchlist</Type>
      <Valid_Time_Position>
        <Start_Time>2025-11-14T00:00:00Z</Start_Time>
        <End_Time>2025-12-14T00:00:00Z</End_Time>
      </Valid_Time_Position>
      <Observable>
        <Object>
          <Properties xsi:type="AddressObjectType"
                      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                      category="ipv4-addr">
            <Address_Value condition="Equals">203.0.113.50</Address_Value>
          </Properties>
        </Object>
      </Observable>
      <Confidence value="High"/>
      <Sightings sightings_count="847">
        <Sighting timestamp="2025-11-14T22:15:00Z">
          <Source>Honeypot-FR-01</Source>
        </Sighting>
      </Sightings>
    </Indicator>
  </Indicators>

</STIX_Package>
```

### Configuration WAF ModSecurity

Les règles WAF (Web Application Firewall) ModSecurity utilisent une syntaxe XML pour la configuration des politiques de sécurité applicative.

```xml title="XML — règles ModSecurity WAF"
<?xml version="1.0" encoding="UTF-8"?>
<modsecurity-config version="2.9">

  <policy name="OWASP-CRS-Base">
    <description>Politique de base OWASP Core Rule Set</description>

    <settings>
      <SecRuleEngine>On</SecRuleEngine>
      <SecRequestBodyAccess>On</SecRequestBodyAccess>
      <SecResponseBodyAccess>On</SecResponseBodyAccess>
      <SecRequestBodyLimit>13107200</SecRequestBodyLimit>
      <SecAuditLog>/var/log/modsec_audit.log</SecAuditLog>
    </settings>

    <rules>
      <rule id="942100" phase="2" severity="CRITICAL">
        <description>Détection injection SQL — libinjection</description>
        <condition>
          <target>ARGS</target>
          <operator>detectSQLi</operator>
        </condition>
        <action type="block">
          <message>SQL Injection Attack Detected</message>
          <tag>OWASP_CRS/WEB_ATTACK/SQL_INJECTION</tag>
          <logdata>%{MATCHED_VAR}</logdata>
        </action>
      </rule>

      <rule id="941100" phase="2" severity="CRITICAL">
        <description>Détection XSS — libinjection</description>
        <condition>
          <target>ARGS</target>
          <operator>detectXSS</operator>
        </condition>
        <action type="block">
          <message>XSS Attack Detected</message>
          <tag>OWASP_CRS/WEB_ATTACK/XSS</tag>
          <logdata>%{MATCHED_VAR}</logdata>
        </action>
      </rule>

      <rule id="920350" phase="1" severity="WARNING">
        <description>IP dans la liste noire</description>
        <condition>
          <target>REMOTE_ADDR</target>
          <operator>@ipMatchFromFile</operator>
          <value>blacklist_ips.txt</value>
        </condition>
        <action type="block">
          <message>Accès refusé — IP blacklistée</message>
        </action>
      </rule>
    </rules>

  </policy>

</modsecurity-config>
```

<br />

---

## CSV — Exemples cybersécurité

### Export de logs d'authentification

Format typique d'export de logs Active Directory ou d'un LDAP. Utilisé pour l'analyse forensique, la détection d'anomalies ou l'alimentation d'un SIEM.

```csv title="CSV — logs d'authentification Active Directory"
timestamp,event_id,user,domain,source_ip,workstation,result,failure_reason,logon_type
2025-11-15T08:12:34Z,4624,alice.dupont,CORP,192.168.1.45,WS-ALICE,SUCCESS,,Interactive
2025-11-15T08:15:02Z,4625,bob.martin,CORP,192.168.1.50,WS-BOB,FAILURE,Wrong password,Network
2025-11-15T08:15:04Z,4625,bob.martin,CORP,192.168.1.50,WS-BOB,FAILURE,Wrong password,Network
2025-11-15T08:15:07Z,4625,bob.martin,CORP,192.168.1.50,WS-BOB,FAILURE,Wrong password,Network
2025-11-15T08:15:09Z,4740,bob.martin,CORP,192.168.1.50,WS-BOB,LOCKED,,Network
2025-11-15T09:00:00Z,4624,svc-backup,CORP,192.168.1.200,SRV-BACKUP,SUCCESS,,Service
2025-11-15T09:45:12Z,4624,admin,CORP,203.0.113.50,,SUCCESS,,Network
2025-11-15T10:23:45Z,4625,administrator,CORP,203.0.113.50,,FAILURE,Bad password,Network
2025-11-15T10:23:47Z,4625,administrator,CORP,203.0.113.50,,FAILURE,Bad password,Network
2025-11-15T10:23:49Z,4625,administrator,CORP,203.0.113.50,,FAILURE,Bad password,Network
```

!!! tip "Lecture du CSV"
    La ligne 7 est suspecte : connexion réussie de `admin` depuis une IP externe (`203.0.113.50`) sans workstation renseignée. Les lignes 8-10 montrent des tentatives de brute force sur `administrator` depuis la même IP externe.

### Inventaire des actifs et vulnérabilités

Format d'export CMDB (Configuration Management Database) enrichi des résultats de scan. Sert de base pour la priorisation des correctifs.

```csv title="CSV — inventaire actifs et CVE"
hostname,ip,os,os_version,criticite,cve_id,cvss_score,severity,patch_disponible,date_detection,sla_remediation
srv-web-01,192.168.1.10,Ubuntu,22.04 LTS,HIGH,CVE-2024-1234,9.8,CRITICAL,Oui,2025-11-01,2025-11-08
srv-web-01,192.168.1.10,Ubuntu,22.04 LTS,HIGH,CVE-2024-5678,7.5,HIGH,Oui,2025-11-01,2025-11-15
srv-db-01,192.168.1.20,CentOS,7.9,CRITICAL,CVE-2023-9999,9.8,CRITICAL,Non,2025-10-15,2025-10-22
srv-db-01,192.168.1.20,CentOS,7.9,CRITICAL,CVE-2024-1111,8.1,HIGH,Oui,2025-11-05,2025-11-12
ws-rh-05,192.168.2.45,Windows,10 22H2,MEDIUM,CVE-2024-3333,6.5,MEDIUM,Oui,2025-11-10,2025-11-24
srv-backup,192.168.1.200,Windows Server,2019,HIGH,CVE-2024-4444,7.8,HIGH,Oui,2025-11-08,2025-11-15
```

### Résultats de scan réseau

Export Nmap au format CSV pour traitement automatisé. Utilisé pour cartographier les surfaces d'attaque et détecter les services exposés non autorisés.

```csv title="CSV — résultats scan Nmap"
ip,hostname,port,protocol,state,service,version,banner,first_seen,last_seen
192.168.1.1,router.local,22,tcp,open,ssh,OpenSSH 8.9,SSH-2.0-OpenSSH_8.9,2025-01-01,2025-11-15
192.168.1.1,router.local,80,tcp,open,http,nginx 1.24.0,,2025-01-01,2025-11-15
192.168.1.1,router.local,443,tcp,open,https,nginx 1.24.0,,2025-01-01,2025-11-15
192.168.1.10,srv-web-01,22,tcp,open,ssh,OpenSSH 9.0,,2025-01-15,2025-11-15
192.168.1.10,srv-web-01,80,tcp,open,http,Apache 2.4.54,,2025-01-15,2025-11-15
192.168.1.10,srv-web-01,8080,tcp,open,http-proxy,Squid 5.7,,2025-09-01,2025-11-15
192.168.1.20,srv-db-01,3306,tcp,open,mysql,MySQL 5.7.38,,2025-01-15,2025-11-15
192.168.1.20,srv-db-01,6379,tcp,open,redis,Redis 6.2.7,,2025-08-01,2025-11-15
192.168.1.50,ws-dev-01,22,tcp,open,ssh,OpenSSH 9.0,,2025-03-01,2025-11-15
192.168.1.50,ws-dev-01,3000,tcp,open,http,Node.js,Express,2025-10-01,2025-11-15
```

!!! tip "Points d'attention"
    Port 6379 (Redis) ouvert sur `srv-db-01` sans authentification mentionnée — vecteur d'attaque classique. Port 3000 (Node.js/Express) sur un poste de développement accessible depuis le réseau — service de développement exposé en production.

<br />

---

## Conclusion

!!! quote "Ce qu'il faut retenir"
    La manipulation de formats comme JSON, YAML et CSV est omniprésente en développement et automatisation. Savoir les lire, les structurer et les convertir est une compétence transversale qui vous servira au quotidien.

!!! quote "Conclusion"
    _Ces exemples ne sont pas des exercices académiques — ce sont des structures rencontrées quotidiennement dans les environnements de sécurité. Un analyste SOC lit des JSON de threat intelligence, un ingénieur DevSecOps écrit des pipelines YAML, un auditeur produit des rapports XCCDF, un pentester exporte des résultats Nmap en CSV. Savoir lire ces formats à vue, identifier ce qui est suspect et les manipuler programmatiquement est une compétence fondamentale._

<br />