import settings
import os
from pathlib import Path

def test_settings():
    print("root_path=%s"%settings.ROOT_PATH)
    assert settings.ROOT_PATH == Path(r"D:\project\python\tradenote")
