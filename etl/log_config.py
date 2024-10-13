import logging

def setup_logger():
    # Configuration basique du logger
    logging.basicConfig(
        level=logging.INFO,  # Niveau de log (peut être ajusté à DEBUG pour plus de détails)
        format="%(asctime)s - %(levelname)s - %(message)s",  # Format des messages de log
        handlers=[
            logging.FileHandler("data/output/pipeline.log"),  # Fichier de log
            logging.StreamHandler()  # Affiche aussi dans la console
        ]
    )
    logger = logging.getLogger()
    return logger
