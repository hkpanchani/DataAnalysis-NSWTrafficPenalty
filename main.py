import sys
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QButtonGroup
from view import Ui_MainWindow
from dataModel import Dataset

file = 'dataset\\dataset.csv'

class Main(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setComboBoxes()
        self.initialiseTable()

    def setComboBoxes(self):
        filter_by = ['All Penalty Cases','Camera or Radar Cases','Mobile Phone Cases']
        analysis_over = ['Over Time','Offence Code','Location Code']
        
        # Initialise FilterBy Drop Down 
        for item in filter_by:
            self.ui.filterBySpin.addItem(item)
        
        # Initialise Analysys Over Drop Down
        for item in analysis_over:
            self.ui.analysisOverSpin.addItem(item)

    def initialiseTable(self):
        # ds.getModel()
        self.ui.table.setModel(ds.getAllData())

    # def clearTableData(self):
    #     self.ui.table.clar

if __name__ == "__main__":
    ds = Dataset(filepath=file)
    df = ds.dateFilter(start_date='1/3/2012',end_date='1/5/2012')
    # print(df)

    # To be used when GUI Window is ready
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

    