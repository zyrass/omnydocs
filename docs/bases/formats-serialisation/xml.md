---
description: "Maîtriser le format XML pour l'échange de données structurées et hiérarchiques"
icon: lucide/book-open-check
tags: ["XML", "DONNÉES", "FORMATS", "SOAP", "CONFIGURATION"]
---

# XML - eXtensible Markup Language

## Introduction

<div
  class="omny-meta"
  data-level="🟢 Débutant & 🟡 Intermédiaire"
  data-version="1.1"
  data-time="50-55 minutes">
</div>

!!! quote "Analogie pédagogique"
    _Imaginez un **système de classement de bibliothèque** où chaque livre est dans une catégorie, chaque catégorie dans une section, chaque section dans un étage, avec des **étiquettes explicites** à chaque niveau indiquant exactement où vous êtes. **XML fonctionne exactement ainsi** : chaque élément a une **balise d'ouverture** (`<livre>`) et une **balise de fermeture** (`</livre>`), créant une structure hiérarchique claire et auto-descriptive où chaque donnée porte son propre nom._

> **XML (eXtensible Markup Language)** est un format de **données textuelles** créé pour représenter des **informations structurées** de manière **hiérarchique** et **extensible**. Contrairement à HTML qui est conçu pour afficher du contenu, XML est conçu pour **stocker et transporter des données** avec une structure stricte et validable.

XML a dominé l'échange de données dans les années 2000-2010, notamment avec **SOAP**, **RSS**, **SVG**, et les **fichiers de configuration** (Maven, Spring, Ant). Bien que JSON l'ait supplanté pour les APIs REST, XML reste **essentiel** pour les **systèmes legacy**, les **protocoles bancaires/financiers**, les **standards industriels** (HL7 médical, XBRL finance), et certains **formats de documents** (Office Open XML, SVG).

!!! info "Pourquoi c'est important ?"
    XML est omniprésent dans les **systèmes legacy**, les **services SOAP**, les **fichiers de configuration Java/Spring**, les **formats Office** (docx, xlsx), les **flux RSS/Atom**, **SVG**, et constitue un standard dans la **finance**, la **santé**, et l'**administration**.

## Structure XML

### Syntaxe de base

**Document XML simple :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<utilisateur>
    <nom>Dupont</nom>
    <prenom>Alice</prenom>
    <age>28</age>
    <actif>true</actif>
</utilisateur>
```

**Règles syntaxiques strictes :**

- ✅ **Une seule racine** : Tout document XML doit avoir un élément racine unique
- ✅ **Balises fermées** : Chaque `<ouverture>` doit avoir son `</fermeture>`
- ✅ **Sensible à la casse** : `<Nom>` ≠ `<nom>`
- ✅ **Imbrication correcte** : 
    - ✅ `<a><b></b></a>` 
    - ❌ `<a><b></a></b>`
- ✅ **Caractères spéciaux échappés** : `<`, `>`, `&`, `"`, `'`

### Déclaration XML

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
```

**Attributs de la déclaration :**

- `version` : Version XML (toujours `1.0` ou `1.1`)
- `encoding` : Encodage des caractères (`UTF-8` recommandé)
- `standalone` : Document autonome (`yes`) ou avec DTD externe (`no`)

### Éléments et attributs

**Éléments (balises) :**
```xml
<!-- Élément avec contenu -->
<nom>Alice</nom>

<!-- Élément vide (auto-fermant) -->
<br/>
<image src="photo.jpg"/>

<!-- Élément avec sous-éléments -->
<adresse>
    <rue>12 rue des Fleurs</rue>
    <ville>Paris</ville>
    <code_postal>75001</code_postal>
</adresse>
```

**Attributs :**
```xml
<utilisateur id="1234" actif="true" role="admin">
    <nom>Alice</nom>
</utilisateur>
```

**Éléments vs Attributs - Quand utiliser quoi ?**

| Critère | Élément | Attribut |
|---------|---------|----------|
| **Données structurées** | ✅ `<adresse><ville>...</ville></adresse>` | ❌ Pas de hiérarchie |
| **Métadonnées** | ⚠️ Possible | ✅ `<user id="123">` |
| **Valeurs multiples** | ✅ Plusieurs `<telephone>` | ❌ Un seul attribut `id` |
| **Lisibilité** | ✅ Plus clair | ⚠️ Compact mais dense |
| **Recommandation** | **Privilégier pour données** | **Pour métadonnées uniquement** |

### Espaces de noms (Namespaces)

Les **namespaces** évitent les conflits de noms d'éléments.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns:sec="http://example.com/security"
      xmlns:usr="http://example.com/user">
    
    <sec:policy id="pol-001">
        <sec:rule>Block SSH from external</sec:rule>
    </sec:policy>
    
    <usr:user id="123">
        <usr:name>Alice</usr:name>
    </usr:user>
</root>
```

**Namespace par défaut :**
```xml
<root xmlns="http://example.com/default">
    <!-- Tous les éléments sans préfixe utilisent ce namespace -->
    <element>Contenu</element>
</root>
```

### Commentaires et CDATA

**Commentaires :**
```xml
<!-- Ceci est un commentaire sur une ligne -->

<!--
    Commentaire multi-lignes
    pour expliquer la structure
-->

<nom>Alice</nom> <!-- Commentaire en fin de ligne -->
```

**CDATA (Character Data) :**

