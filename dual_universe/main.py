import csv
import sys
import threading

from PyQt6 import QtCore, QtGui, QtWidgets
from sqlmodel import Session, select

from dual_universe.config.db_setup import engine
from dual_universe.src.MDU import EngineLoop
from dual_universe.src.models import Character


class EngineThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._running = threading.Event()
        self._running.set()  # Set the event to true initially

    def run(self):
        engine_loop = EngineLoop()
        engine_loop.engine()
        print("Engine running...")

    def stop(self):
        self._running.clear()


class Ui_Dialog(object):
    def __init__(self):
        self.start_engine = EngineThread()
        self.verticalLayout = None
        self.verticalLayoutWidget = None
        self.deselectAll_btn = None
        self.selectAll_btn = None
        self.fileupload_btn = None
        self.password_lable = None
        self.email_lable = None
        self.username_lable = None
        self.textEdit_3 = None
        self.textEdit_2 = None
        self.textEdit = None
        self.tableView = None
        self.save_Button = None
        self.start_Button = None
        self.stop_Button = None
        self.selected_usernames = set()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 800)
        self.tableView = QtWidgets.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(10, 10, 361, 661))
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
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

        self.username_lable = QtWidgets.QLabel(Dialog)
        self.username_lable.setGeometry(QtCore.QRect(400, 20, 61, 75))
        self.username_lable.setObjectName("username_lable")
        # self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

        self.email_lable = QtWidgets.QLabel(Dialog)
        self.email_lable.setGeometry(QtCore.QRect(400, 60, 49, 75))
        self.email_lable.setObjectName("email_lable")

        self.password_lable = QtWidgets.QLabel(Dialog)
        self.password_lable.setGeometry(QtCore.QRect(400, 110, 49, 75))
        self.password_lable.setObjectName("password_lable")

        self.fileupload_btn = QtWidgets.QPushButton(Dialog)
        self.fileupload_btn.setGeometry(QtCore.QRect(410, 650, 75, 24))
        self.fileupload_btn.setObjectName("fileupload_btn")
        self.fileupload_btn.clicked.connect(
            self.upload_file
        )  # Connect upload button to function

        self.selectAll_btn = QtWidgets.QPushButton(Dialog)
        self.selectAll_btn.setGeometry(QtCore.QRect(690, 150, 75, 24))
        self.selectAll_btn.setObjectName("selectAll_btn")
        self.selectAll_btn.clicked.connect(
            self.select_all
        )  # Connect Select All button to function

        self.deselectAll_btn = QtWidgets.QPushButton(Dialog)
        self.deselectAll_btn.setGeometry(QtCore.QRect(520, 150, 75, 24))
        self.deselectAll_btn.setObjectName("deselectAll_btn")
        self.deselectAll_btn.clicked.connect(
            self.deselect_all
        )  # Connect Deselect All button to function

        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(400, 190, 160, 451))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.start_Button = QtWidgets.QPushButton(Dialog)
        self.start_Button.setGeometry(QtCore.QRect(500, 650, 75, 24))
        self.start_Button.setObjectName("start_Button")
        self.start_Button.clicked.connect(
            self.start_engine_thread
        )  # Connect Start Engine button to function

        self.stop_Button = QtWidgets.QPushButton(Dialog)
        self.stop_Button.setGeometry(QtCore.QRect(600, 650, 75, 24))
        self.stop_Button.setObjectName("stop_Button")
        self.stop_Button.clicked.connect(
            self.stop_engine
        )  # Connect Stop Engine button to function

        self.save_Button = QtWidgets.QPushButton(Dialog)
        self.save_Button.setGeometry(QtCore.QRect(700, 650, 75, 24))
        self.save_Button.setObjectName("save_Button")
        self.save_Button.clicked.connect(self.save_selection)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def start_engine_thread(self):
        self.engine_thread = EngineThread()
        self.engine_thread.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.username_lable.setText(_translate("Dialog", "Username*"))
        self.email_lable.setText(_translate("Dialog", "Email"))
        self.password_lable.setText(_translate("Dialog", "Password"))
        self.fileupload_btn.setText(_translate("Dialog", "File upload"))
        self.selectAll_btn.setText(_translate("Dialog", "Select All"))
        self.deselectAll_btn.setText(_translate("Dialog", "Deselect All"))
        self.save_Button.setText(_translate("Dialog", "Save"))
        self.start_Button.setText(_translate("Dialog", "Start Engine"))
        self.stop_Button.setText(_translate("Dialog", "Stop Engine"))

    def stop_engine(self):
        self.start_engine.stop()

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
    # TODO: Database initial setup
    # TODO: Initial File creation

    app = QtWidgets.QApplication([])
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.refresh_display()
    Dialog.show()
    sys.exit(app.exec())
