from src.models.models import Portfolio

class WelcomeController(object):
    def __init__(self):
        self.portfolio_model_cls = Portfolio

    @staticmethod
    def query_portfolio_list():
        portfolio_list = Portfolio().get_all()
        return portfolio_list