Permet d'inclure du texte contenant des caractères spéciaux sans échappement.

```xml
<script>
    <![CDATA[
        if (x < 10 && y > 5) {
            alert("Condition met!");
        }
    ]]>
</script>

<code>
    <![CDATA[
        SELECT * FROM users WHERE age > 18 AND role = 'admin';
    ]]>
</code>
```

### Caractères spéciaux et entités

**Entités prédéfinies :**

| Caractère | Entité XML | Usage |
|-----------|------------|-------|
| `<` | `&lt;` | Balise ouvrante |
| `>` | `&gt;` | Balise fermante |
| `&` | `&amp;` | Esperluette |
| `"` | `&quot;` | Guillemet double |
| `'` | `&apos;` | Apostrophe |

```xml
<message>
    Condition: x &lt; 10 &amp;&amp; y &gt; 5
</message>

<citation>
    Il a dit &quot;Bonjour&quot; et c&apos;est tout.
</citation>
```

## Cas d'usage en cybersécurité

!!! danger "Attention - prenez ces exemples de contenu avec ce que l'on peut obtenir. Il n'est pas question de l'analyser ici."

### Exemple 1 : Rapport de scan de vulnérabilités (Nessus XML)

!!! example "Exemple n°1 - Export Nessus XML"

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <NessusClientData_v2>
        <Report name="Network Scan 2025-11-15">
            <ReportHost name="192.168.1.10">
                <HostProperties>
                    <tag name="host-ip">192.168.1.10</tag>
                    <tag name="operating-system">Linux Kernel 5.15</tag>
                    <tag name="host-fqdn">server01.example.com</tag>
                </HostProperties>
                
                <ReportItem port="22" svc_name="ssh" protocol="tcp" 
                            severity="2" pluginID="10267" pluginName="SSH Weak Encryption">
                    <description>
                        The remote SSH server supports weak encryption algorithms.
                    </description>
                    <solution>
                        Disable weak ciphers in sshd_config
                    </solution>
                    <risk_factor>Medium</risk_factor>
                    <cvss_base_score>5.3</cvss_base_score>
                    <cve>CVE-2016-6210</cve>
                    <exploit_available>false</exploit_available>
                </ReportItem>
                
                <ReportItem port="445" svc_name="smb" protocol="tcp" 
                            severity="4" pluginID="97833" pluginName="SMB EternalBlue">
                    <description>
                        The remote Windows host is affected by remote code execution vulnerability
                        known as EternalBlue.
                    </description>
                    <solution>
                        Apply MS17-010 security update immediately.
                    </solution>
                    <risk_factor>Critical</risk_factor>
                    <cvss_base_score>9.8</cvss_base_score>
                    <cve>CVE-2017-0144</cve>
                    <exploit_available>true</exploit_available>
                    <exploitability_ease>Exploits are available</exploitability_ease>
                </ReportItem>
            </ReportHost>
            
            <ReportHost name="192.168.1.15">
                <HostProperties>
                    <tag name="host-ip">192.168.1.15</tag>
                    <tag name="operating-system">Ubuntu 20.04</tag>
                </HostProperties>
                
                <ReportItem port="3306" svc_name="mysql" protocol="tcp" 
                            severity="3" pluginID="11111" pluginName="MySQL SQL Injection">
                    <description>
                        MySQL version is vulnerable to SQL injection attacks.
                    </description>
                    <solution>
                        Upgrade to MySQL 5.7.26 or later
                    </solution>
                    <risk_factor>High</risk_factor>
                    <cvss_base_score>8.1</cvss_base_score>
                    <cve>CVE-2019-2614</cve>
                </ReportItem>
            </ReportHost>
        </Report>
    </NessusClientData_v2>
    ```

### Exemple 2 : Configuration de règles de firewall (Cisco XML)

!!! example "Exemple n°2 - Cisco ASA XML Configuration"

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <firewall-config xmlns="http://cisco.com/asa/config">
        <version>9.12</version>
        <hostname>firewall-dmz-01</hostname>
        
        <interfaces>
            <interface name="GigabitEthernet0/0">
                <nameif>outside</nameif>
                <security-level>0</security-level>
                <ip-address>203.0.113.1</ip-address>
                <netmask>255.255.255.0</netmask>
            </interface>
            
            <interface name="GigabitEthernet0/1">
                <nameif>inside</nameif>
                <security-level>100</security-level>
                <ip-address>192.168.1.1</ip-address>
                <netmask>255.255.255.0</netmask>
            </interface>
            
            <interface name="GigabitEthernet0/2">
                <nameif>dmz</nameif>
                <security-level>50</security-level>
                <ip-address>10.0.0.1</ip-address>
                <netmask>255.255.255.0</netmask>
            </interface>
        </interfaces>
        
        <access-lists>
            <access-list name="OUTSIDE_IN">
                <ace id="1" action="deny">
                    <protocol>ip</protocol>
                    <source>any</source>
                    <destination>192.168.1.0/24</destination>
                    <description>Block direct access to internal network</description>
                </ace>
                
                <ace id="2" action="permit">
                    <protocol>tcp</protocol>
                    <source>any</source>
                    <destination>10.0.0.10</destination>
                    <port>443</port>
                    <description>Allow HTTPS to web server in DMZ</description>
                </ace>
                
                <ace id="3" action="deny">
                    <protocol>ip</protocol>
                    <source>any</source>
                    <destination>any</destination>
                    <log>true</log>
                    <description>Deny all other traffic</description>
                </ace>
            </access-list>
            
            <access-list name="DMZ_IN">
                <ace id="1" action="deny">
                    <protocol>ip</protocol>
                    <source>10.0.0.0/24</source>
                    <destination>192.168.1.0/24</destination>
                    <description>Block DMZ to internal</description>
                </ace>
                
                <ace id="2" action="permit">
                    <protocol>tcp</protocol>
                    <source>10.0.0.10</source>
                    <destination>192.168.1.50</destination>
                    <port>3306</port>
                    <description>Allow web server to database</description>
                </ace>
            </access-list>
        </access-lists>
        
        <nat-rules>
            <rule id="1" type="static">
                <inside-interface>dmz</inside-interface>
                <inside-ip>10.0.0.10</inside-ip>
                <outside-interface>outside</outside-interface>
                <outside-ip>203.0.113.10</outside-ip>
                <description>NAT for web server</description>
            </rule>
        </nat-rules>
    </firewall-config>
    ```

