from src.models import Portfolio
from src.database import DatabaseManager
from datetime import datetime
from src.utils.log import logger
import pytest



def test_portfolio_create():
    portfolio = Portfolio(
                          name="test_name_3",
                          desc_msg='test desc msg',
                          crt_dt=datetime.now(),
                          is_del=0
    )
    portfolio.create()

def test_portfolio_getall(db_manager):
    portfolio_list = Portfolio.get_all(db_manager)

    assert len(portfolio_list) == 5
    for item in portfolio_list:
        logger.debug(item)
