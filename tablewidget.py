import csv
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.tableWidget = QTableWidget()

        self.label = QLabel()
        self.label.setText("Итого:")
        self.label.setAlignment(Qt.AlignRight)

        self.summ = QLineEdit()
        self.summ.setAlignment(Qt.AlignRight)
        self.summ.setFixedWidth(70)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)

        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.label)
        self.layout2.addWidget(self.summ)

        self.layout.addLayout(self.layout2)

        self.setLayout(self.layout)

        self.loadTable('price.csv')
        self.show()


    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            title = next(reader)
            title.append('Количество')
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
                self.tableWidget.setItem(i, j + 1, QTableWidgetItem("0"))



        #self.tableWidget.resizeColumnsToContents()
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tableWidget.cellChanged.connect(self.calcSum)

    def calcSum(self, crow, ccol):
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        resnum = 0
        for i in range(rows):
            resnum += int(self.tableWidget.item(i, cols - 2).text()) *\
                      int(self.tableWidget.item(i, cols - 1).text())
        self.summ.setText(str(resnum))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())