### Exemple 3 : SAML (Authentification SSO)

!!! example "Exemple n°3 - SAML Authentication Response"

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <samlp:Response xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
                    xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"
                    ID="_8e8dc5f69a98cc4c1ff3427e5ce34606fd672f91e6"
                    Version="2.0"
                    IssueInstant="2025-11-15T10:30:45Z"
                    Destination="https://app.example.com/saml/acs"
                    InResponseTo="_269bb8e9ff06cb0e1d34a8bb45b3d6b5">
        
        <saml:Issuer>https://idp.example.com/saml/metadata</saml:Issuer>
        
        <samlp:Status>
            <samlp:StatusCode Value="urn:oasis:names:tc:SAML:2.0:status:Success"/>
        </samlp:Status>
        
        <saml:Assertion xmlns:xs="http://www.w3.org/2001/XMLSchema"
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                        ID="_d71a3a8e9fcc45c9e9d248ef7049393fc8f04e5f75"
                        Version="2.0"
                        IssueInstant="2025-11-15T10:30:45Z">
            
            <saml:Issuer>https://idp.example.com/saml/metadata</saml:Issuer>
            
            <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
                <ds:SignedInfo>
                    <ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                    <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
                    <ds:Reference URI="#_d71a3a8e9fcc45c9e9d248ef7049393fc8f04e5f75">
                        <ds:Transforms>
                            <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                            <ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/>
                        </ds:Transforms>
                        <ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
                        <ds:DigestValue>cMTqA1...</ds:DigestValue>
                    </ds:Reference>
                </ds:SignedInfo>
                <ds:SignatureValue>FzLMqA...</ds:SignatureValue>
                <ds:KeyInfo>
                    <ds:X509Data>
                        <ds:X509Certificate>MIID...</ds:X509Certificate>
                    </ds:X509Data>
                </ds:KeyInfo>
            </ds:Signature>
            
            <saml:Subject>
                <saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">
                    alice@example.com
                </saml:NameID>
                <saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">
                    <saml:SubjectConfirmationData NotOnOrAfter="2025-11-15T10:35:45Z"
                                                   Recipient="https://app.example.com/saml/acs"
                                                   InResponseTo="_269bb8e9ff06cb0e1d34a8bb45b3d6b5"/>
                </saml:SubjectConfirmation>
            </saml:Subject>
            
            <saml:Conditions NotBefore="2025-11-15T10:30:45Z"
                             NotOnOrAfter="2025-11-15T10:35:45Z">
                <saml:AudienceRestriction>
                    <saml:Audience>https://app.example.com/saml/metadata</saml:Audience>
                </saml:AudienceRestriction>
            </saml:Conditions>
            
            <saml:AuthnStatement AuthnInstant="2025-11-15T10:30:45Z"
                                 SessionNotOnOrAfter="2025-11-15T18:30:45Z"
                                 SessionIndex="_be9967abd904ddcae3c0eb4189adbe3f71e327cf93">
                <saml:AuthnContext>
                    <saml:AuthnContextClassRef>
                        urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport
                    </saml:AuthnContextClassRef>
                </saml:AuthnContext>
            </saml:AuthnStatement>
            
            <saml:AttributeStatement>
                <saml:Attribute Name="uid" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
                    <saml:AttributeValue xsi:type="xs:string">alice</saml:AttributeValue>
                </saml:Attribute>
                <saml:Attribute Name="email" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
                    <saml:AttributeValue xsi:type="xs:string">alice@example.com</saml:AttributeValue>
                </saml:Attribute>
                <saml:Attribute Name="role" NameFormat="urn:oasis:names:tc:SAML:2.0:attrname-format:basic">
                    <saml:AttributeValue xsi:type="xs:string">admin</saml:AttributeValue>
                    <saml:AttributeValue xsi:type="xs:string">user</saml:AttributeValue>
                </saml:Attribute>
            </saml:AttributeStatement>
        </saml:Assertion>
    </samlp:Response>
    ```

### Exemple 4 : Configuration Spring Security

!!! example "Exemple n°4 - Spring Security XML Configuration"

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans:beans xmlns="http://www.springframework.org/schema/security"
                 xmlns:beans="http://www.springframework.org/schema/beans"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 xsi:schemaLocation="
                     http://www.springframework.org/schema/beans
                     http://www.springframework.org/schema/beans/spring-beans.xsd
                     http://www.springframework.org/schema/security
                     http://www.springframework.org/schema/security/spring-security.xsd">
        
        <!-- Configuration HTTP Security -->
        <http auto-config="false" use-expressions="true">
            <!-- CSRF Protection -->
            <csrf/>
            
            <!-- Security Headers -->
            <headers>
                <frame-options policy="DENY"/>
                <content-type-options/>
                <xss-protection/>
                <hsts include-subdomains="true" max-age-seconds="31536000"/>
            </headers>
            
            <!-- URL Access Rules -->
            <intercept-url pattern="/public/**" access="permitAll"/>
            <intercept-url pattern="/login" access="permitAll"/>
            <intercept-url pattern="/api/**" access="hasRole('API_USER')"/>
            <intercept-url pattern="/admin/**" access="hasRole('ADMIN')"/>
            <intercept-url pattern="/**" access="isAuthenticated()"/>
            
            <!-- Form Login -->
            <form-login login-page="/login"
                        login-processing-url="/perform_login"
                        default-target-url="/dashboard"
                        authentication-failure-url="/login?error=true"
                        username-parameter="username"
                        password-parameter="password"/>
            
            <!-- Logout -->
            <logout logout-url="/logout"
                    logout-success-url="/login?logout=true"
                    delete-cookies="JSESSIONID"
                    invalidate-session="true"/>
            
            <!-- Session Management -->
            <session-management session-fixation-protection="migrateSession">
                <concurrency-control max-sessions="1"
                                     expired-url="/login?expired=true"
                                     error-if-maximum-exceeded="false"/>
            </session-management>
            
            <!-- Remember Me -->
            <remember-me key="uniqueAndSecret"
                         token-validity-seconds="86400"
                         remember-me-parameter="remember-me"/>
        </http>
        
        <!-- Authentication Manager -->
        <authentication-manager>
            <authentication-provider>
                <password-encoder ref="bcryptEncoder"/>
                <user-service>
                    <user name="admin"
                          password="$2a$10$slYQmyNdGzTn7ZLBXBChFOC9f6kFjAqPhccnP6DxlWXx2lPk1C3G6"
                          authorities="ROLE_ADMIN,ROLE_USER"/>
                    <user name="user"
                          password="$2a$10$EblZqNptyYvcLm/VwDCVAuBjzZOI7khzdyGPBr08PpIi0na624b8."
                          authorities="ROLE_USER"/>
                </user-service>
            </authentication-provider>
        </authentication-manager>
        
        <!-- BCrypt Password Encoder -->
        <beans:bean id="bcryptEncoder" 
                    class="org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder">
            <beans:constructor-arg value="10"/>
        </beans:bean>
        
        <!-- Method Security -->
        <global-method-security pre-post-annotations="enabled"
                                secured-annotations="enabled"
                                jsr250-annotations="enabled"/>
    </beans:beans>
    ```

