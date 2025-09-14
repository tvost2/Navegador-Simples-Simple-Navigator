import sys
from PyQt5.QtWidgets import QApplication
from navegador import Navegador

if __name__ == "__main__":
    app = QApplication(sys.argv)
    nav = Navegador()
    nav.show()
    sys.exit(app.exec_())