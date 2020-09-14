from PyQt5 import QtCore, QtGui, QtWidgets
import re
import os
from os import path
import json

tname = ''

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(365, 200)
        self.create_button = QtWidgets.QPushButton(Dialog)
        self.create_button.setGeometry(QtCore.QRect(70, 130, 75, 23))
        self.create_button.clicked.connect(lambda: self.openCreateWindow('None'))

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
    
    ### Create Commands ###
    def openCreateWindow(self, template = 'None'):
        if path.exists('presets.json'):
            with open('presets.json', 'r') as f:
                presets = json.load(f)
        else:
            presets = {}

        self.create_window = QtWidgets.QDialog()
        self.create_window.setWindowTitle("Create")
        self.create_window.resize(600, 575)

        # Text Boxes
        self.template_text = QtWidgets.QTextEdit(self.create_window)
        self.template_text.setGeometry(QtCore.QRect(50, 50, 500, 300))

        self.variable_text = QtWidgets.QTextEdit(self.create_window)
        self.variable_text.setGeometry(QtCore.QRect(50, 450, 350, 100))
        self.variable_text.setPlaceholderText("Word 1\nWord 2\nWord 3")

        # Buttons
        self.create_variable = QtWidgets.QPushButton(self.create_window)
        self.create_variable.setGeometry(QtCore.QRect(450, 375, 100, 25))
        self.create_variable.setText("Add Variable")
        self.create_variable.clicked.connect(self.format)

        self.create_variable = QtWidgets.QPushButton(self.create_window)
        self.create_variable.setGeometry(QtCore.QRect(175, 375, 100, 25))
        self.create_variable.setText("Select")
        self.create_variable.clicked.connect(self.choose)

        self.save_button = QtWidgets.QPushButton(self.create_window)
        self.save_button.setGeometry(QtCore.QRect(450, 450, 100, 40))
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save)

        self.copy_button = QtWidgets.QPushButton(self.create_window)
        self.copy_button.setGeometry(QtCore.QRect(450, 510, 100, 40))
        self.copy_button.setText("Copy")
        self.copy_button.clicked.connect(self.copy)

        # Set dropdown
        self.template_dropdown = QtWidgets.QComboBox(self.create_window)
        self.template_dropdown.setGeometry(QtCore.QRect(50, 375, 100, 25))
        if template != 'None':
            for keys in presets[template]:
                self.template_dropdown.addItem(keys[0])

        # Labels
        self.template_label = QtWidgets.QLabel(self.create_window)
        self.template_label.setGeometry(QtCore.QRect(50, 25, 500, 25))
        self.template_label.setText("Input template below. Denote variables by highlighting desired variables and clicking the variable button.")

        self.variable_label = QtWidgets.QLabel(self.create_window)
        self.variable_label.setGeometry(QtCore.QRect(50, 415, 350, 25))
        self.variable_label.setText("Input variables in order, each on a new line.")

        self.create_window.show()

    def choose(self):
        global tname
        if path.exists('templates.json'):
            with open('templates.json', 'r') as f:
                templates = json.load(f)

        if path.exists('presets.json'):
            with open('presets.json', 'r') as f:
                presets = json.load(f)

        preset_name = self.template_dropdown.currentText()

        # If there was a preset option
        if preset_name != '':
            for key in presets:
                if key == tname:
                    for sets in presets[key]:
                        if sets[0] == preset_name:
                            self.variable_text.setText(sets[1])
        
    def format(self):
        self.template_text.cut()
        self.template_text.insertPlainText("_____")

    def save(self):
        valid = self.valid_template_check()
        if valid == True:
            # If there's already a file, 
            if path.exists('presets.json'):
                with open('presets.json', 'r') as f:
                    presets = json.load(f)
            else:
                presets = {}

            self.save_window = QtWidgets.QDialog()
            self.save_window.setWindowTitle("Save")
            self.save_window.resize(400, 250)

            self.dropdown_label = QtWidgets.QLabel(self.save_window)
            self.dropdown_label.setGeometry(QtCore.QRect(130, 60, 150, 25))
            self.dropdown_label.setText("Select which template to add to.")

            self.dropdown = QtWidgets.QComboBox(self.save_window)
            self.dropdown.setGeometry(QtCore.QRect(150, 100, 100, 25))
            for keys in presets:
                self.dropdown.addItem(keys)

            self.new_button = QtWidgets.QPushButton(self.save_window)
            self.new_button.setGeometry(QtCore.QRect(75, 175, 75, 25))
            self.new_button.setText("New")
            self.new_button.clicked.connect(self.new_preset)

            self.select_button = QtWidgets.QPushButton(self.save_window)
            self.select_button.setGeometry(QtCore.QRect(250, 175, 75, 25))
            self.select_button.setText("Select")
            self.select_button.clicked.connect(self.select_window)

            self.save_window.show()
        
    def new_preset(self):
        self.new_window = QtWidgets.QDialog()
        self.new_window.setWindowTitle("New")
        self.new_window.resize(250, 200)

        self.template_name_text = QtWidgets.QTextEdit(self.new_window)
        self.template_name_text.setGeometry(QtCore.QRect(75, 25, 100, 25))
        self.template_name_text.setPlaceholderText("Template Name")

        self.name_text = QtWidgets.QTextEdit(self.new_window)
        self.name_text.setGeometry(QtCore.QRect(75, 75, 100, 25))
        self.name_text.setPlaceholderText("Preset Name")

        self.add_button = QtWidgets.QPushButton(self.new_window)
        self.add_button.setGeometry(QtCore.QRect(75, 125, 100, 25))
        self.add_button.setText("Add")
        self.add_button.clicked.connect(self.add)

        self.save_window.close()
        self.new_window.show()

    def add(self):
        # If there's already a file, 
        if path.exists('templates.json'):
            with open('templates.json', 'r') as f:
                templates = json.load(f)
        else:
            templates = {}
        
        if path.exists('presets.json'):
            with open('presets.json', 'r') as f:
                presets = json.load(f)
        else:
            presets = {}

        # Get template name
        self.template_name_text.selectAll()
        template_name = self.template_name_text.textCursor().selectedText()

        if template_name in templates:
            self.error_window = QtWidgets.QDialog()
            self.error_window.setWindowTitle("Error")
            self.error_window.resize(300, 100)

            self.variable_label = QtWidgets.QLabel(self.error_window)
            self.variable_label.setGeometry(QtCore.QRect(90, 25, 120, 25))
            self.variable_label.setText("Template already exists!")

            self.close_error = QtWidgets.QPushButton(self.error_window)
            self.close_error.setGeometry(QtCore.QRect(125, 50, 50, 25))
            self.close_error.setText("Close")
            self.close_error.clicked.connect(self.close_error_window)

            self.error_window.show()
        else:
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

            # Get preset name
            self.name_text.selectAll()
            preset_name = self.name_text.textCursor().selectedText()

            # Add data to preset dictionary
            preset = (preset_name, var_text, text_variables)
            presets[template_name] = []
            presets[template_name].append(preset)

            # Add data to preset dictionary
            template = text
            templates[template_name] = template

            with open('presets.json', 'w') as f:
                json.dump(presets, f)

            with open('templates.json', 'w') as t:
                json.dump(templates, t)

            self.new_window.close()

    def select_window(self):
        self.sel_window = QtWidgets.QDialog()
        self.sel_window.setWindowTitle("Select")
        self.sel_window.resize(250, 150)

        self.sel_text = QtWidgets.QTextEdit(self.sel_window)
        self.sel_text.setGeometry(QtCore.QRect(75, 50, 100, 25))
        self.sel_text.setPlaceholderText("Preset Name")

        self.sel_button = QtWidgets.QPushButton(self.sel_window)
        self.sel_button.setGeometry(QtCore.QRect(75, 100, 100, 25))
        self.sel_button.setText("Add")
        self.sel_button.clicked.connect(self.select)

        self.save_window.close()
        self.sel_window.show()

    def select(self):
        # If there's already a file, 
        if path.exists('presets.json'):
            with open('presets.json', 'r') as f:
                templates = json.load(f)
        else:
            templates = {}

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

        # Get preset name
        self.sel_text.selectAll()
        name = self.sel_text.textCursor().selectedText()

        template_name = self.dropdown.currentText()

        # Add data to template dictionary and dropdown
        preset = (name, var_text, text_variables)
        if template_name not in templates:
            templates[template_name] = []
        templates[template_name].append(preset)

        with open('presets.json', 'w') as f:
            json.dump(templates, f)

        self.template_dropdown.addItem(name)

        self.sel_window.close()

    def copy(self):  
        valid = self.valid_template_check()
        if valid == True:
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

            for word in range(0, text_variables):
                text = text.replace(space, variables[word], 1)

            self.result = QtWidgets.QTextEdit(self.create_window)
            self.result.setGeometry(QtCore.QRect(-5000, 50, 500, 300))
            self.result.setText(text)
            self.result.selectAll()
            self.result.copy()

    def valid_template_check(self):
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
            return False
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
            return False
        else:
            return True

    def close_error_window(self):
        self.error_window.close()

    ### Load Commands ###
    def openLoadWindow(self):        
        # If there's already a file, 
        if path.exists('templates.json'):
            with open('templates.json', 'r') as f:
                templates = json.load(f)

        self.load_window = QtWidgets.QDialog()
        self.load_window.setWindowTitle("Load")
        self.load_window.resize(400, 250)

        self.load_label = QtWidgets.QLabel(self.load_window)
        self.load_label.setGeometry(QtCore.QRect(140, 60, 150, 25))
        self.load_label.setText("Select which template to use.")

        self.dropdown = QtWidgets.QComboBox(self.load_window)
        self.dropdown.setGeometry(QtCore.QRect(150, 100, 100, 25))
        for keys in templates:
            self.dropdown.addItem(keys)

        self.load_button = QtWidgets.QPushButton(self.load_window)
        self.load_button.setGeometry(QtCore.QRect(175, 175, 50, 25))
        self.load_button.setText("Load")
        self.load_button.clicked.connect(self.load)

        self.load_window.show()

    def load(self):
        # If there's already a file, 
        if path.exists('templates.json'):
            global tname
            with open('templates.json', 'r') as f:
                templates = json.load(f)
                
            
            tname = self.dropdown.currentText()
            self.openCreateWindow(tname)

            # Set variables
            self.template_text.setText(templates[tname])

            self.load_window.close()
            self.create_window.show()

        else:
            self.error_window = QtWidgets.QDialog()
            self.error_window.setWindowTitle("Error")
            self.error_window.resize(300, 100)

            self.variable_label = QtWidgets.QLabel(self.error_window)
            self.variable_label.setGeometry(QtCore.QRect(90, 25, 120, 25))
            self.variable_label.setText("No templates exist yet!")

            self.close_error = QtWidgets.QPushButton(self.error_window)
            self.close_error.setGeometry(QtCore.QRect(125, 50, 50, 25))
            self.close_error.setText("Close")
            self.close_error.clicked.connect(self.close_error_window)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
