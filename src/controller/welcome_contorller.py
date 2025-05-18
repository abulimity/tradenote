from src.ui.view.welcome_view import WelcomeView
from src.models.models import Portfolio

class WelcomeController(object):
    def __init__(self):
        self.portfolio_model_cls = Portfolio
        self.welcome_view = WelcomeView


    def query_portfolio_list(self):
        pass