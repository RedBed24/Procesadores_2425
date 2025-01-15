import logging

# Configurar el logger
logger = logging.getLogger("partitune_logger")
logger.setLevel(logging.DEBUG)  # Nivel mínimo de los mensajes que se procesarán

# Formato de los mensajes
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Handler para la salida estándar (consola)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Handler para el archivo de log
file_handler = logging.FileHandler("partitune.log", mode="w")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
