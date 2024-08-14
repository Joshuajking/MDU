import csv
import sys
import threading

from PyQt6 import QtCore, QtGui, QtWidgets
from sqlmodel import Session, select

from config.db_setup import engine
from models.models import Character


class EngineThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Your code with Engine() here
        pass


class Ui_Dialog(object):
    def __init__(self):
        self.verticalLayout = None
        self.verticalLayoutWidget = None
        self.pushButton_3 = None
        self.pushButton_2 = None
        self.pushButton = None
        self.label_3 = None
        self.label_2 = None
        self.label = None
        self.textEdit_3 = None
        self.textEdit_2 = None
        self.textEdit = None
        self.tableView = None
        self.saveButton = None
        self.selected_usernames = set()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 700)
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 361, 661))
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.Stretch
        )

        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(510, 20, 261, 21))
        self.textEdit.setObjectName("textEdit")

        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(510, 60, 261, 21))
        self.textEdit_2.setObjectName("textEdit_2")

        self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_3.setGeometry(QtCore.QRect(510, 110, 261, 21))
        self.textEdit_3.setObjectName("textEdit_3")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(400, 20, 61, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(400, 60, 49, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(400, 110, 49, 16))
        self.label_3.setObjectName("label_3")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(410, 650, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(
            self.upload_file
        )  # Connect upload button to function

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(690, 150, 75, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(
            self.select_all
        )  # Connect Select All button to function

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 150, 75, 24))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(
            self.deselect_all
        )  # Connect Deselect All button to function

        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(400, 190, 160, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.saveButton = QtWidgets.QPushButton(Dialog)
        self.saveButton.setGeometry(QtCore.QRect(600, 650, 75, 24))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_selection)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username*"))
        self.label_2.setText(_translate("Dialog", "Email"))
        self.label_3.setText(_translate("Dialog", "Password"))
        self.pushButton.setText(_translate("Dialog", "File upload"))
        self.pushButton_2.setText(_translate("Dialog", "Select All"))
        self.pushButton_3.setText(_translate("Dialog", "Deselect All"))
        self.saveButton.setText(_translate("Dialog", "Save"))

    def upload_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None,
            "Open File",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;JSON Files (*.json)",
        )
        allowed_headers = ["username", "email", "password"]

        # Fetch existing characters from the database
        with Session(engine) as session:
            characters_from_db = session.exec(select(Character)).all()
            existing_usernames = {
                character.username.lower() for character in characters_from_db
            }

        # Process the file if a file is selected
        if file_path:
            new_characters = []
            with open(file_path, "r") as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    if all(header in row for header in allowed_headers):
                        username = row["username"].strip().lower()  # Normalize username
                        if username:
                            character_data = {
                                "username": username,
                                "email": row["email"],
                                "password": row["password"],
                            }
                            new_characters.append(character_data)

            # Update existing characters and add new characters to the database
            with Session(engine) as session:
                for character_data in new_characters:
                    username = character_data[
                        "username"
                    ]  # Convert to lowercase for case-insensitive check
                    if username in existing_usernames:
                        # Update existing character
                        existing_character = session.exec(
                            select(Character).filter(Character.username.ilike(username))
                        ).one()
                        existing_character.email = character_data["email"]
                        existing_character.password = character_data["password"]
                        existing_character.active = username in self.selected_usernames
                    else:
                        # Add new character
                        new_character = Character(
                            username=username,
                            email=character_data["email"],
                            password=character_data["password"],
                            active=username in self.selected_usernames,
                        )
                        session.add(new_character)

                # Commit the changes to the database
                session.commit()

        # Refresh the display of characters
        self.refresh_display()
        self.save_selection()

    def save_selection(self):
        # Update the active status of characters in the database based on selected usernames
        with Session(engine) as session:
            model = self.tableView.model()
            for row in range(model.rowCount()):
                username_item = model.item(row, 1)
                username = username_item.text()
                active = model.item(row, 0).checkState() == QtCore.Qt.CheckState.Checked
                character = session.exec(
                    select(Character).filter(Character.username.ilike(username))
                ).one()
                character.active = active
            session.commit()

    def refresh_display(self):
        # Fetch characters from the database and update the table view
        with Session(engine) as session:
            characters_from_db = session.exec(select(Character)).all()

        nested_dict = {"characters": {}}
        for character in characters_from_db:
            username = character.username.capitalize()
            email = character.email.lower()
            password = character.password
            has_package = character.has_package
            has_gametime = character.has_gametime
            active = (
                character.active
            )  # Assuming you have an 'active' attribute in your Character models
            character_info = {
                "email": email,
                "password": password,
                "has_package": has_package,
                "has_gametime": has_gametime,
                "active": active,
            }
            nested_dict["characters"][username] = character_info

        model = QtGui.QStandardItemModel()
        model.setColumnCount(5)
        model.setHorizontalHeaderLabels(
            [
                "Select",
                "Username",
                "Email",
                "Password",
                "Package",
                "Game Time",
                "Active",
            ]
        )

        for row, (username, character_info) in enumerate(
            nested_dict["characters"].items()
        ):
            check_box = QtWidgets.QCheckBox()
            item = QtGui.QStandardItem()
            item.setCheckable(True)
            item.setCheckState(
                QtCore.Qt.CheckState.Checked
                if character_info["active"]
                else QtCore.Qt.CheckState.Unchecked
            )
            model.setItem(row, 0, item)
            self.tableView.setIndexWidget(model.index(row, 0), check_box)

            model.setItem(row, 1, QtGui.QStandardItem(username))
            model.setItem(row, 2, QtGui.QStandardItem(character_info["email"]))
            model.setItem(row, 3, QtGui.QStandardItem(character_info["password"]))
            model.setItem(row, 4, QtGui.QStandardItem(character_info["has_package"]))
            model.setItem(row, 5, QtGui.QStandardItem(character_info["has_gametime"]))
            model.setItem(
                row,
                6,
                QtGui.QStandardItem(
                    "Active" if character_info["active"] else "Inactive"
                ),
            )

        self.tableView.setModel(model)
        self.tableView.resizeColumnsToContents()

    def select_all(self):
        model = self.tableView.model()
        for row in range(model.rowCount()):
            item = model.item(row, 0)
            item.setCheckState(QtCore.Qt.CheckState.Checked)
        self.update_selected_usernames()

    def deselect_all(self):
        model = self.tableView.model()
        for row in range(model.rowCount()):
            item = model.item(row, 0)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.update_selected_usernames()

    def update_selected_usernames(self):
        model = self.tableView.model()
        self.selected_usernames = set()
        for row in range(model.rowCount()):
            item = model.item(row, 0)
            if item.checkState() == QtCore.Qt.CheckState.Checked:
                username_item = model.item(row, 1)
                username = username_item.text()
                self.selected_usernames.add(username)


if __name__ == "__main__":
    engine_thread = EngineThread()
    engine_thread.start()

    app = QtWidgets.QApplication([])
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.refresh_display()
    Dialog.show()
    sys.exit(app.exec())
