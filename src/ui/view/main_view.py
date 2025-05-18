from qfluentwidgets import FluentWindow, FluentIcon as FIF
from src.ui.subinterface.welcome_interface import WelcomeInterface
from src.ui.subinterface.portfolio_detail_interface import PortfolioDetailInterface


class WelcomeView(FluentWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.welcomeInterface = WelcomeInterface(self)
        self.portfolioInterface = PortfolioDetailInterface(self)
        # self.createPortfolioInterface = CreatePortfolioWidget(self)
        
        self.initNavigation()
        self.initWindow()
    
    def initNavigation(self):
        self.addSubInterface(self.welcomeInterface, FIF.HOME, '欢迎')
        self.addSubInterface(self.portfolioInterface, FIF.DOCUMENT, '投资组合')
        # self.addSubInterface(self.createPortfolioInterface, FIF.ADD, '创建投资组合')
    
    def initWindow(self):
        self.resize(800, 600)
        self.setWindowTitle('TradeNote')