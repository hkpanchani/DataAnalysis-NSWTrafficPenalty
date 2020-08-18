import sys
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QButtonGroup
from view import Ui_MainWindow
from dataModel import Dataset

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)




if __name__ == "__main__":
    file = 'dataset\\dataset.csv'
    ds = Dataset(filepath=file)
    df = ds.dateFilter(start_date='1/3/2012',end_date='1/5/2012')
    print(df)

    # To be used when GUI Window is ready
    # app = QtWidgets.QApplication(sys.argv)
    # window = Main()
    # window.show()
    # sys.exit(app.exec_())

    