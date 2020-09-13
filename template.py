from PyQt5 import QtCore, QtGui, QtWidgets
import re

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 200)
        self.create_button = QtWidgets.QPushButton(Dialog)
        self.create_button.setGeometry(QtCore.QRect(70, 130, 75, 23))
        self.create_button.clicked.connect(self.openCreateWindow)
        self.load_button = QtWidgets.QPushButton(Dialog)
        self.load_button.setGeometry(QtCore.QRect(220, 130, 75, 23))
        self.load_button.clicked.connect(self.openLoadWindow)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 70, 171, 16))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Template Maker"))
        self.create_button.setText(_translate("Dialog", "Create"))
        self.load_button.setText(_translate("Dialog", "Load"))
        self.label.setText(_translate("Dialog", "Create or Load a Template"))

    def openCreateWindow(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Create")
        self.dialog.resize(600, 575)

        # Text Boxes
        self.template_text = QtWidgets.QTextEdit(self.dialog)
        self.template_text.setGeometry(QtCore.QRect(50, 50, 500, 300))

        self.variable_text = QtWidgets.QTextEdit(self.dialog)
        self.variable_text.setGeometry(QtCore.QRect(50, 450, 350, 100))
        self.variable_text.setPlaceholderText("Word 1\nWord 2\nWord 3")

        # Buttons
        self.create_variable = QtWidgets.QPushButton(self.dialog)
        self.create_variable.setGeometry(QtCore.QRect(450, 375, 100, 25))
        self.create_variable.setText("Add Variable")
        self.create_variable.clicked.connect(self.format)

        self.save = QtWidgets.QPushButton(self.dialog)
        self.save.setGeometry(QtCore.QRect(450, 450, 100, 40))
        self.save.setText("Save")
        self.save.clicked.connect(self.format)

        self.copy_button = QtWidgets.QPushButton(self.dialog)
        self.copy_button.setGeometry(QtCore.QRect(450, 510, 100, 40))
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(self.copy)

        # Labels
        self.template_label = QtWidgets.QLabel(self.dialog)
        self.template_label.setGeometry(QtCore.QRect(50, 25, 500, 25))
        self.template_label.setText("Input template below. Denote variables by highlighting desired variables and clicking the variable button.")

        self.variable_label = QtWidgets.QLabel(self.dialog)
        self.variable_label.setGeometry(QtCore.QRect(50, 415, 350, 25))
        self.variable_label.setText("Input variables in order, each on a new line.")

        self.dialog.show()

    def openLoadWindow(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.show()

    def format(self):
        self.template_text.cut()
        self.template_text.insertPlainText("_____")

    def copy(self):  
        # Get text in template box
        self.template_text.selectAll()
        text = self.template_text.textCursor().selectedText()
        text_variables = 0
        space = "_____"
        for match in re.finditer(space, text):
            text_variables += 1

        # Get text in variable box
        self.variable_text.selectAll()
        var_text = self.variable_text.textCursor().selectedText()
        variables = var_text.split("\u2029")
        print(text)
        print(variables)

        if variables[0] == '':
            var_count = 0
        else:
            var_count = len(variables)

        if text == '' and text_variables == 0:
            self.error_window = QtWidgets.QDialog()
            self.error_window.setWindowTitle("Error")
            self.error_window.resize(300, 100)

            self.variable_label = QtWidgets.QLabel(self.error_window)
            self.variable_label.setGeometry(QtCore.QRect(110, 25, 120, 25))
            self.variable_label.setText("Nothing to copy!")

            self.close_error = QtWidgets.QPushButton(self.error_window)
            self.close_error.setGeometry(QtCore.QRect(125, 50, 50, 25))
            self.close_error.setText("Close")
            self.close_error.clicked.connect(self.close_error_window)

            self.error_window.show()
        # If the number of variables does not match the number of blank spaces
        elif text_variables != var_count:
            self.error_window = QtWidgets.QDialog()
            self.error_window.setWindowTitle("Error")
            self.error_window.resize(300, 100)

            self.variable_label = QtWidgets.QLabel(self.error_window)

            if text_variables > var_count:
                self.variable_label.setGeometry(QtCore.QRect(100, 25, 120, 25))
                self.variable_label.setText("Input to few variables!")
            else:
                self.variable_label.setGeometry(QtCore.QRect(95, 25, 120, 25))
                self.variable_label.setText("Input to many variables!")

            self.close_error = QtWidgets.QPushButton(self.error_window)
            self.close_error.setGeometry(QtCore.QRect(125, 50, 50, 25))
            self.close_error.setText("Close")
            self.close_error.clicked.connect(self.close_error_window)

            self.error_window.show()
        else:   
            for word in range(0, text_variables):
                text = text.replace(space, variables[word], 1)

            self.result = QtWidgets.QTextEdit(self.dialog)
            self.result.setGeometry(QtCore.QRect(-5000, 50, 500, 300))
            self.result.setText(text)
            self.result.selectAll()
            self.result.copy()

    def close_error_window(self):
        self.error_window.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
