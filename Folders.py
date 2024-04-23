import json
import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtGui import QIcon


class Data:
    # Very basic functionality!!
    # Currently without demanding the right input.
    # Without handling the case when card and category have the same name. And other things
    """
    Everything that relates to managing data. Stores in json.
    Create/delete/rename/copy/cut Folders and Categories.
    Create/delete/copy/change Cards.
    Create a pool. Get random card.
    """

    def __init__(self, filename):
        # Start position. We always start from Main folder.
        # Navigation system. Keeping info about current object. Path.

        self.pool = {} # All cards
        self.categories_in_pool = [] # (forUI) Categories to show in first window(main_menu)


        self.filename = filename
        self.data = self.load_data()
        self.main_menu = self.data['Main']  # For button Main_Menu and what to show at the start

        self.current_object = {}
        self.current_path = ['Main']  # For back function
        self.update_content()

    def load_data(self):
        # Loading json. Creating if does not exist.
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            default_data = {'Main': {'name': 'Main Folder', 'type': 'folder', 'content': {}}}
            with open(self.filename, 'w') as file:
                json.dump(default_data, file)
            return default_data

    def save_data(self):
        # Save data
        with open(self.filename, 'w') as file:
            json.dump(self.data, file)

    def create_folder(self, name):
        # Create folder
        if name not in self.current_object['content'] and self.current_object['type'] == 'folder':
            self.current_object['content'][name] = {
                'name': name,
                'type': 'folder',
                'content': {}
            }
            self.update_content()  # Update current object info and content
            self.save_data()

    def create_category(self, name):
        # Create category. Difference between category and folder - can not create folder in category.
        # If card created in category it acquires category's name.
        self.current_object['content'][name] = {
            'name': self.current_object['name']+'_'+name,
            'type': 'category',
            'content': {}
        }
        self.update_content()  # Update window and content
        self.save_data()

    def create_card(self, name, chance, description):
        # Create card.
        # Set name, chance and description.
        # Chance. If we set 20 it means 20%, converted to 0.2
        self.current_object['content'][name] = {
            'name': name,
            'category': name if self.current_object['type'] == 'folder' else self.current_object['name'],
            'type': 'card',
            'chance': int(chance)/100,
            'description': description
        }
        self.update_content()  # Update window and content
        self.save_data()

    def open_object(self, name):
        # Open folder
        self.current_path.append('content')
        self.current_path.append(name)
        self.update_content()  # Update window and content

    def back(self):
        # Back or up in hierarchy
        if len(self.current_path) >= 2:
            self.current_path = self.current_path[:-2]
            self.update_content()

    def update_content(self):
        # Update info about current object
        current = self.data
        for step in self.current_path:
            current = current[step]
        self.current_object = current

    def delete_object(self, name):
        # Delete object
        if name in self.current_object['content']:
            del self.current_object['content'][name]
            self.save_data()

    def remove_all(self):
        # Clear the pool
        self.pool = []

    def add_to_pool(self, name):
        # Add object to pool.
        # If category added to pool, all the card in this category will be added to pool
        object_we_add = self.current_object['content']['name']
        if object_we_add['type'] == 'card':
            self.pool.append(object_we_add)
            self.categories_in_pool.append(object_we_add['name'])
        elif object_we_add['type'] =='category':
            self.pool.append(object_we_add['content'])
            self.categories_in_pool.append(object_we_add['name'])
        else:
            # Pull out and add all the categories and cards
            # Probably recursive function



class CreateDialog(QtWidgets.QDialog):
    # Creating small menu for name input and saving.
    def __init__(self, parent=None):
        super(CreateDialog, self).__init__(parent)
        self.setWindowTitle("Create")
        self.layout = QtWidgets.QVBoxLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.layout.addWidget(QtWidgets.QLabel("Name:"))
        self.layout.addWidget(self.name_edit)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)


class Create_Card_Dialog(QtWidgets.QDialog):
    # Creating small window for name, chance and description input for cards.
    # Gonna change it later so everything will be in a single window
    def __init__(self, parent=None):
        super(Create_Card_Dialog, self).__init__(parent)
        self.setWindowTitle("Create")
        self.layout = QtWidgets.QVBoxLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.layout.addWidget(QtWidgets.QLabel("Name:"))
        self.layout.addWidget(self.name_edit)

        self.chance_edit = QtWidgets.QLineEdit()
        self.layout.addWidget(QtWidgets.QLabel("Chance:"))
        self.layout.addWidget(self.chance_edit)

        self.description_edit = QtWidgets.QTextEdit()
        self.layout.addWidget(QtWidgets.QLabel("Description:"))
        self.layout.addWidget(self.description_edit)

        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)


