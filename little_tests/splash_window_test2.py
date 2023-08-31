import sys
from PyQt5 import QtCore, QtGui, QtWidgets     # + QtWidgets


import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import QTimer, Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel("""

            <div style='background:url(../images/splash_title.png);width:400px;height:200px;'>abcada</div>
            """)

    # SplashScreen - Indicates that the window is a splash screen. This is the default type for .QSplashScreen
    # FramelessWindowHint - Creates a borderless window. The user cannot move or resize the borderless window through the window system.
    label.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
    label.show()

    # Automatically exit after  5 seconds
    QTimer.singleShot(5000, app.quit)
    sys.exit(app.exec_())