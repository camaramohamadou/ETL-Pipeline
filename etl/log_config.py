import logging

def setup_logger():
    # Configuration basique du logger
    logger = logging.getLogger('etl_pipeline')
    logger.setLevel(logging.INFO)  # Niveau de log (peut être ajusté à DEBUG)

    # Créer un format pour les messages de log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Handler pour écrire les logs dans un fichier
    file_handler = logging.FileHandler("data/output/pipeline.log")
    file_handler.setFormatter(formatter)

    # Handler pour afficher les logs dans la console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Ajouter les handlers au logger
    if not logger.handlers:  # Évite d'ajouter plusieurs handlers lors de multiples initialisations
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
