from qfluentwidgets import CardWidget, ListWidget, SubtitleLabel, PushButton, Dialog
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from ..widgets.recent_portfolio_card import RecentPortfolioCard
from ..widgets.welcome_card import WelcomeCard
from ..widgets.create_portfolio_dialog import CreatePortfolioDialog

class WelcomeInterface(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('welcomeWidget')
        self.initUI()
    
    def initUI(self):
        # 创建主布局
        self.mainLayout = QHBoxLayout(self)

        # 左侧欢迎卡片
        self.welcome_card = WelcomeCard()
        # 右侧卡片
        self.recent_portfolio_card = RecentPortfolioCard()
        
        # 创建右侧容器卡片
        self.rightCard = CardWidget(self)
        self.rightLayout = QVBoxLayout(self.rightCard)
        self.rightLayout.addWidget(self.recent_portfolio_card)
        
        self.mainLayout.addWidget(self.welcome_card)
        self.mainLayout.addWidget(self.rightCard)
        
        # 设置布局间距
        self.mainLayout.setSpacing(16)
        self.mainLayout.setContentsMargins(16, 16, 16, 16)
        
        # 连接信号
        self.welcome_card.createBnt.clicked.connect(self.showCreateDialog)

    
    def showCreateDialog(self):
        """显示创建投资组合对话框"""
        dialog = CreatePortfolioDialog(self)
        dialog.exec()
        