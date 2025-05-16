from qfluentwidgets import CardWidget, SubtitleLabel, setFont,ListWidget, FluentIcon as FIF, IconWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class RecentPortfolioCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('recentPortfolioCard')
        self.initUI()

    def initUI(self):
        # 创建主布局
        self.layout = QVBoxLayout(self)

        self.portfolioListTitle = SubtitleLabel('近期使用投资组合：', self)
        self.portfolioList = ListWidget(self)

        self.portfolioList.addItem('投资组合1')
        self.portfolioList.addItem('投资组合2')
        self.portfolioList.addItem('投资组合3')
        # 将右侧标题添加到右侧布局
        self.layout.addStretch(1)
        self.layout.addWidget(self.portfolioListTitle)
        # 将右侧列表添加到右侧布局
        self.layout.addWidget(self.portfolioList)
        self.layout.addStretch(1)