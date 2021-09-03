from PyQt5.QtWidgets import QApplication

from DesktopClock import DesktopClock


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mw1 = DesktopClock()
    mw1.show()
    sys.exit(app.exec())