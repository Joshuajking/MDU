from time import sleep

import keyboard
import pyautogui
import pydirectinput
from ahk import AHK

from core.DUCharacters import DUCharacters
from logs.logging_config import logger
from models.models import ImageLocation, SearchAreaLocation
from querysets.querysets import CharacterQuerySet
from utils.special_mission_ocr import OCREngine
from utils.verify_screen import VerifyScreen


class CharacterLink:
	ahk = AHK()
	# self.ahk.send_raw(character.email)

	def __init__(self):
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
			# return remaining_currency

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

	def character_link(self):
		all_active_characters = CharacterQuerySet.get_active_characters()  # Get the characters dictionary
		# loop over all the accounts
		for character in all_active_characters:
			self.character = character

			has_gametime = self.characters.login(character)

			if not has_gametime:
				continue
			sleep(15)
			# Open wallet screen
			pydirectinput.press('o')
			sleep(3)
			self.get_wallet_currency()
			self.get_recipient_searchEdit()
			self.get_recipient_searchArea()
			self.get_amount()
			self.complete_transfer()

		self.characters.logout()


if __name__ == "__main__":
	# name = 'CYT Transportation'
	#
	# RECIPIENT_SEARCH_AREA = OCREngine().ocr_missions(
	# 	search_area=SearchAreaLocation.RECIPIENT_SEARCH_AREA,
	# 	search_text=name,
	# 	# scroll=True,
	# 	# click=True
	# )
	obj = CharacterLink()
	obj.character_link()