## Manipulation XML par langage

### :fontawesome-brands-python: Python

**Lecture XML avec ElementTree (standard) :**
```python
import xml.etree.ElementTree as ET

# Parser fichier XML
tree = ET.parse('config.xml')
root = tree.getroot()

# Accéder aux éléments
print(f"Racine: {root.tag}")

# Parcourir les enfants directs
for child in root:
    print(f"  {child.tag}: {child.text}")

# Accéder par chemin
nom = root.find('nom').text
age = root.find('age').text
print(f"{nom}, {age} ans")

# Accéder aux attributs
utilisateur = root.find('utilisateur')
user_id = utilisateur.get('id')
print(f"ID: {user_id}")
```

**Recherche avec XPath :**
```python
import xml.etree.ElementTree as ET

tree = ET.parse('rapport.xml')
root = tree.getroot()

# Trouver tous les éléments
vulnerabilites = root.findall('.//ReportItem[@severity="4"]')

print(f"Vulnérabilités critiques: {len(vulnerabilites)}")

for vuln in vulnerabilites:
    port = vuln.get('port')
    nom = vuln.get('pluginName')
    cvss = vuln.find('cvss_base_score').text
    print(f"  Port {port}: {nom} (CVSS: {cvss})")
```

**Écriture XML :**
```python
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Créer structure
root = ET.Element('configuration')

# Ajouter éléments
database = ET.SubElement(root, 'database')
ET.SubElement(database, 'host').text = 'localhost'
ET.SubElement(database, 'port').text = '5432'
ET.SubElement(database, 'name').text = 'mydb'

# Ajouter élément avec attributs
server = ET.SubElement(root, 'server', attrib={'ssl': 'true', 'timeout': '30'})
ET.SubElement(server, 'address').text = '192.168.1.100'

# Formater avec indentation
xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")

# Sauvegarder
with open('output.xml', 'w', encoding='utf-8') as f:
    f.write(xml_str)

print("✅ Fichier XML créé")
```

