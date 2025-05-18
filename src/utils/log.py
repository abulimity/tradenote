import settings
import os
from datetime import datetime
from logging import getLogger, StreamHandler, Formatter
from logging.handlers import RotatingFileHandler

log_level = settings.LOG_LEVEL
log_dir = settings.LOG_PATH
log_format = settings.LOG_FORMATTER
log_file_name = f"log_{datetime.now().strftime('%Y-%m-%d %H:%M')}.log"
log_file_path = log_dir.joinpath(log_file_name)

log_file_max_size = 64 * 1024
log_file_log_backup_count = 8
log_file_encoding = "utf-8"

formatter = Formatter(log_format)

rotating_file_handler = RotatingFileHandler(
    filename=log_file_path,
    maxBytes=log_file_max_size,
    backupCount=log_file_log_backup_count,
    encoding=log_file_encoding
)
rotating_file_handler.setLevel(log_level)
rotating_file_handler.setFormatter(formatter)

console_handler = StreamHandler()
console_handler.setLevel(log_level)
console_handler.setFormatter(formatter)

logger = getLogger()

logger.setLevel(log_level)
logger.addHandler(rotating_file_handler)
logger.addHandler(console_handler)