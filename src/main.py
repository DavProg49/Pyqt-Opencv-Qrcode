import sys

from PyQt5.QtWidgets import QApplication

from module.gui import StartWindow
from module.scanner import Camera

if __name__ == '__main__':
    camera = Camera(0)
    app = QApplication(sys.argv)
    window = StartWindow(camera)
    window.show()
    sys.exit(app.exec_())
