from PyQt6.QtCore import QEasingCurve
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import CardWidget


class PortfolioDetailInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('PortfolioDetailInterface')
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)  # 启用动画

        # 设置布局间距
        self.mainLayout.setSpacing(16)
        self.mainLayout.setContentsMargins(16, 16, 16, 16)

        # portfolio base info
        self.baseinfoLayout = QHBoxLayout(self)

