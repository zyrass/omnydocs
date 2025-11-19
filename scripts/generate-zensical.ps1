# ============================================================================
# Script PowerShell : génération de zensical.toml à partir de fragments TOML
# UTF-8 SANS BOM + CRLF, accents préservés
# ============================================================================

$ErrorActionPreference = "Stop"

$TOML_OUT     = "zensical.toml"

$PROJECT_HEAD = "config/toml/00-project-core.toml"
$NAV_DIR      = "config/toml/navigation"
$PROJECT_TAIL = "config/toml/10-project-theme-and-markdown.toml"

Write-Host "Generation du fichier $TOML_OUT ..."

# On stocke tout dans une simple chaîne
$script:content = ""

function Add-File {
    param(
        [string]$path
    )

    if (-not (Test-Path $path)) {
        throw "Fichier introuvable : $path"
    }

    # Lit le fichier en UTF-8, brut
    $text = Get-Content $path -Raw -Encoding UTF8
    $script:content += $text
}

function Add-CRLF {
    $script:content += "`r`n"
}

# 1) Core [project] sans nav
Add-File $PROJECT_HEAD
Add-CRLF
Add-CRLF

# 2) Navigation (fragments)
Add-File "$NAV_DIR/00-nav-accueil.toml"
Add-CRLF
Add-File "$NAV_DIR/01-nav-bases-fondamentaux.toml"
Add-CRLF
Add-File "$NAV_DIR/02-nav-sys-reseau.toml"
Add-CRLF
Add-File "$NAV_DIR/03-nav-dev-cloud.toml"
Add-CRLF
Add-File "$NAV_DIR/04-nav-devsecops.toml"
Add-CRLF
Add-File "$NAV_DIR/05-nav-cyber.toml"
Add-CRLF
Add-File "$NAV_DIR/06-nav-cyber-outils.toml"
Add-CRLF
Add-File "$NAV_DIR/07-nav-glossaire.toml"
Add-CRLF
Add-CRLF

# 3) Thème / markdown / extras
Add-File $PROJECT_TAIL
Add-CRLF

# Écriture finale en UTF-8 SANS BOM
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($TOML_OUT, $script:content, $utf8NoBom)

Write-Host "Fichier $TOML_OUT genere avec succes (UTF-8 sans BOM, CRLF, accents preservés)."