class Folders_UI(object):
    """
    GUI for managing folders.
    Right now very basic things. Only navigation, creating and deleting.
    """
    def __init__(self, data):
        self.data = data

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Folder")
        fixed_size = QtCore.QSize(550, 500)
        MainWindow.setFixedSize(fixed_size)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 50, 550, 450))
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 548, 448))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 531, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 551, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.BackBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.BackBtn.setObjectName("BackBtn")
        self.horizontalLayout.addWidget(self.BackBtn)
        self.MainMenuBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.MainMenuBtn.setObjectName("MainMenuBtn")
        self.horizontalLayout.addWidget(self.MainMenuBtn)
        self.CreateFolderBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.CreateFolderBtn.setObjectName("CreateFolderBtn")
        self.horizontalLayout.addWidget(self.CreateFolderBtn)
        self.CreateCategoryBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.CreateCategoryBtn.setObjectName("CreateCategoryBtn")
        self.horizontalLayout.addWidget(self.CreateCategoryBtn)
        self.CreateCardBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.CreateCardBtn.setObjectName("CreateCardBtn")
        self.horizontalLayout.addWidget(self.CreateCardBtn)
        self.RandomBtn = QtWidgets.QPushButton(self.layoutWidget)
        self.RandomBtn.setObjectName("RandomBtn")
        self.horizontalLayout.addWidget(self.RandomBtn)

        self.actionFolder = QtWidgets.QAction(MainWindow)
        self.actionFolder.setObjectName("actionFolder")
        self.actionCategory = QtWidgets.QAction(MainWindow)
        self.actionCategory.setObjectName("actionCategory")
        self.actionCard = QtWidgets.QAction(MainWindow)
        self.actionCard.setObjectName("actionCard")

        self.BackBtn.clicked.connect(self.back)
        # self.MainMenuBtn.clicked.connect(self.go_to_main_menu)
        self.CreateFolderBtn.clicked.connect(self.create_folder_dialog)
        self.CreateCategoryBtn.clicked.connect(self.create_category_dialog)
        self.CreateCardBtn.clicked.connect(self.create_card_dialog)
        # self.RandomBtn.clicked.connect(self.random_function)
        self.scrollArea.setWidgetResizable(False)  # Disable automatic resizing of content
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.populate_folders()  # Call method to populate folder buttons

        # Create the context menu
        self.contextMenu = QMenu()
        self.deleteAction = QAction("Delete", self.contextMenu)
        self.deleteAction.triggered.connect(self.delete_selected_item)
        self.contextMenu.addAction(self.deleteAction)

        # Connect the right-click event to the context menu
        self.scrollAreaWidgetContents.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.scrollAreaWidgetContents.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Get the widget under the cursor
        widget = self.scrollAreaWidgetContents.childAt(position)

        if widget is not None:
            # Store the name of the item for later use
            self.right_clicked_item_name = widget.objectName()

            # Show the context menu at the cursor position
            self.contextMenu.popup(QtGui.QCursor.pos())

    def delete_selected_item(self):
        # Delete the item that was right-clicked
        if hasattr(self, 'right_clicked_item_name'):
            self.data.delete_object(self.right_clicked_item_name)
            self.clear_layout()
            self.populate_folders()


    def populate_folders(self):
        # Method to populate folder buttons in the UI
        folder_content = self.data.current_object['content']
        row = 0
        column = 0
        for index, (name, items) in enumerate(folder_content.items()):
            if items['type'] == 'folder':
                row = index // 4
                column = index % 4
                folder_button = QtWidgets.QPushButton(name)
                folder_button.setObjectName(name)
                folder_button.clicked.connect(lambda _, name=name: self.open_folder(name))
                folder_button.setIcon(QIcon('Folder.png'))
                self.gridLayout.addWidget(folder_button, row, column)
            elif items['type'] == 'category':
                row = index // 4
                column = index % 4
                folder_button = QtWidgets.QPushButton(name)
                folder_button.setObjectName(name)
                folder_button.clicked.connect(lambda _, name=name: self.open_folder(name))
                folder_button.setIcon(QIcon('Category.png'))
                self.gridLayout.addWidget(folder_button, row, column)
            else:
                row = index // 4
                column = index % 4
                card_button = QtWidgets.QPushButton(name)
                card_button.setObjectName(name)
                card_button.setIcon(QIcon('Card.png'))
                self.gridLayout.addWidget(card_button, row, column)


    def clear_layout(self):
        # Method to clear current layout (remove all buttons)
        for i in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)



    def open_folder(self, name):
        self.data.open_object(name)
        self.clear_layout()
        self.populate_folders()

    def back(self):
        self.data.back()
        self.clear_layout()
        self.populate_folders()


    def create_folder_dialog(self):
        # Method to show the create folder dialog
        dialog = CreateDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:  # Show the dialog as modal
            folder_name = dialog.name_edit.text()
            if folder_name:  # Ensure a folder name is provided
                self.data.create_folder(folder_name)
                self.clear_layout()
                self.populate_folders()

    def create_category_dialog(self):
        # Method to show the create category dialog
        dialog = CreateDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            category_name = dialog.name_edit.text()
            if category_name:
                self.data.create_category(category_name)
                self.clear_layout()
                self.populate_folders()

    def create_card_dialog(self):
        # Method to show the create card dialog
        dialog = Create_Card_Dialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:  # Show the dialog as modal
            card_name = dialog.name_edit.text()
            chance = dialog.chance_edit.text()
            description = dialog.description_edit.toPlainText()
            if card_name and chance and description:
                self.data.create_card(name=card_name, chance=chance, description=description)
                self.clear_layout()
                self.populate_folders()






    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data"))
        self.BackBtn.setText(_translate("MainWindow", "Back"))
        self.MainMenuBtn.setText(_translate("MainWindow", "Main_menu"))
        self.CreateFolderBtn.setText(_translate("MainWindow", "Create Folder"))
        self.CreateCategoryBtn.setText(_translate("MainWindow", "Create Category"))
        self.CreateCardBtn.setText(_translate("MainWindow", "Create Card"))
        self.RandomBtn.setText(_translate("MainWindow", "Random"))
        self.actionFolder.setText(_translate("MainWindow", "Folder"))
        self.actionCategory.setText(_translate("MainWindow", "Category"))
        self.actionCard.setText(_translate("MainWindow", "Card"))




