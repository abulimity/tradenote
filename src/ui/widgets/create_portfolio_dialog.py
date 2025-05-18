from qfluentwidgets import MessageBoxBase, SubtitleLabel, PushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from .create_portfolio_card import CreatePortfolioCard

class CreatePortfolioDialog(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置对话框标题
        # self.titleLabel = SubtitleLabel('创建新的投资组合', self)
        
        # 创建投资组合创建卡片
        self.createPortfolioCard = CreatePortfolioCard()
        
        # 设置对话框内容
        self.viewLayout.addWidget(self.createPortfolioCard)
        
        # 设置对话框标题样式
        # self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        
        # 设置布局边距
        self.viewLayout.setContentsMargins(16, 16, 16, 16)
        self.viewLayout.setSpacing(16)
        
        # 移动到父窗口中心
        self.moveToParentCenter()
        
        # 调整对话框大小以适应内容
        # self.adjustSize()
    
    def moveToParentCenter(self):
        """将对话框移动到父窗口中心"""
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = (parent_rect.height() - self.height()) // 2
            self.move(x, y)
        