from qfluentwidgets import CardWidget, SubtitleLabel, setFont,ListWidget, FluentIcon as FIF, IconWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class AllPortfolioCard(CardWidget):
    def __init__(self,controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setObjectName('recentPortfolioCard')
        self.initUI()

    def initUI(self):
        # 创建主布局
        self.layout = QVBoxLayout(self)

        self.portfolioListTitle = SubtitleLabel('所有投资组合：', self)
        self.portfolioList = ListWidget(self)

        for item in self.controller.query_portfolio_list():
            self.portfolioList.addItem(item['name'])

        # 将右侧标题添加到右侧布局
        self.layout.addStretch(1)
        self.layout.addWidget(self.portfolioListTitle)
        # 将右侧列表添加到右侧布局
        self.layout.addWidget(self.portfolioList)
        self.layout.addStretch(1)