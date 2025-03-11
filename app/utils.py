import logging
import time

def setup_logging():
    """
    Configure le système de logs pour l'application.
    """
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

def log_execution_time(func):
    """
    Décorateur pour mesurer le temps d'exécution d'une fonction.

    Usage:
    @log_execution_time
    def my_function():
        ...
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Execution de {func.__name__} terminée en {execution_time:.4f} secondes")
        return result
    return wrapper
