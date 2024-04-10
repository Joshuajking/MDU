from time import sleep

import keyboard
import pyautogui
import pydirectinput
from ahk import AHK

from src.config_manager import timing_decorator
from src.du_character import DUCharacters
from src.logging_config import logger
from src.models import ImageLocation, SearchAreaLocation
from src.querysets import CharacterQuerySet
from src.special_mission_ocr import OCREngine
from src.verify_screen import VerifyScreen


class CharacterLink:

	# self.ahk.send_raw(character.email)

	def __init__(self):
		self.ahk = AHK()
		self.ocr = OCREngine()
		self.verify = VerifyScreen()
		self.characters = DUCharacters()
		self.character = None
		self.remaining_currency = None

	def get_wallet_currency(self):
		# Ocr for the currency amount
		currency = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.WALLET_CURRENCY,
			scrap=True,
		)
		logger.debug(f"{self.character.username}: OCR'd - {currency}")

		base_amount = 100000.00
		currency = currency.replace(' ', '')  # Remove spaces
		if float(currency) > base_amount:
			converted_currency = float(currency) - base_amount
			self.remaining_currency = str(converted_currency)
			return True
		else:
			return False

	def get_recipient_searchEdit(self):
		# Find recipient search field & click in it
		response_image_to_compare = self.verify.screen(
			screen_name=ImageLocation.WALLET_SCREEN,
			image_to_compare='recipient_searchEdit.png',
			skip_sleep=True,
			mouse_click=True,
		)

		# Type Organization/Person name
		self.ahk.send_raw('cyt transportation')
		# keyboard.press('space')
		# self.ahk.send_raw('transportation')
		# Give time for name to populate
		sleep(3)
		# select name from drop down
		findName = 'CYT Transportation'
		findName_of = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.WALLET_RECIPIENT_LIST,
			search_text=findName,
			scroll=True,
			click=True
		)

	def get_recipient_searchArea(self):
		# Verify name is correct
		verify_findName = 'CYT Transportation'
		verify_findName_of = self.ocr.ocr_missions(
			search_area=SearchAreaLocation.RECIPIENT_SEARCH_AREA,
			search_text=verify_findName,
		)
		logger.debug(f"Transferring {self.remaining_currency} to {verify_findName_of}")

	def get_amount(self):
		# Enter amount to send/recieve
		image_list = ['amountEdit']
		var = self.verify.screen(
			screen_name=ImageLocation.WALLET_SCREEN,
			image_to_compare='amountEdit',
			skip_sleep=True,
			mouse_click=True,
		)
		pyautogui.click(clicks=3, interval=0.1)
		sleep(1)
		keyboard.press('backspace')
		sleep(1)

		self.ahk.send_raw(self.remaining_currency)
		logger.debug(f"{self.character.username}: Deposited - {self.remaining_currency}")

	def complete_transfer(self):
		# Complete Transfer
		var = self.verify.screen(
			screen_name=ImageLocation.WALLET_SCREEN,
			image_to_compare='selected_transfer_btn',
			skip_sleep=True,
			mouse_click=True,
		)
		# Complete Transfer
		var = self.verify.screen(
			screen_name=ImageLocation.WALLET_SCREEN,
			image_to_compare='transfer_currency_btn',
			skip_sleep=True,
			mouse_click=True,
		)

	@timing_decorator
	def character_link(self):
		delay = 10
		all_active_characters = CharacterQuerySet.get_active_characters()  # Get the characters dictionary
		# loop over all the accounts
		for character in all_active_characters:
			self.character = character
			# var = pyautogui.locateOnScreen(
			# 	image=r'..\data\du_images\login_screen\du_login_screen_label.png',
			# 	minSearchTime=3,
			# 	confidence=0.8
			# )
			has_gametime = self.characters.login(self.character)
			if not has_gametime:
				continue
			for i in range(delay):
				sleep(1)
				logger.info(f"Waiting for {i}/{delay}")
		# Open wallet screen
		# pydirectinput.press('o')
		# sleep(3)
		# result = self.get_wallet_currency()
		# if result:
		# 	self.get_recipient_searchEdit()
		# 	self.get_recipient_searchArea()
		# 	self.get_amount()
		# 	self.complete_transfer()

		self.characters.logout()

	def set_link(self):
		screen_width, screen_height = pyautogui.size()
		screen_x = screen_width / 2
		screen_y = screen_height / 2
		var = None
		while var is None:
			var = pyautogui.locateOnScreen(
				image=r"C:\Users\joshu\Pictures\Screenshots\Screenshot 2024-04-07 204607.png",
				minSearchTime=3,
				confidence=0.7,
			)
			if var is None:
				screen_y -= screen_y * -0.25
				pydirectinput.moveTo(round(screen_x), round(screen_y), duration=3)
			else:
				sleep(2)
				pydirectinput.moveTo(var, duration=3)
				sleep(2)
				pydirectinput.rightClick(var)


if __name__ == "__main__":
	obj = CharacterLink()
	obj.character_link()
