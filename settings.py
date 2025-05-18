from pathlib import Path
import os

# LOG
ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
LOG_LEVEL = "DEBUG"
LOG_FORMATTER = "%(asctime)s-%(levelname)s-%(name)s-%(filename)s %(lineno)d: %(message)s"
LOG_PATH = ROOT_PATH.joinpath(r"logs")
DATABASE_PATH = ROOT_PATH.joinpath(r"data/tradenote.db")