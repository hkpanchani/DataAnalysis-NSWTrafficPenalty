import sys
import datetime
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QButtonGroup
from view import Ui_MainWindow
from dataModel import Dataset
from matplotlib import pyplot as plt
import collections

choice = None
allRecords = True
filterBySpinOptions = [[],['Camera','Radar'],['mobile']]

file = 'dataset\\dataset.csv'

class Main(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.modeGroup = QButtonGroup()
        self.modeGroup.addButton(self.ui.filterRecord)
        self.modeGroup.addButton(self.ui.plotGraph)
        
        self.ui.allRecordsCB.clicked.connect(self.allRecordsCBMode)

        self.ui.filterRecord.clicked.connect(self.onClickedMode)
        self.ui.plotGraph.clicked.connect(self.onClickedMode)

        self.ui.submitBtn.clicked.connect(self.execute)

        self.initialiseDefaultOptions()

        # Default UI initialisation calls
        self.setComboBoxes()
        self.initialiseTable()

    def onClickedMode(self):
        global choice
        radioBtn = self.sender()
        if radioBtn.isChecked():
            if radioBtn.text() == "Filter Records":
                choice = "filterRecord"
                self.ui.analysisOverSpin.setEnabled(False)
                self.ui.filterBySpin.setEnabled(True) 
            elif radioBtn.text() == "Plot a Graph":
                choice = "plotGraph"
                self.ui.filterBySpin.setEnabled(False)
                self.ui.analysisOverSpin.setEnabled(True)                
            
    def initialiseDefaultOptions(self):
        self.ui.allRecordsCB.setChecked(True)
        self.ui.startDateEdit.setEnabled(False)
        self.ui.endDateEdit.setEnabled(False)
        self.ui.filterRecord.setChecked(True)
        self.ui.analysisOverSpin.setEnabled(False)

    def allRecordsCBMode(self):
        global allRecords
        if self.ui.allRecordsCB.isChecked():
            allRecords = True
            self.ui.startDateEdit.setEnabled(False)
            self.ui.endDateEdit.setEnabled(False)
        else:
            allRecords = False
            self.ui.startDateEdit.setEnabled(True)
            self.ui.endDateEdit.setEnabled(True)

    def setComboBoxes(self):
        filter_by = ['All Penalty Cases','Camera or Radar Cases','Mobile Phone Cases']
        analysis_over = ['Distribution of Cases per offence code','Mobile phone usage over time','Mobile phone usage over Offence code','Distribution of Cases per Speed Band']
        
        # Initialise FilterBy Drop Down 
        for item in filter_by:
            self.ui.filterBySpin.addItem(item)
        
        # Initialise Analysys Over Drop Down
        for item in analysis_over:
            self.ui.analysisOverSpin.addItem(item)

    def initialiseTable(self):
        df = ds.getAllData()
        model = ds.getModel(df)
        self.ui.table.setModel(model)

    def filterDateWiseRecords(self):
        model = ds.dateFilter(start_date='1/3/2012',end_date='1/5/2012') #working
        self.ui.table.setModel(model)
    
    def execute(self):
        global allRecords,filterBySpinOptions
        df = ds.getAllData()

        if self.ui.filterRecord.isChecked():
            if self.ui.allRecordsCB.isChecked():
                df = ds.getAllData()
                pass
            else:
                start_date = datetime.datetime.strftime(self.ui.startDateEdit.date().toPyDate(),'%d/%m/%Y')
                end_date = datetime.datetime.strftime(self.ui.endDateEdit.date().toPyDate(),'%d/%m/%Y')
                df = ds.dateFilter(start_date,end_date,df)
            
            df = ds.filterBy(filterBySpinOptions[self.ui.filterBySpin.currentIndex()],df)

            self.ui.table.setModel(ds.getModel(df))
        
        if self.ui.plotGraph.isChecked():
            if self.ui.allRecordsCB.isChecked():
                df = ds.getAllData()
                pass
            else:
                start_date = datetime.datetime.strftime(self.ui.startDateEdit.date().toPyDate(),'%d/%m/%Y')
                end_date = datetime.datetime.strftime(self.ui.endDateEdit.date().toPyDate(),'%d/%m/%Y')
                df = ds.dateFilter(start_date,end_date,df)

            anlSpinInd = self.ui.analysisOverSpin.currentIndex()

            if anlSpinInd == 0:
                self.piePlot(df['OFFENCE_CODE'].value_counts().to_dict())
            elif anlSpinInd == 1:
                df = ds.filterBy(['mobile'],df)
                self.linePlot(df['OFFENCE_FINYEAR'].value_counts().to_dict())
            elif anlSpinInd == 2:
                df = ds.filterBy(['mobile'],df)
                self.piePlot(df['OFFENCE_CODE'].value_counts().to_dict())
            elif anlSpinInd == 3:
                self.piePlot(df['SPEED_BAND'].value_counts().to_dict())
                


            # print(df['OFFENCE_CODE'].value_counts().to_dict())
            # print(sum(list(df['OFFENCE_CODE'].value_counts().to_dict())))

    def piePlot(self,dict):
        print(dict)
        keys = list(dict.keys())
        values = list(dict.values())

        total = sum(values)

        othersValue = sum(values[10:])
        keys = keys[:11]
        values = values[:11]

        keys.append("Others")
        values.append(othersValue)

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        # ax.set_title(self.ui.analysisOverSpin.currentText(),bbox={'facecolor':'0.8', 'pad':3})
        ax.axis('equal')
        ax.pie(values, labels = keys,autopct='%1.2f%%')
        plt.title(self.ui.analysisOverSpin.currentText()) 
        plt.legend(keys,loc="upper right")
        # plt.get_current_fig_manager().
        plt.show()

    def linePlot(self,dict):
        dict = collections.OrderedDict(sorted(dict.items()))
        keys = list(dict.keys())
        values = list(dict.values())
        print(keys)

        plt.scatter(keys, values, color= "green", marker= "*", s=30) 
        
        plt.xlabel('Financial Year')
        plt.ylabel('Cases')
        plt.title(self.ui.analysisOverSpin.currentText()) 
        plt.legend() 
        
        plt.show() 


if __name__ == "__main__":
    ds = Dataset(filepath=file)
    # print(df)

    # To be used when GUI Window is ready
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())

    