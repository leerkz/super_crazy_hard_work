import logging
import os


def setting_log(logger_name: str) -> logging.Logger:
    # Получаем экземпляр логгера с указанным именем
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования DEBUG

    # Определяем директорию для логов в текущей рабочей директории
    log_dir = os.path.join(os.getcwd(), "log")

    # Создаем директорию, если она не существует
    os.makedirs(log_dir, exist_ok=True)

    # Формируем путь к файлу лога
    log_path = os.path.join(log_dir, f"{logger_name}.log")

    # Создаем файловый обработчик лога
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)  # Устанавливаем уровень логирования DEBUG

    # Устанавливаем формат сообщений лога
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Добавляем файловый обработчик к логгеру
    logger.addHandler(file_handler)

    return logger  # Возвращаем настроенный экземпляр логгера
