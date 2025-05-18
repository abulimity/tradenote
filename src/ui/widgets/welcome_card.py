from qfluentwidgets import CardWidget, ListWidget, SubtitleLabel, PushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from ..widgets.recent_portfolio_card import AllPortfolioCard

class WelcomeCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('welcomeWidget')
        self.initUI()
    
    def initUI(self):
        # 创建主布局
        self.mainLayout = QVBoxLayout(self)
        # 创建左侧卡片
        self.leftCard = CardWidget(self)

        # 创建Logo 和 标题
        self.titleLayout = QHBoxLayout()
        self.logoLabel = SubtitleLabel('🗒️', self)
        self.titleLabel = SubtitleLabel('TradeNote', self)
        self.titleLayout.addWidget(self.logoLabel)
        self.titleLayout.addWidget(self.titleLabel)
        # 创建按钮部分
        self.createBnt = PushButton('创建投资组合', self, FIF.ADD)
        self.openBnt = PushButton('打开投资组合', self, FIF.FOLDER)
        # 将Logo 和 标题添加到左侧布局
        self.mainLayout.addLayout(self.titleLayout)
        # 将按钮添加到左侧布局
        self.mainLayout.addWidget(self.createBnt)
        self.mainLayout.addWidget(self.openBnt)


        # 设置主布局
        self.setLayout(self.mainLayout)
        # 设置布局间距
        self.mainLayout.setSpacing(16)
        self.mainLayout.setContentsMargins(16, 16, 16, 16)
        