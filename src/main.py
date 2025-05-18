import sys
from PyQt6.QtWidgets import QApplication
from ui.view.main_view import WelcomeView
from controller.welcome_contorller import WelcomeController
from src.utils.log import logger

if __name__ == '__main__':
    logger.info("open main view")
    app = QApplication(sys.argv)
    view = WelcomeView()
    # controller = WelcomeController()
    view.show()
    app.exec()