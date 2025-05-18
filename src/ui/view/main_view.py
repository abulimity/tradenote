from qfluentwidgets import FluentWindow, FluentIcon as FIF
from src.ui.subinterface.welcome_interface import WelcomeInterface


class WelcomeView(FluentWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.welcomeInterface = WelcomeInterface(self)
        # self.homeInterface = HomeWidget(self)
        # self.createPortfolioInterface = CreatePortfolioWidget(self)
        
        self.initNavigation()
        self.initWindow()
    
    def initNavigation(self):
        self.addSubInterface(self.welcomeInterface, FIF.HOME, '欢迎')
        # self.addSubInterface(self.homeInterface, FIF.DOCUMENT, '主页')
        # self.addSubInterface(self.createPortfolioInterface, FIF.ADD, '创建投资组合')
    
    def initWindow(self):
        self.resize(800, 600)
        self.setWindowTitle('TradeNote')