**Parser rapport Nessus :**
```python
import xml.etree.ElementTree as ET
from collections import defaultdict

def analyser_nessus(fichier_xml):
    """Analyse un rapport Nessus XML"""
    
    tree = ET.parse(fichier_xml)
    root = tree.getroot()
    
    stats = {
        'hosts': 0,
        'vulns_par_severite': defaultdict(int),
        'cves': set(),
        'vulns_critiques': []
    }
    
    # Parcourir les hôtes
    for host in root.findall('.//ReportHost'):
        stats['hosts'] += 1
        hostname = host.get('name')
        
        # Parcourir les vulnérabilités
        for item in host.findall('.//ReportItem'):
            severity = item.get('severity')
            stats['vulns_par_severite'][severity] += 1
            
            # CVEs
            for cve in item.findall('cve'):
                stats['cves'].add(cve.text)
            
            # Vulnérabilités critiques
            if severity == '4':
                vuln = {
                    'host': hostname,
                    'port': item.get('port'),
                    'nom': item.get('pluginName'),
                    'cvss': item.find('cvss_base_score').text if item.find('cvss_base_score') is not None else 'N/A'
                }
                stats['vulns_critiques'].append(vuln)
    
    # Affichage
    print(f"=== Analyse Nessus ===")
    print(f"Hôtes scannés: {stats['hosts']}")
    print(f"\nVulnérabilités par sévérité:")
    for sev, count in sorted(stats['vulns_par_severite'].items(), reverse=True):
        severite_nom = {
            '0': 'Info',
            '1': 'Low',
            '2': 'Medium',
            '3': 'High',
            '4': 'Critical'
        }.get(sev, 'Unknown')
        print(f"  {severite_nom}: {count}")
    
    print(f"\nCVEs uniques: {len(stats['cves'])}")
    
    print(f"\n🚨 Vulnérabilités critiques ({len(stats['vulns_critiques'])}):")
    for vuln in stats['vulns_critiques'][:10]:
        print(f"  {vuln['host']}:{vuln['port']} - {vuln['nom']} (CVSS: {vuln['cvss']})")

# Utilisation
analyser_nessus('nessus_scan.xml')
```

**Utiliser lxml (plus puissant) :**
```python
from lxml import etree

# Parser avec validation
schema = etree.XMLSchema(file='schema.xsd')
parser = etree.XMLParser(schema=schema)

try:
    tree = etree.parse('config.xml', parser)
    print("✅ XML valide selon le schéma")
except etree.XMLSyntaxError as e:
    print(f"❌ Erreur XML: {e}")
```

### :fontawesome-brands-js: JavaScript (Node.js)

**Lecture XML avec xml2js :**
```javascript
const fs = require('fs');
const xml2js = require('xml2js');

// Installation : npm install xml2js

// Parser XML
const xmlString = fs.readFileSync('config.xml', 'utf8');

xml2js.parseString(xmlString, (err, result) => {
    if (err) {
        console.error('❌ Erreur:', err);
        return;
    }
    
    // Accéder aux données (converti en objet JS)
    const utilisateur = result.utilisateur;
    console.log(`Nom: ${utilisateur.nom[0]}`);
    console.log(`Âge: ${utilisateur.age[0]}`);
    
    // Attributs
    if (utilisateur.$) {
        console.log(`ID: ${utilisateur.$.id}`);
    }
});

// Version async/await
async function parserXml() {
    const xmlString = fs.readFileSync('config.xml', 'utf8');
    const parser = new xml2js.Parser();
    
    try {
        const result = await parser.parseStringPromise(xmlString);
        console.log(JSON.stringify(result, null, 2));
    } catch (err) {
        console.error('❌ Erreur:', err);
    }
}
```

**Écriture XML :**
```javascript
const xml2js = require('xml2js');
const fs = require('fs');

const builder = new xml2js.Builder({
    xmldec: { version: '1.0', encoding: 'UTF-8' },
    renderOpts: { pretty: true, indent: '    ' }
});

const config = {
    configuration: {
        database: {
            host: 'localhost',
            port: 5432,
            name: 'mydb'
        },
        server: {
            $: { ssl: 'true', timeout: '30' },
            address: '192.168.1.100'
        }
    }
};

const xml = builder.buildObject(config);

fs.writeFileSync('output.xml', xml, 'utf8');
console.log('✅ Fichier XML créé');
```

**Parser avec xpath :**
```javascript
const xpath = require('xpath');
const dom = require('xmldom').DOMParser;
const fs = require('fs');

// Installation : npm install xpath xmldom

const xmlString = fs.readFileSync('rapport.xml', 'utf8');
const doc = new dom().parseFromString(xmlString);

// Requête XPath
const vulns = xpath.select('//ReportItem[@severity="4"]', doc);

console.log(`Vulnérabilités critiques: ${vulns.length}`);

vulns.forEach(vuln => {
    const port = vuln.getAttribute('port');
    const nom = vuln.getAttribute('pluginName');
    
    const cvssNode = xpath.select('cvss_base_score/text()', vuln)[0];
    const cvss = cvssNode ? cvssNode.nodeValue : 'N/A';
    
    console.log(`  Port ${port}: ${nom} (CVSS: ${cvss})`);
});
```

**Analyser SAML Response :**
```javascript
const xml2js = require('xml2js');
const fs = require('fs');

async function analyserSAML(fichierXml) {
    const xmlString = fs.readFileSync(fichierXml, 'utf8');
    const parser = new xml2js.Parser({
        tagNameProcessors: [xml2js.processors.stripPrefix],
        attrNameProcessors: [xml2js.processors.stripPrefix]
    });
    
    const result = await parser.parseStringPromise(xmlString);
    
    const assertion = result.Response.Assertion[0];
    const subject = assertion.Subject[0];
    const attributes = assertion.AttributeStatement[0].Attribute;
    
    console.log('=== SAML Authentication ===');
    console.log(`User: ${subject.NameID[0]._}`);
    
    console.log('\nAttributes:');
    attributes.forEach(attr => {
        const name = attr.$.Name;
        const values = attr.AttributeValue.map(v => v._);
        console.log(`  ${name}: ${values.join(', ')}`);
    });
}

// Utilisation
analyserSAML('saml_response.xml');
```

