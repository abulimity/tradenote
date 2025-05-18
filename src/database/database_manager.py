import sqlite3
import settings
from typing import List, Dict, Optional
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path: str = None):
        """
        初始化数据库管理器
        :param db_path: 数据库文件路径
        """
        if db_path is None:
            db_path = settings.DATABASE_PATH
        self.db_path = Path(db_path)
        self.conn = None
        self.is_connected = False

    def connect(self):
        """
        连接到数据库
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.is_connected = True
            return self.is_connected
        except sqlite3.Error as e:
            print(f"数据库连接错误: {e}")
            self.is_connected = False
            return self.is_connected

    def disconnect(self):
        """
        断开数据库连接
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.is_connected = False

    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        创建数据库表
        :param table_name: 表名
        :param columns: 列定义，键为列名，值为列类型
        """
        if not self.conn:
            print("未连接到数据库")
            return

        columns_def = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"创建表 {table_name} 失败: {e}")

    def insert(self, table_name: str, data: Dict[str, any]):
        """
        插入数据到指定表
        :param table_name: 表名
        :param data: 插入的数据，键为列名，值为插入的值
        :return: 插入记录的 ID
        """
        if not self.conn:
            print("未连接到数据库")
            return None

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"插入数据到 {table_name} 失败: {e}")
            return None

    def select(self, table_name: str, columns: Optional[List[str]] = None, where: Optional[str] = None,
               params: Optional[tuple] = None):
        """
        查询数据
        :param table_name: 表名
        :param columns: 要查询的列，默认为所有列
        :param where: 条件语句
        :param params: 条件参数
        :return: 查询结果
        """
        if not self.conn:
            print("未连接到数据库")
            return []

        if columns is None:
            columns_str = "*"
        else:
            columns_str = ', '.join(columns)

        query = f"SELECT {columns_str} FROM {table_name}"
        if where:
            query += f" WHERE {where}"

        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"查询 {table_name} 数据失败: {e}")
            return []

    def update(self, table_name: str, data: Dict[str, any], where: str, params: tuple):
        """
        更新数据
        :param table_name: 表名
        :param data: 要更新的数据，键为列名，值为更新的值
        :param where: 条件语句
        :param params: 条件参数
        """
        if not self.conn:
            print("未连接到数据库")
            return

        set_clause = ', '.join([f"{col_name} = ?" for col_name in data.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, tuple(data.values()) + params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"更新 {table_name} 数据失败: {e}")

    def delete(self, table_name: str, where: str, params: tuple):
        """
        删除数据
        :param table_name: 表名
        :param where: 条件语句
        :param params: 条件参数
        """
        if not self.conn:
            print("未连接到数据库")
            return

        query = f"DELETE FROM {table_name} WHERE {where}"
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"删除 {table_name} 数据失败: {e}")