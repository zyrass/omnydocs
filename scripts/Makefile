# ============================================================================
# Makefile : génération de zensical.toml à partir de fragments TOML
# ============================================================================

# Fichier TOML final utilisé par Zensical (NE PAS éditer à la main).
TOML_OUT = zensical.toml

# Fichier de base [project] (sans nav).
PROJECT_HEAD = config/toml/00-project-core.toml

# Fragments de navigation (dans l'ordre).
NAV_PARTS = \
	config/toml/navigation/00-nav-header.toml \
	config/toml/navigation/10-nav-accueil.toml \
	config/toml/navigation/20-nav-bases-fondamentaux.toml \
	config/toml/navigation/99-nav-footer.toml

# Reste de la configuration (thème, markdown, extras, etc.).
PROJECT_TAIL = config/toml/10-project-theme-and-markdown.toml

.PHONY: config clean show

# Génère zensical.toml
config:
	@echo "🔧 Génération de $(TOML_OUT)..."
	@cat $(PROJECT_HEAD) > $(TOML_OUT)
	@echo "" >> $(TOML_OUT)
	@cat $(NAV_PARTS) >> $(TOML_OUT)
	@echo "" >> $(TOML_OUT)
	@cat $(PROJECT_TAIL) >> $(TOML_OUT)
	@echo "✅ $(TOML_OUT) généré."

# Debug : affiche le TOML généré
show: config
	@echo "-----------------------------"
	@cat $(TOML_OUT)
	@echo "-----------------------------"

# Nettoyage
clean:
	@rm -f $(TOML_OUT)
	@echo "🧹 $(TOML_OUT) supprimé."