### :fontawesome-brands-php: PHP

**Lecture XML avec SimpleXML :**
```php
<?php

// Parser fichier XML
$xml = simplexml_load_file('config.xml');

// Accéder aux éléments
echo "Nom: " . $xml->nom . "\n";
echo "Âge: " . $xml->age . "\n";

// Accéder aux attributs
$id = (string)$xml['id'];
echo "ID: $id\n";

// Parcourir les enfants
foreach ($xml->children() as $child) {
    echo "{$child->getName()}: {$child}\n";
}
?>
```

**Recherche avec XPath :**
```php
<?php

$xml = simplexml_load_file('rapport.xml');

// Enregistrer namespaces si nécessaire
$xml->registerXPathNamespace('ns', 'http://example.com/namespace');

// Requête XPath
$vulns = $xml->xpath('//ReportItem[@severity="4"]');

echo "Vulnérabilités critiques: " . count($vulns) . "\n\n";

foreach ($vulns as $vuln) {
    $port = (string)$vuln['port'];
    $nom = (string)$vuln['pluginName'];
    $cvss = (string)$vuln->cvss_base_score;
    
    echo "Port $port: $nom (CVSS: $cvss)\n";
}
?>
```

**Écriture XML avec DOMDocument :**
```php
<?php

// Créer document
$dom = new DOMDocument('1.0', 'UTF-8');
$dom->formatOutput = true;

// Créer racine
$root = $dom->createElement('configuration');
$dom->appendChild($root);

// Ajouter éléments
$database = $dom->createElement('database');
$root->appendChild($database);

$host = $dom->createElement('host', 'localhost');
$database->appendChild($host);

$port = $dom->createElement('port', '5432');
$database->appendChild($port);

// Élément avec attributs
$server = $dom->createElement('server');
$server->setAttribute('ssl', 'true');
$server->setAttribute('timeout', '30');
$root->appendChild($server);

$address = $dom->createElement('address', '192.168.1.100');
$server->appendChild($address);

// Sauvegarder
$dom->save('output.xml');
echo "✅ Fichier XML créé\n";
?>
```

**Parser configuration firewall :**
```php
<?php

function analyserFirewallConfig($fichierXml) {
    $xml = simplexml_load_file($fichierXml);
    
    echo "=== Configuration Firewall ===\n";
    echo "Hostname: {$xml->hostname}\n";
    echo "Version: {$xml->version}\n\n";
    
    // Interfaces
    echo "Interfaces:\n";
    foreach ($xml->interfaces->interface as $iface) {
        $name = (string)$iface['name'];
        $nameif = (string)$iface->nameif;
        $ip = (string)$iface->{'ip-address'};
        $security = (string)$iface->{'security-level'};
        
        echo "  $name ($nameif) - $ip - Security Level: $security\n";
    }
    
    // Access Lists
    echo "\nAccess Lists:\n";
    foreach ($xml->{'access-lists'}->{'access-list'} as $acl) {
        $aclName = (string)$acl['name'];
        echo "  ACL: $aclName\n";
        
        foreach ($acl->ace as $ace) {
            $action = (string)$ace['action'];
            $proto = (string)$ace->protocol;
            $src = (string)$ace->source;
            $dst = (string)$ace->destination;
            $desc = (string)$ace->description;
            
            echo "    $action $proto $src -> $dst ($desc)\n";
        }
    }
}

// Utilisation
analyserFirewallConfig('firewall_config.xml');
?>
```

### :fontawesome-brands-golang: Go (Golang)

**Lecture XML :**
```go
package main

import (
    "encoding/xml"
    "fmt"
    "os"
)

type Configuration struct {
    XMLName  xml.Name `xml:"configuration"`
    Nom      string   `xml:"nom"`
    Prenom   string   `xml:"prenom"`
    Age      int      `xml:"age"`
    Actif    bool     `xml:"actif"`
}

func main() {
    // Lire fichier
    data, err := os.ReadFile("config.xml")
    if err != nil {
        panic(err)
    }
    
    // Parser XML
    var config Configuration
    err = xml.Unmarshal(data, &config)
    if err != nil {
        panic(err)
    }
    
    fmt.Printf("Nom: %s\n", config.Nom)
    fmt.Printf("Âge: %d\n", config.Age)
}
```

**Structures avec attributs :**
```go
package main

import (
    "encoding/xml"
    "os"
)

type Utilisateur struct {
    XMLName xml.Name `xml:"utilisateur"`
    ID      string   `xml:"id,attr"`
    Role    string   `xml:"role,attr"`
    Nom     string   `xml:"nom"`
    Prenom  string   `xml:"prenom"`
}

func main() {
    data, _ := os.ReadFile("utilisateur.xml")
    
    var user Utilisateur
    xml.Unmarshal(data, &user)
    
    fmt.Printf("%s %s (ID: %s, Role: %s)\n", 
        user.Prenom, user.Nom, user.ID, user.Role)
}
```

