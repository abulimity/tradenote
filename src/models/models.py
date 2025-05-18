from src.database import DatabaseManager
from src.utils.log import logger
from datetime import datetime


class BaseModel:
    table_name = None
    columns = []
    db_manager = DatabaseManager()

    def __init__(self, **kwargs):

        self.data_dict = {}
        # 遍历 kwargs 中的键值对
        for key, value in kwargs.items():
            if key in self.columns:
                setattr(self, key, value)
                self.data_dict[key] = value
            else:
                logger.warning(f"Key '{key}' is not a valid attribute of {self.__class__.__name__}, ignoring.")
        # 处理未在 kwargs 中提供的列，设置为 None
        for col in self.columns:
            if col not in self.data_dict:
                setattr(self, col, None)
                self.data_dict[col] = None

    def create(self):
        """新增数据"""
        if not self.db_manager.connect():
            logger.error("无法连接到数据库，新增数据失败")
            return None

        data = {col: getattr(self, col) for col in self.columns if hasattr(self, col)}
        try:
            record_id = self.db_manager.insert(self.table_name, data)
            setattr(self, 'id', record_id)
            self.data_dict['id'] = record_id
            logger.info(f"成功在 {self.table_name} 表中新增记录，ID: {record_id}")
            return record_id
        except Exception as e:
            logger.error(f"在 {self.table_name} 表中新增记录失败: {e}")
            return None
        finally:
            self.db_manager.disconnect()

    @classmethod
    def get_by_id(cls, db_manager: DatabaseManager, record_id):
        """根据 ID 查询数据"""
        if not db_manager.connect():
            logger.error("无法连接到数据库，查询数据失败")
            return None

        try:
            result = db_manager.select(cls.table_name, where="id = ?", params=(record_id,))
            if result:
                data = dict(zip(cls.columns, result[0]))
                instance = cls(db_manager, **data)
                return instance
            return None
        except Exception as e:
            logger.error(f"在 {cls.table_name} 表中根据 ID 查询记录失败: {e}")
            return None
        finally:
            db_manager.disconnect()

    def delete(self):
        """删除数据"""
        if not self.db_manager.connect():
            logger.error("无法连接到数据库，删除数据失败")
            return False

        try:
            self.db_manager.delete(self.table_name, "id = ?", (self.id,))
            logger.info(f"成功在 {self.table_name} 表中删除记录，ID: {self.id}")
            return True
        except Exception as e:
            logger.error(f"在 {self.table_name} 表中删除记录失败: {e}")
            return False
        finally:
            self.db_manager.disconnect()

    def __str__(self):
        """打印对象信息"""
        attributes = ', '.join([f"{col}={getattr(self, col)}" for col in self.columns if hasattr(self, col)])
        return f"{self.__class__.__name__}({attributes})"

    @classmethod
    def get_all(cls):
        """
        批量查询模型对应表中的所有数据
        :param db_manager: 数据库管理器实例
        :return: 包含所有记录的列表字典
        """
        if not cls.db_manager.connect():
            logger.error("无法连接到数据库，批量查询数据失败")
            return []

        try:
            result = cls.db_manager.select(cls.table_name)
            all_records = []
            for row in result:
                record = dict(zip(cls.columns, row))
                all_records.append(record)
            return all_records
        except Exception as e:
            logger.error(f"在 {cls.table_name} 表中批量查询记录失败: {e}")
            return []
        finally:
            cls.db_manager.disconnect()


class Portfolio(BaseModel):
    table_name = "tb_portfolio"
    columns = ["id", "name", "desc_msg", "crt_dt", "update_dt", "is_del"]

    def create(self):
        self.data_dict["crt_dt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data_dict["update_dt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for key, value in self.data_dict.items():
            setattr(self, key, value)
        return super().create()


class SecAccount(BaseModel):
    table_name = "tb_sec_account"
    columns = ["id", "name", "crt_dt", "is_del"]


class CashAccount(BaseModel):
    table_name = "tb_cash_account"
    columns = ["id", "name", "currency_type", "crt_dt", "is_del"]


class PortfolioSecAccountRel(BaseModel):
    table_name = "tb_portfolio_sec_account_rel"
    columns = ["id", "portfolio_id", "sec_account_id", "is_del", "crt_dt"]


class SecCashAccountRel(BaseModel):
    table_name = "tb_sec_cash_account_rel"
    columns = ["id", "sec_id", "cash_id", "is_del", "crt_dt"]
