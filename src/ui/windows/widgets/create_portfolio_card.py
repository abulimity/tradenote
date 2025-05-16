from qfluentwidgets import CardWidget, SubtitleLabel, setFont,LineEdit,ComboBox, FluentIcon as FIF, IconWidget
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class CreatePortfolioCard(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('createPortfolioCard')
        self.initUI()

    def initUI(self):
        # 创建主布局
        self.layout = QVBoxLayout(self)

        # 创建并设置标签字体
        self.portfolioNameLabel = SubtitleLabel('投资组合名称：', self)
        setFont(self.portfolioNameLabel, 14)
        self.portfolioNameEdit = LineEdit(self)
        self.portfolioNameEdit.setPlaceholderText('请输入投资组合名称')

        # 选择投资组合展示货币
        self.currencyLabel = SubtitleLabel('选择结算货币：', self)
        setFont(self.currencyLabel, 14)
        self.currencyComboBox = ComboBox(self)
        self.currencyComboBox.addItems(['CNY', 'USD', 'EUR', 'HKD'])

        # 选择关联证券账户
        self.accountLabel = SubtitleLabel('选择关联证券账户：', self)
        setFont(self.accountLabel, 14)
        self.accountComboBox = ComboBox(self)
        self.accountComboBox.addItems(['账户1', '账户2', '账户3'])

        # 添加现金账户 至少需要一个现金账户
        self.cashAccountLabel = SubtitleLabel('添加现金账户：', self)
        setFont(self.cashAccountLabel, 14)
        self.cashAccountComboBox = ComboBox(self)
        self.cashAccountComboBox.addItems(['账户1', '账户2', '账户3'])

        # 设置布局间距
        self.layout.setSpacing(10)
        
        # 添加组件到布局
        self.layout.addWidget(self.portfolioNameLabel)
        self.layout.addWidget(self.portfolioNameEdit)
        self.layout.addWidget(self.currencyLabel)
        self.layout.addWidget(self.currencyComboBox)
        self.layout.addWidget(self.accountLabel)
        self.layout.addWidget(self.accountComboBox)
        self.layout.addWidget(self.cashAccountLabel)
        self.layout.addWidget(self.cashAccountComboBox)

        # 设置卡片固定大小
        self.setFixedSize(300, 400)