class MainWindow(object):
    def __init__(self, data):
        self.data = data


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        fixed_size = QtCore.QSize(550, 500)
        MainWindow.setFixedSize(fixed_size)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        MainWindow.setCentralWidget(self.centralwidget)
        self.setupButtons()
        self.setupScrollAreas()
        self.setup_grid_layouts()

        self.retranslateUi(MainWindow)

    def setupButtons(self):
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, 69, 551, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_4 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.Random = QtWidgets.QPushButton(self.centralwidget)
        self.Random.setGeometry(QtCore.QRect(200, 20, 140, 30))
        self.Random.setObjectName("Random")

    def setupScrollAreas(self):
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(-10, 110, 561, 100))
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 559, 98))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        self.scrollArea_2 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_2.setGeometry(QtCore.QRect(0, 210, 550, 290))
        self.scrollArea_2.setWidgetResizable(False)
        self.scrollArea_2.setFixedHeight(290)
        self.scrollArea_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 545, 285))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)


    def setup_grid_layouts(self):
        self.gridLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 0, 530, 100))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget_2")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setObjectName("gridLayout_2")

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 530, 280))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout.setSpacing(30)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setObjectName("gridLayout")

        row = 0
        column = 0
        for i in range(90):
            row = i // 4
            column = i % 4
            test_button = QtWidgets.QPushButton(str(i))
            test_button.setObjectName(str(i))
            test_button.setMinimumSize(100, 100)
            test_button.setMaximumSize(80, 100)
            self.gridLayout_2.addWidget(test_button, row, column)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Random.setText(_translate("MainWindow", "Random"))
        self.pushButton_4.setText(_translate("MainWindow", "Add"))
        self.pushButton_3.setText(_translate("MainWindow", "RemoveAll"))
        self.pushButton_2.setText(_translate("MainWindow", "UnfrzAll"))
        self.pushButton_5.setText(_translate("MainWindow", "FrzAll"))
        self.pushButton.setText(_translate("MainWindow", "Folders"))



if __name__=='__main__':
    Main_app = QtWidgets.QApplication(sys.argv)

    data = Data('data.json')

    window = QtWidgets.QMainWindow()

    MainUI = MainWindow(data)
    MainUI.setupUi(window)

    window.show()
    sys.exit(Main_app.exec_())