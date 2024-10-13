PY=python3
SHELL := /bin/bash
PYTHON3_OK := $(shell python3 --version 2> /dev/null)

.PHONY: help init install test run clean

.DEFAULT_GOAL := help

# Afficher la liste des commandes disponibles
help:
	@echo "Commandes disponibles :"
	@echo "  make init    - Initialiser l'environnement virtuel et installer les dépendances"
	@echo "  make install - Installer toutes les bibliothèques requises"
	@echo "  make test    - Exécuter les tests unitaires pour valider le code"
	@echo "  make run     - Exécuter le pipeline ETL"
	@echo "  make clean   - Supprimer l'environnement et les fichiers temporaires"

# Initialiser l'environnement virtuel et installer les dépendances
init: check-python
	@echo "Initialisation de l'environnement virtuel..."
	$(PY) -m venv .env
	@echo "Activation de l'environnement et installation des dépendances..."
	source .env/bin/activate && $(MAKE) install

# Installer les dépendances listées dans requirements.txt
install:
	@echo "Installation des dépendances..."
	source .env/bin/activate && pip install -r requirements.txt
	@echo "Installation du projet terminée."

# Exécuter les tests unitaires avec unittest
test:
	@echo "Exécution des tests unitaires..."
	source .env/bin/activate && python -m unittest discover tests
	@echo "Tests terminés."

# Exécuter le pipeline ETL
run:
	@echo "Exécution du pipeline ETL..."
	source .env/bin/activate && python pipeline.py

# Nettoyer l'environnement et supprimer les fichiers temporaires
clean:
	@echo "Nettoyage de l'espace de travail du projet..."
	rm -rf .env
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	@echo "Nettoyage terminé."

# Vérifier si Python 3 est installé
check-python:
ifndef PYTHON3_OK
	$(error "Python 3 est requis mais non trouvé. Veuillez installer Python 3.")
endif
