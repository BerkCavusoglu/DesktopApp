from ast import Index
import enum
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from panel import *

#Interface Operations
app = QApplication(sys.argv)
window = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)
window.show()

#Database Operations
import sqlite3

connection = sqlite3.connect("record.db")
operations = connection.cursor()
connection.commit()
table = operations.execute("Create Table if Not Exists Record(Name text,Surname text,Company text)")
connection.commit()

ui.tbl1.setHorizontalHeaderLabels(("Ad","Soyad","Company"))
def record_add():
    Name = ui.lne1.text()
    Surname = ui.lne2.text()
    Company = ui.cmb1.currentText()
    
    try:
        add = "insert into Regist(Name,Surname,Company) values (?,?,?)"
        operations.execute(add,(Name,Surname,Company))
        connection.commit()
        ui.statusbar.showMessage("Record Added !",10000)
        record_add
    except:
        ui.statusbar.showMessage("Record Not Added !",10000)
        
    def list_record():
        ui.tbl1.clear()
        ui.tbl1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ui.tbl1.setHorizontalHeaderLabels(("Name","Surname","Company"))
        query = "select * from Regist"
        operations.execute(query)
        
        for indexRow,RegistNumber in enumerate(operations):
            for IndexColumn,RecordColumn in enumerate(RegistNumber):
                ui.tbl1.setItem(indexRow,IndexColumn,QTableWidgetItem(str(RecordColumn)))
                
    def Record_delete():
        delete_message = QMessageBox.question(window,"Delete Confirm","Are you sure want to delete ?")
        QMessageBox.Yes |QMessageBox.No
        
        if delete_message == QMessageBox.Yes:
            Selected_Record = ui.tbl1.selectedItems()
            Delete_Record = Selected_Record[0].text()
            
            query = "delete from Record where Ad = ?"
            
            try:
                operations.execute(query,(Delete_Record,))
                connection.commit()
                ui.statusbar.showMessage("Record deleted",10000)
                list_record()
            except:
                ui.statusbar.showMessage("Record deleted failed",10000)
            
        else:
            ui.statusbar.showMessage("Operations cancelled",10000)
                
    def list_by_company():
        listcompany = ui.cmb2.currentText()
        query = "select * from Record where Company = ?"
        operations.execute(query,(list_by_company,))
        ui.tbl1.clear()
        ui.tbl1.setHorizontalHeaderLabels(("Name","Surname","Company"))
        for indexRow,RegistNumber in enumerate(operations):
            for IndexColumn,RecordColumn in enumerate(RegistNumber):
                ui.tbl1.setItem(indexRow,IndexColumn,QTableWidgetItem(str(RecordColumn)))
    #Buttons
    ui.btn1.clicked.connect(record_add)
    ui.btn2.clicked.connect(Record_delete)
    ui.btn3.clicked.connect(list_by_company)
sys.exit(app.exec_())

