from QtSplashScreen import SplashScreen
from PyQt5.QtWidgets import QApplication
import sys
app=QApplication(sys.argv)
splash=SplashScreen()
splash.show()
sys.exit(app.exec_())