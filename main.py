import csv
import os
import sys
import threading
from time import perf_counter, sleep

from PyQt6 import QtCore, QtGui, QtWidgets
from sqlmodel import Session, select

from settings import engine
from src.config_manager import ConfigManager
from src.du_character import DUCharacters
from src.du_client_manager import DUClientManager
from src.du_flight import DUFlight
from src.du_missions import DUMissions
from src.logging_config import logger
from src.models import Character
from src.querysets import CharacterQuerySet
from src.video_recording import get_last_30_seconds


class EngineThread(threading.Thread):
	def __init__(self):
		super().__init__()
		self.client = DUClientManager()
		self._running = threading.Event()
		self._running.set()  # Set the event to true initially
		self.retrieve_mode = True

	def active_package_count(self):
		package_count = CharacterQuerySet.count_has_package_and_active_characters()
		logger.info(f"package_count: {package_count}")
		active_character_count = CharacterQuerySet.count_active_characters()

		if active_character_count > 0:
			percentage = (package_count / active_character_count) * 100
			logger.info(f"percentage of package taken: {percentage}")
			if percentage >= 75:
				self.retrieve_mode = False
			else:
				self.retrieve_mode = True

	def run(self):

		client_limit = 21600
		client_run = 0
		start_time = perf_counter()
		while self._running.is_set():
			logger.info(f"is running {self._running}")
			client_start = perf_counter()
			try:
				self.client.start_application()
				du_characters = DUCharacters()
				flight = DUFlight()
				missions = DUMissions()
				config_manager = ConfigManager()
				all_active_characters = CharacterQuerySet.get_active_characters()
				active_character_count = CharacterQuerySet.count_active_characters()
				for character in all_active_characters:
					if not self._running.is_set():
						break
					has_gametime = du_characters.login(character)
					if not has_gametime:
						continue
					status = missions.process_package(character)
					logger.info(f"{character.username} package status: {status}")
					CharacterQuerySet.update_character(character, {'has_package': status["has_package"]})
					du_characters.logout()
					logger.info(f"retrieve_mode: {self.retrieve_mode}")

				self.active_package_count()
				logger.info(f"retrieve_mode: {self.retrieve_mode}")

				pilot = CharacterQuerySet.read_character_by_username(config_manager.get_value('config.pilot'))
				logger.info(f"Logging into Pilot: {pilot.username}")
				du_characters.login(pilot)
				flight.mission_flight(self.retrieve_mode)

			except Exception as e:
				get_last_30_seconds()
				sleep(10)
				logger.error(f"Exception: {str(e)}")
				# self.client.stop_application()
				client_stop = perf_counter()
				client_runtime = client_stop - client_start
				client_run += client_runtime
				logger.info(f"Client runtime: {client_run}")
				sleep(20)
				continue

			else:
				client_stop = perf_counter()
				client_runtime = client_stop - client_start
				client_run += client_runtime
				logger.info(f"Client runtime: {client_run}")
				elapsed_time = perf_counter() - start_time
				if elapsed_time >= 6 * 60 * 60:  # 6 hours in seconds
					self.client.stop_application()
					break
			logger.info("Restarting after 6 hours...")
			continue


	def stop(self):
		self._running.clear()
		logger.warning(f"Stopping {self}")