**Écriture XML :**
```go
package main

import (
    "encoding/xml"
    "os"
)

type Config struct {
    XMLName  xml.Name  `xml:"configuration"`
    Database Database  `xml:"database"`
    Server   Server    `xml:"server"`
}

type Database struct {
    Host string `xml:"host"`
    Port int    `xml:"port"`
    Name string `xml:"name"`
}

type Server struct {
    SSL     string `xml:"ssl,attr"`
    Timeout string `xml:"timeout,attr"`
    Address string `xml:"address"`
}

func main() {
    config := Config{
        Database: Database{
            Host: "localhost",
            Port: 5432,
            Name: "mydb",
        },
        Server: Server{
            SSL:     "true",
            Timeout: "30",
            Address: "192.168.1.100",
        },
    }
    
    // Marshaler avec indentation
    output, err := xml.MarshalIndent(config, "", "    ")
    if err != nil {
        panic(err)
    }
    
    // Ajouter déclaration XML
    xmlStr := xml.Header + string(output)
    
    // Écrire fichier
    os.WriteFile("output.xml", []byte(xmlStr), 0644)
    
    fmt.Println("✅ Fichier XML créé")
}
```

**Parser rapport Nessus :**
```go
package main

import (
    "encoding/xml"
    "fmt"
    "os"
)

type NessusReport struct {
    XMLName xml.Name     `xml:"NessusClientData_v2"`
    Report  ReportDetail `xml:"Report"`
}

type ReportDetail struct {
    Name  string       `xml:"name,attr"`
    Hosts []ReportHost `xml:"ReportHost"`
}

type ReportHost struct {
    Name  string       `xml:"name,attr"`
    Items []ReportItem `xml:"ReportItem"`
}

type ReportItem struct {
    Port        string  `xml:"port,attr"`
    Severity    string  `xml:"severity,attr"`
    PluginName  string  `xml:"pluginName,attr"`
    Description string  `xml:"description"`
    RiskFactor  string  `xml:"risk_factor"`
    CVSSScore   string  `xml:"cvss_base_score"`
    CVE         string  `xml:"cve"`
}

func analyserNessus(fichierXml string) {
    data, _ := os.ReadFile(fichierXml)
    
    var report NessusReport
    xml.Unmarshal(data, &report)
    
    fmt.Println("=== Analyse Nessus ===")
    fmt.Printf("Rapport: %s\n", report.Report.Name)
    fmt.Printf("Hôtes: %d\n\n", len(report.Report.Hosts))
    
    critiques := 0
    for _, host := range report.Report.Hosts {
        for _, item := range host.Items {
            if item.Severity == "4" {
                critiques++
                fmt.Printf("🚨 %s:%s - %s (CVSS: %s)\n",
                    host.Name, item.Port, item.PluginName, item.CVSSScore)
            }
        }
    }
    
    fmt.Printf("\nTotal vulnérabilités critiques: %d\n", critiques)
}

func main() {
    analyserNessus("nessus_scan.xml")
}
```

### :fontawesome-brands-rust: Rust

**Lecture XML avec serde-xml-rs :**
```rust
use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
struct Configuration {
    nom: String,
    prenom: String,
    age: u32,
    actif: bool,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string("config.xml")?;
    let config: Configuration = serde_xml_rs::from_str(&data)?;
    
    println!("Nom: {}", config.nom);
    println!("Âge: {}", config.age);
    
    Ok(())
}
```

**Structures avec attributs :**
```rust
use serde::Deserialize;
use std::fs;

#[derive(Debug, Deserialize)]
struct Utilisateur {
    #[serde(rename = "@id")]
    id: String,
    #[serde(rename = "@role")]
    role: String,
    nom: String,
    prenom: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let data = fs::read_to_string("utilisateur.xml")?;
    let user: Utilisateur = serde_xml_rs::from_str(&data)?;
    
    println!("{} {} (ID: {}, Role: {})", 
        user.prenom, user.nom, user.id, user.role);
    
    Ok(())
}
```

**Écriture XML :**
```rust
use serde::Serialize;
use std::fs;

#[derive(Debug, Serialize)]
struct Config {
    database: Database,
    server: Server,
}

#[derive(Debug, Serialize)]
struct Database {
    host: String,
    port: u16,
    name: String,
}

#[derive(Debug, Serialize)]
struct Server {
    #[serde(rename = "@ssl")]
    ssl: String,
    #[serde(rename = "@timeout")]
    timeout: String,
    address: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = Config {
        database: Database {
            host: "localhost".to_string(),
            port: 5432,
            name: "mydb".to_string(),
        },
        server: Server {
            ssl: "true".to_string(),
            timeout: "30".to_string(),
            address: "192.168.1.100".to_string(),
        },
    };
    
    let xml = serde_xml_rs::to_string(&config)?;
    
    // Ajouter déclaration XML
    let xml_full = format!("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n{}", xml);
    
    fs::write("output.xml", xml_full)?;
    
    println!("✅ Fichier XML créé");
    
    Ok(())
}
```

