import sys
from PyQt6.QtWidgets import (QApplication, QFrame, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QTreeWidget,
                           QTreeWidgetItem, QTableWidget, QSplitter)
from PyQt6.QtCore import Qt
from qfluentwidgets import (FluentWindow, SubtitleLabel, setFont, 
                          PrimaryPushButton, CardWidget, FluentIcon as FIF,
                          TreeWidget, TableWidget)

class WelcomeWidget(CardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        # 设置唯一的对象名称
        self.setObjectName('welcomeInterface')
        self.setupUI()

    def setupUI(self):
        # 创建标题部分
        titleLayout = QVBoxLayout()
        self.logoLabel = SubtitleLabel('🗒️', self)  # 使用emoji作为临时logo
        self.titleLabel = SubtitleLabel('TradeNote', self)
        
        # 设置字体和对齐
        setFont(self.logoLabel, 48)
        setFont(self.titleLabel, 36)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        titleLayout.addWidget(self.logoLabel)
        titleLayout.addWidget(self.titleLabel)
        titleLayout.setSpacing(10)
        
        # 创建按钮部分
        buttonLayout = QVBoxLayout()
        self.openFileBtn = PrimaryPushButton('打开文件', self, FIF.FOLDER)
        self.createFileBtn = PrimaryPushButton('创建文件', self, FIF.ADD)
        self.recentFileBtn = PrimaryPushButton('近期文件', self, FIF.HISTORY)
        
        # 设置按钮大小和样式
        for btn in [self.openFileBtn, self.createFileBtn, self.recentFileBtn]:
            btn.setFixedWidth(200)
            buttonLayout.addWidget(btn)
        
        buttonLayout.setSpacing(10)
        
        # 添加到主布局
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(titleLayout)
        self.vBoxLayout.addSpacing(30)
        self.vBoxLayout.addLayout(buttonLayout)
        self.vBoxLayout.addStretch(1)
        
        # 设置卡片样式
        self.setFixedWidth(400)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)

class HomeWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('homeInterface')
        self.setupUI()

    def setupUI(self):
        # 创建主布局
        layout = QHBoxLayout(self)
        
        # 创建左侧树状菜单
        self.treeWidget = TreeWidget(self)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setFixedWidth(200)
        
        # 添加一些示例树节点
        root = QTreeWidgetItem(self.treeWidget, ['交易记录'])
        child1 = QTreeWidgetItem(root, ['2024年'])
        child2 = QTreeWidgetItem(child1, ['1月'])
        
        # 创建右侧区域
        rightWidget = QFrame(self)
        rightLayout = QVBoxLayout(rightWidget)
        
        # 创建右侧上下分割器
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 创建表格区域
        self.tableWidget = TableWidget(self)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['日期', '交易品种', '方向', '数量', '价格'])
        
        # 创建图表区域
        self.chartFrame = QFrame()
        self.chartFrame.setStyleSheet('background-color: #f0f0f0;')
        chartLayout = QVBoxLayout(self.chartFrame)
        chartLabel = SubtitleLabel('图表区域', self)
        chartLayout.addWidget(chartLabel)
        
        # 添加到分割器
        splitter.addWidget(self.tableWidget)
        splitter.addWidget(self.chartFrame)
        
        # 设置分割器比例
        splitter.setStretchFactor(0, 3)  # 表格区域占3
        splitter.setStretchFactor(1, 2)  # 图表区域占2
        
        # 添加到右侧布局
        rightLayout.addWidget(splitter)
        
        # 添加到主布局
        layout.addWidget(self.treeWidget)
        layout.addWidget(rightWidget)
        
        # 设置布局边距
        layout.setContentsMargins(0, 0, 0, 0)
        rightLayout.setContentsMargins(16, 16, 16, 16)

class Window(FluentWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.welcomeInterface = WelcomeWidget(self)
        self.homeInterface = HomeWidget(self)
        
        self.initNavigation()
        self.initWindow()
    
    def initNavigation(self):
        self.addSubInterface(self.welcomeInterface, FIF.HOME, '欢迎')
        self.addSubInterface(self.homeInterface, FIF.DOCUMENT, '主页')
    
    def initWindow(self):
        self.resize(1000, 600)
        self.setWindowTitle('TradeNote')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()