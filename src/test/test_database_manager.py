from src.database import DatabaseManager
from pathlib import Path
import pytest

@pytest.fixture()
def db_manager():
    # 测试使用临时数据库文件
    test_db_path = Path(r"D:\project\python\tradenote\data\test_tradenote.db")
    db_manager = DatabaseManager(str(test_db_path))
    db_manager.connect()
    yield db_manager
    db_manager.disconnect()
    # 删除临时数据库文件
    # if test_db_path.exists():
    #     test_db_path.unlink()

def test_database_manager_connect(db_manager):
    assert db_manager.db_path == Path(r"D:\project\python\tradenote\data\test_tradenote.db")
    # 因为在 fixture 里已经连接，这里检查连接状态
    assert db_manager.is_connected == True

def test_database_manager_insert(db_manager):
    # 创建测试表
    columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER"
    }
    db_manager.create_table("test_table", columns)

    # 插入数据
    data = {
        "name": "Alice",
        "age": 30
    }
    record_id = db_manager.insert("test_table", data)
    assert record_id is not None
    assert isinstance(record_id, int)

def test_database_manager_select(db_manager):
    # 创建测试表
    columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER"
    }
    db_manager.create_table("test_table", columns)

    # 插入数据
    data = {
        "name": "Bob",
        "age": 25
    }
    record_id = db_manager.insert("test_table", data)

    # 查询数据
    result = db_manager.select("test_table", where="id = ?", params=(record_id,))
    assert len(result) == 1
    assert result[0][1] == "Bob"
    assert result[0][2] == 25

def test_database_manager_update(db_manager):
    # 创建测试表
    columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER"
    }
    db_manager.create_table("test_table", columns)

    # 插入数据
    data = {
        "name": "Charlie",
        "age": 35
    }
    record_id = db_manager.insert("test_table", data)

    # 更新数据
    update_data = {
        "age": 36
    }
    db_manager.update("test_table", update_data, where="id = ?", params=(record_id,))

    # 查询更新后的数据
    result = db_manager.select("test_table", where="id = ?", params=(record_id,))
    assert result[0][2] == 36

def test_database_manager_delete(db_manager):
    # 创建测试表
    columns = {
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "name": "TEXT NOT NULL",
        "age": "INTEGER"
    }
    db_manager.create_table("test_table", columns)

    # 插入数据
    data = {
        "name": "David",
        "age": 40
    }
    record_id = db_manager.insert("test_table", data)

    # 删除数据
    db_manager.delete("test_table", where="id = ?", params=(record_id,))

    # 查询删除后的数据
    result = db_manager.select("test_table", where="id = ?", params=(record_id,))
    assert len(result) == 0