**Parser avec quick-xml (performant) :**
```rust
use quick_xml::events::Event;
use quick_xml::Reader;
use std::fs;

fn analyser_nessus(fichier_xml: &str) -> Result<(), Box<dyn std::error::Error>> {
    let xml = fs::read_to_string(fichier_xml)?;
    let mut reader = Reader::from_str(&xml);
    reader.trim_text(true);
    
    let mut buf = Vec::new();
    let mut critiques = 0;
    let mut in_critical = false;
    
    loop {
        match reader.read_event(&mut buf) {
            Ok(Event::Start(ref e)) => {
                if e.name() == b"ReportItem" {
                    for attr in e.attributes() {
                        let attr = attr?;
                        if attr.key == b"severity" && attr.value.as_ref() == b"4" {
                            in_critical = true;
                            critiques += 1;
                        }
                    }
                }
            }
            Ok(Event::End(ref e)) => {
                if e.name() == b"ReportItem" {
                    in_critical = false;
                }
            }
            Ok(Event::Eof) => break,
            Err(e) => return Err(Box::new(e)),
            _ => {}
        }
        buf.clear();
    }
    
    println!("Vulnérabilités critiques: {}", critiques);
    
    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    analyser_nessus("nessus_scan.xml")
}
```

## Bonnes pratiques

### Validation XML

**DTD (Document Type Definition) :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE utilisateur [
    <!ELEMENT utilisateur (nom, prenom, age, email?)>
    <!ELEMENT nom (#PCDATA)>
    <!ELEMENT prenom (#PCDATA)>
    <!ELEMENT age (#PCDATA)>
    <!ELEMENT email (#PCDATA)>
    <!ATTLIST utilisateur
        id ID #REQUIRED
        actif (true|false) "true">
]>
<utilisateur id="u123" actif="true">
    <nom>Dupont</nom>
    <prenom>Alice</prenom>
    <age>28</age>
    <email>alice@example.com</email>
</utilisateur>
```

**XSD (XML Schema Definition) - Plus puissant :**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    
    <xs:element name="utilisateur">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="nom" type="xs:string"/>
                <xs:element name="prenom" type="xs:string"/>
                <xs:element name="age" type="xs:positiveInteger"/>
                <xs:element name="email" type="xs:string" minOccurs="0"/>
            </xs:sequence>
            <xs:attribute name="id" type="xs:ID" use="required"/>
            <xs:attribute name="actif" type="xs:boolean" default="true"/>
        </xs:complexType>
    </xs:element>
    
</xs:schema>
```

### Sécurité XML

!!! danger "Vulnérabilités XML courantes"
    
    **1. XXE (XML External Entity) Injection**
    ```xml
    <?xml version="1.0"?>
    <!DOCTYPE foo [
        <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <data>&xxe;</data>
    ```
    
    **Protection :** Désactiver entités externes
    ```python
    # Python
    parser = ET.XMLParser()
    parser.entity = {}  # Désactiver entités
    
    # PHP
    libxml_disable_entity_loader(true);
    ```
    
    **2. Billion Laughs Attack (XML Bomb)**
    ```xml
    <!DOCTYPE lolz [
        <!ENTITY lol "lol">
        <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
        <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
        <!-- ... -->
    ]>
    <lolz>&lol9;</lolz>
    ```
    
    **Protection :** Limiter taille et profondeur
    
    **3. XPath Injection**
    ```python
    # ❌ VULNÉRABLE
    username = request.POST['username']
    xpath = f"//user[name='{username}']"
    
    # ✅ SÉCURISÉ - Paramétrage
    # Utiliser bibliothèques avec paramètres liés
    ```

### Performance

!!! tip "Optimisations XML"
    - **Streaming** pour gros fichiers (SAX parser, non DOM)
    - **Compression** : gzip les XML volumineux
    - **Caching** : Parser une fois, réutiliser
    - **Alternatives** : Considérer JSON/Protobuf si possible

### Quand utiliser XML vs JSON

| Critère | XML | JSON |
|---------|-----|------|
| **Lisibilité** | ⚠️ Verbeux | ✅ Concis |
| **Métadonnées** | ✅ Attributs, namespaces | ⚠️ Limité |
| **Validation** | ✅ XSD puissant | ⚠️ JSON Schema moins mature |
| **Standards existants** | ✅ SOAP, RSS, SVG, Office | ✅ APIs REST modernes |
| **Commentaires** | ✅ Natifs | ❌ Aucun |
| **Performance parsing** | ⚠️ Plus lent | ✅ Plus rapide |
| **Taille fichier** | ❌ Gros | ✅ Compact |

**Recommandations :**
- **Utilisez XML** pour : SOAP, systèmes legacy, standards industriels (HL7, XBRL), configuration complexe (Maven, Spring), documents (Office)
- **Utilisez JSON** pour : APIs REST modernes, configuration simple, communication web, stockage NoSQL

## Le mot de la fin

!!! quote
    **XML a façonné l'échange de données structurées** pendant deux décennies et reste **essentiel** dans de nombreux domaines malgré le déclin de son usage pour les nouvelles APIs. Sa **rigueur syntaxique**, sa **capacité de validation**, et son **support des métadonnées** en font un choix solide pour les systèmes nécessitant **fiabilité et traçabilité**.
    
    Chaque langage offre des outils robustes pour manipuler XML :
    
    - **Python** avec `ElementTree` (standard) et `lxml` (puissant)
    - **JavaScript** avec `xml2js` pour conversion objet/XML
    - **PHP** avec `SimpleXML` et `DOMDocument` natifs
    - **Go** avec `encoding/xml` type-safe
    - **Rust** avec `serde-xml-rs` et `quick-xml` performant
    
    Maîtriser XML c'est comprendre ses **forces** (validation stricte, namespaces, standards matures) et ses **faiblesses** (verbosité, complexité, vulnérabilités XXE). Dans les environnements **legacy, financiers, médicaux, et gouvernementaux**, XML reste **incontournable** et le restera pour des années.

---
