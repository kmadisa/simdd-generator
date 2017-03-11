#!/usr/bin/python
 
# Import PySide classes
import sys
import json
from PySide.QtCore import *
from PySide.QtGui import *
from functools import partial

# Create a Qt application
#app = QApplication(sys.argv)
# Create a Label and show it
#label = QLabel("Hello World")
#label.show()
#main_win = QMainWindow()

#_attributes = {}
_simdd_attr = {}
_simdd_attr['dynamicAttributes'] = []


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        wid = QWidget()
        wid.resize(250, 150)

        # Configure the window's dimensions.
        self.setCentralWidget(wid)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('SIMMD Generator')
        self.setWindowIcon(QIcon('troll.jpg'))

        # Add buttons to the main window.
        add_attr_button = QPushButton('Add attribute information', wid)
        add_attr_button.setToolTip('Add attribute information for simulation')
        add_attr_button.resize(add_attr_button.sizeHint())
        add_attr_button.move(80, 50)
        add_attr_button.clicked.connect(self.add_attr)

        add_cmd_button = QPushButton('Add command information', wid)
        add_cmd_button.setToolTip('Add command information for simulation')
        add_cmd_button.resize(add_cmd_button.sizeHint())
        add_cmd_button.move(80, 80)

        add_cmd_ovride_button = QPushButton('Add command override info', wid)
        add_cmd_ovride_button.setToolTip('Add override information for simulation')
        add_cmd_ovride_button.resize(add_cmd_ovride_button.sizeHint())
        add_cmd_ovride_button.move(80, 150)

        cancel_button = QPushButton('Cancel', wid)
        cancel_button.setToolTip('Close the application.')
        cancel_button.resize(cancel_button.sizeHint())

        generate_file_button = QPushButton('Generate SIMMD file', wid)
        generate_file_button.setToolTip('Write the information to a json file.')
        generate_file_button.resize(generate_file_button.sizeHint())
        generate_file_button.move(80, 180)
        generate_file_button.clicked.connect(self.gen_simdd_file)

        # Configure the layout of the main window.
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(generate_file_button)
        hbox.addWidget(cancel_button)
        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(add_attr_button)
        vbox.addWidget(add_cmd_button)
        vbox.addWidget(add_cmd_ovride_button)
        vbox.addLayout(hbox)

        # Menu bar actions
        openAction = QAction('&Open', self)
        openAction.setStatusTip('Open a json file')

        saveAction = QAction('&Save', self)
        saveAction.setStatusTip('Save a json file')

        saveAsAction = QAction('&Save As', self)
        saveAsAction.setStatusTip('Save a json file using another file name')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Close the application')
        exitAction.triggered.connect(self.close)

        # Add a menubar to the main window.
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addMenu('&Open recent')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(exitAction)
        editMenu = menubar.addMenu('&Edit')

        wid.setLayout(vbox)
        self.show()

    def add_attr(self, *args):
        dialog = QDialog()
        labels = []
        text_fields = [] 

        name = QLabel('name')
        labels.append(name)
        quant_type = QLabel('quantity_simulation_type')
        labels.append(quant_type)
        min_bound = QLabel('min_bound')
        labels.append(min_bound)
        max_bound = QLabel('max_bound')
        labels.append(max_bound)
        mean = QLabel('mean')
        labels.append(mean)
        max_slew_rate = QLabel('max_slew_rate')
        labels.append(max_slew_rate)
        update_period = QLabel('update_period')
        labels.append(update_period)
        std_dev = QLabel('std_dev')
        labels.append(std_dev)


        nameEdit = QLineEdit()
        text_fields.append(nameEdit)
        quant_typeEdit = QLineEdit()
        text_fields.append(quant_typeEdit)
        min_boundEdit = QLineEdit()
        text_fields.append(min_boundEdit)
        max_boundEdit = QLineEdit()
        text_fields.append(max_boundEdit)
        meanEdit = QLineEdit()
        text_fields.append(meanEdit)
        max_slew_rateEdit = QLineEdit()
        text_fields.append(max_slew_rateEdit)
        update_periodEdit = QLineEdit()
        text_fields.append(update_periodEdit)
        std_devEdit = QLineEdit()
        text_fields.append(std_devEdit)


        #edit = QLineEdit('enter som som')
        button = QPushButton('Add')
        but = QPushButton('Cancel')

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(name, 1, 0)
        grid.addWidget(nameEdit, 1, 1)
        grid.addWidget(quant_type, 2, 0)
        grid.addWidget(quant_typeEdit, 2, 1)
        grid.addWidget(min_bound, 3, 0)
        grid.addWidget(min_boundEdit, 3, 1)
        grid.addWidget(max_bound, 4, 0)
        grid.addWidget(max_boundEdit, 4, 1)
        grid.addWidget(mean, 5, 0)
        grid.addWidget(meanEdit, 5, 1)
        grid.addWidget(max_slew_rate, 6, 0)
        grid.addWidget(max_slew_rateEdit, 6, 1)
        grid.addWidget(update_period, 7, 0)
        grid.addWidget(update_periodEdit, 7, 1)
        grid.addWidget(std_dev, 8, 0)
        grid.addWidget(std_devEdit, 8, 1)

        grid.addWidget(button, 9, 0)
        grid.addWidget(but, 9, 1)
        dialog.setLayout(grid)

        button.clicked.connect(partial(self.add, labels, text_fields, dialog))
        but.clicked.connect(partial(self.cancel, dialog))
        dialog.exec_()

    def add(self, labels, text_fields, dialog):
        attr = {}
        for label, textfield in zip(labels, text_fields):
            attr[label.text()] = textfield.text()
        sim_info = {}
        sim_info['dataSimulationParameters'] = {}
        for key in attr.keys():
            if key != 'name':
                if key in ['min_bound', 'max_bound', 'mean', 'max_slew_rate', 'update_period', 'std_dev']:
                    try:
                        sim_info['dataSimulationParameters'].update({key:float(attr[key])})
                    except ValueError:
                        mb = QMessageBox()
                        mb.setText("The value for the variable {} is not a valid number".format(key))
                        mb.exec_()
                        return
                else:
                    sim_info['dataSimulationParameters'].update({key:attr[key]})
        _attributes = {}
        _attributes['basicAttributeData'] = {}
        _attributes['basicAttributeData'].update({'name': attr['name']})
        _attributes['basicAttributeData'].update(sim_info)
        _simdd_attr['dynamicAttributes'].append(_attributes)
        print _simdd_attr
        dialog.close()

    def cancel(self, *args):
        sys.exit()

    def gen_simdd_file(self):
        print 'generating file...'
        with open('weather_SIMDD.json', 'w') as fp:
            json.dump(_simdd_attr, fp)
        print 'done!!'


def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
