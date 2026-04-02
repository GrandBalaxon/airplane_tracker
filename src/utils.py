import json
import logging
from pathlib import Path


logger = logging.getLogger("utils")

def initialize_json_file(file_path: Path) -> None:
    """Функция для проверки существования JSON-файла и его инициализации при его отсутствии."""
    if not file_path.exists():
        logger.info(f"Файл по пути {file_path} не найден. Создаем json файл с пустым словарём.")
        try:
            with open(file_path, 'w') as f:
                json.dump({}, f)
                logger.info(f"Создан файл {file_path.name} с пустым словарем.")
        except Exception as e:
            logger.error(f"Ошибка при создании файла: {e}")
            raise
    else:
        logger.info(f"Файл уже существует: {file_path}.")