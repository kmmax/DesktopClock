import time

from PyQt5.QtWidgets import QLabel, QGridLayout, QWidget, \
    QSystemTrayIcon, QSizePolicy, QMenu, QAction, qApp, QDesktopWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QIcon


class DesktopClock(QWidget):
    """Часы, отображаемые на рабочем столе. Управление через системный трей"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__lbl1: QLabel = None
        self.__layout: QGridLayout = None
        self.__initUI()

        # SystemTray
        self.tray_icon = QSystemTrayIcon(self)
        self.__initSystemTray()

        # Timer
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.__timeout)
        self.__timer.start(1000)

    def closeEvent(self, event):
        """Overriding the closeEvent method to intercept the window closing event"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Desktop Clock",
            "DesktopClock was minimized to Tray",
            QSystemTrayIcon.Information,
            2000
        )

    def __initUI(self):

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        """Initialization of clock widget """

        localtime = time.localtime()
        str_time = time.strftime("%H:%M:%S", localtime)
        self.__lbl1: QLabel = QLabel(str_time, self)
        self.__lbl1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__lbl1.setAlignment(Qt.AlignCenter)
        self.__lbl1.setStyleSheet("QLabel {color: yellow; font-size:80px;}")

        self.__layout = QGridLayout()
        self.__layout.addWidget(self.__lbl1, 0, 0)
        self.setLayout(self.__layout)

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)   # hide window and frame
        self.setGeometry(50, 50, 100, 100)
        self.setAttribute(Qt.WA_TranslucentBackground)

        monitor = QDesktopWidget().screenGeometry(1) # monitor secondary monitor
        self.move(monitor.left() + int(monitor.width() / 2 - int(self.width() / 2)), monitor.top())

    def __initSystemTray(self):
        """Initialization of system tray of widget

            Menu:
            - show - show widget
            - hide - hide widget
            - set movable - show widget as window (it can be move)
            - set static - Makes a widget without a border (not movable)
            - exit - Closing the application

        """

        self.tray_icon.setIcon(QIcon("./images/clock.png"))

        # Menu
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)

        hide_action = QAction("Hide", self)
        hide_action.triggered.connect(self.hide)

        moveable_action = QAction("Set Moveable", self)
        moveable_action.triggered.connect(self.__setMovable)

        immovable_action = QAction("Set Immovable", self)
        immovable_action.triggered.connect(self.__setImMovable)

        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(moveable_action)
        tray_menu.addAction(immovable_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)

        self.tray_icon.show()

    @pyqtSlot()
    def __timeout(self):
        """Timer timeout for displaying current time"""
        localtime = time.localtime()
        str_time = time.strftime("%H:%M:%S", localtime)
        self.__lbl1.setText(str_time)

    @pyqtSlot()
    def __setMovable(self):
        """Activation of immovable mode"""
        self.setWindowFlags(Qt.Tool)
        self.show()

    @pyqtSlot()
    def __setImMovable(self):
        """Activation of immovable mode"""
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