class Ui_Dialog(object):
	def __init__(self):
		self.start_engine = EngineThread()
		self.delete_character_btn = None
		self.add_character_btn = None
		self.engine_thread = None
		self.verticalLayout = None
		self.verticalLayoutWidget = None
		self.deselectAll_btn = None
		self.selectAll_btn = None
		self.fileupload_btn = None
		self.password_lable = None
		self.email_lable = None
		self.username_lable = None
		self.passwordtextEdit = None
		self.emailtextEdit = None
		self.usernametextEdit = None
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
		self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
		##############
		self.usernametextEdit = QtWidgets.QTextEdit(Dialog)
		self.usernametextEdit.setGeometry(QtCore.QRect(510, 20, 261, 21))
		self.usernametextEdit.setObjectName("usernametextEdit")

		self.username_lable = QtWidgets.QLabel(Dialog)
		self.username_lable.setGeometry(QtCore.QRect(400, 20, 101, 21))  # Adjusted height to match text edit
		self.username_lable.setObjectName("username_lable")
		##############
		self.emailtextEdit = QtWidgets.QTextEdit(Dialog)
		self.emailtextEdit.setGeometry(QtCore.QRect(510, 60, 261, 21))
		self.emailtextEdit.setObjectName("emailtextEdit")

		self.email_lable = QtWidgets.QLabel(Dialog)
		self.email_lable.setGeometry(QtCore.QRect(400, 60, 101, 21))  # Adjusted height to match text edit
		self.email_lable.setObjectName("email_lable")
		##############
		self.passwordtextEdit = QtWidgets.QTextEdit(Dialog)
		self.passwordtextEdit.setGeometry(QtCore.QRect(510, 110, 261, 21))
		self.passwordtextEdit.setObjectName("passwordtextEdit")

		self.password_lable = QtWidgets.QLabel(Dialog)
		self.password_lable.setGeometry(QtCore.QRect(400, 110, 101, 21))  # Adjusted height to match text edit
		self.password_lable.setObjectName("password_lable")
		##############

		self.fileupload_btn = QtWidgets.QPushButton(Dialog)
		self.fileupload_btn.setGeometry(QtCore.QRect(410, 650, 75, 24))
		self.fileupload_btn.setObjectName("fileupload_btn")
		self.fileupload_btn.clicked.connect(self.upload_file)  # Connect upload button to function

		self.selectAll_btn = QtWidgets.QPushButton(Dialog)
		self.selectAll_btn.setGeometry(QtCore.QRect(690, 150, 75, 24))
		self.selectAll_btn.setObjectName("selectAll_btn")
		self.selectAll_btn.clicked.connect(self.select_all)  # Connect Select All button to function

		self.add_character_btn = QtWidgets.QPushButton(Dialog)
		self.add_character_btn.setGeometry(QtCore.QRect(600, 200, 75, 24))
		self.add_character_btn.setObjectName("add_character_btn")
		self.add_character_btn.clicked.connect(self.add_character)

		self.delete_character_btn = QtWidgets.QPushButton(Dialog)
		self.delete_character_btn.setGeometry(QtCore.QRect(600, 150, 75, 24))
		self.delete_character_btn.setObjectName("delete_character_btn")
		self.delete_character_btn.clicked.connect(self.delete_character)

		self.deselectAll_btn = QtWidgets.QPushButton(Dialog)
		self.deselectAll_btn.setGeometry(QtCore.QRect(520, 150, 75, 24))
		self.deselectAll_btn.setObjectName("deselectAll_btn")
		self.deselectAll_btn.clicked.connect(self.deselect_all)  # Connect Deselect All button to function

		self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
		self.verticalLayoutWidget.setGeometry(QtCore.QRect(400, 190, 160, 451))
		self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

		self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
		self.verticalLayout.setContentsMargins(0, 0, 0, 0)
		self.verticalLayout.setObjectName("verticalLayout")

		self.start_Button = QtWidgets.QPushButton(Dialog)
		self.start_Button.setGeometry(QtCore.QRect(500, 650, 75, 24))
		self.start_Button.setObjectName("start_Button")
		self.start_Button.clicked.connect(self.start_engine_thread)  # Connect Start Engine button to function

		self.stop_Button = QtWidgets.QPushButton(Dialog)
		self.stop_Button.setGeometry(QtCore.QRect(600, 650, 75, 24))
		self.stop_Button.setObjectName("stop_Button")
		self.stop_Button.clicked.connect(self.stop_engine)  # Connect Stop Engine button to function

		self.save_Button = QtWidgets.QPushButton(Dialog)
		self.save_Button.setGeometry(QtCore.QRect(700, 650, 75, 24))
		self.save_Button.setObjectName("save_Button")
		self.save_Button.clicked.connect(self.save_selection)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def start_engine_thread(self):
		self.engine_thread = EngineThread()
		logger.info(f"start engine initiated")
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
		self.add_character_btn.setText(_translate("Dialog", "Add/Update"))
		self.delete_character_btn.setText(_translate("Dialog", "Delete"))

	def stop_engine(self):
		self.start_engine.stop()
		logger.info(f"stop engine initiated")

	def upload_file(self):
		file_dialog = QtWidgets.QFileDialog()
		file_path, _ = file_dialog.getOpenFileName(None, 'Open File', '',
		                                           'CSV Files (*.csv);;Text Files (*.txt);;JSON Files (*.json)')
		allowed_headers = ['username', 'email', 'password']

		# Fetch existing characters from the database
		with Session(engine) as session:
			characters_from_db = session.exec(select(Character)).all()
			existing_usernames = {character.username.lower() for character in characters_from_db}

		# Process the file if a file is selected
		if file_path:
			new_characters = []
			with open(file_path, 'r') as file:
				csv_reader = csv.DictReader(file)
				for row in csv_reader:
					if all(header in row for header in allowed_headers):
						username = row["username"].strip().lower()  # Normalize username
						if username:
							character_data = {
								"username": username,
								"email": row["email"],
								"password": row["password"]
							}
							new_characters.append(character_data)

			# Update existing characters and add new characters to the database
			with Session(engine) as session:
				for character_data in new_characters:
					username = character_data["username"]  # Convert to lowercase for case-insensitive check
					if username in existing_usernames:
						# Update existing character
						existing_character = session.exec(
							select(Character).filter(Character.username.ilike(username))).one()
						existing_character.email = character_data["email"]
						existing_character.password = character_data["password"]
						existing_character.active = username in self.selected_usernames
					else:
						# Add new character
						new_character = Character(username=username, email=character_data["email"],
						                          password=character_data["password"],
						                          active=username in self.selected_usernames)
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
				character = session.exec(select(Character).filter(Character.username.ilike(username))).one()
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
			active = character.active  # Assuming you have an 'active' attribute in your Character model
			character_info = {
				"email": email,
				"password": password,
				"has_package": has_package,
				"has_gametime": has_gametime,
				"active": active
			}
			nested_dict["characters"][username] = character_info

		model = QtGui.QStandardItemModel()
		model.setColumnCount(5)
		model.setHorizontalHeaderLabels(["Select", "Username", "Email", "Password", "Package", "Game Time", "Active"])

		for row, (username, character_info) in enumerate(nested_dict["characters"].items()):
			check_box = QtWidgets.QCheckBox()
			item = QtGui.QStandardItem()
			item.setCheckable(True)
			item.setCheckState(
				QtCore.Qt.CheckState.Checked if character_info["active"] else QtCore.Qt.CheckState.Unchecked)
			model.setItem(row, 0, item)
			self.tableView.setIndexWidget(model.index(row, 0), check_box)

			model.setItem(row, 1, QtGui.QStandardItem(username))
			model.setItem(row, 2, QtGui.QStandardItem(character_info["email"]))
			model.setItem(row, 3, QtGui.QStandardItem(character_info["password"]))
			model.setItem(row, 4, QtGui.QStandardItem(character_info["has_package"]))
			model.setItem(row, 5, QtGui.QStandardItem(character_info["has_gametime"]))
			model.setItem(row, 6, QtGui.QStandardItem("Active" if character_info["active"] else "Inactive"))

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

	def add_character(self):
		username = self.usernametextEdit.toPlainText().strip().capitalize()
		email = self.emailtextEdit.toPlainText().strip()
		password = self.passwordtextEdit.toPlainText().strip()

		try:
			with Session(engine) as session:
				# Check if the user already exists in the database
				character = session.query(Character).filter_by(username=username).first()
				if character:
					# Update the existing user's email and password
					Character.username = username
					character.email = email
					character.password = password
					logger.info(f"Updated user: {character}")
					session.commit()
				else:
					# Create a new user
					new_character = Character(username=username, email=email, password=password)
					session.add(new_character)
					logger.info(f"Created new character: {new_character}")
					session.commit()
		except Exception as e:
			logger.error(f"{str(e)}")
		# Refresh the display of characters
		self.refresh_display()
		self.save_selection()

	def delete_character(self):
		username = self.usernametextEdit.toPlainText().strip()
		try:
			with Session(engine) as session:
				character = session.query(Character).filter_by(username=username).first()
				if character:
					session.delete(character)
					session.commit()
					print(f'Character deleted: {character}')
				else:
					print("Character not found")
		except Exception as e:
			logger.error(f"{str(e)}")
		# Refresh the display of characters
		self.refresh_display()
		self.save_selection()


def delete_large_files(directory, max_size_mb):
	max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
	for filename in os.listdir(directory):
		filepath = os.path.join(directory, filename)
		if os.path.isfile(filepath) and os.path.getsize(filepath) > max_size_bytes:
			# os.remove(filepath)
			print(f"Deleted: {filepath}")


if __name__ == "__main__":
	# Database initial setup
	# pre_load = DbConfig()
	# pre_load.load_image_entries_to_db()
	# TODO: Initial File creation

	# TODO: delete over-size-limit dir
	# Example usage
	# directory_path = ["/utils"]
	# max_file_size_mb = 500  # Specify the maximum file size in megabytes
	# delete_large_files(directory_path, max_file_size_mb)

	app = QtWidgets.QApplication([])
	Dialog = QtWidgets.QDialog()
	ui = Ui_Dialog()
	ui.setupUi(Dialog)
	ui.refresh_display()
	Dialog.show()
	sys.exit(app.exec())
