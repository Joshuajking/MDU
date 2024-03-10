# import logging
#
# import cv2
# import mss
# from numpy import array
# from pyautogui import size
#
# import json
#
# logger = logging.getLogger('debug_logger')
# info_logger = logging.getLogger('info_logger')
# """
# File:Screen.py
#
# Description:
#   Class to handle screen grabs
#
# Author: sumzer0@yahoo.com
# """
#
#
# # size() return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
# # TODO: consider update to handle ED running in a window
# #   find the ED Window
# #   win32gui.SetForegroundWindow(hwnd)
# #    bbox = win32gui.GetWindowRect(hwnd)     will also then give me the resolution of the image
# #     img = ImageGrab.grab(bbox)
#
# class Screen:
# 	def __init__(self):
# 		screen_width, screen_height = size()
#
# 		# Add new screen resolutions here with tested scale factors
# 		# this table will be default, overwriten when loading resolution.json file
# 		scales = {  # scaleX, scaleY
# 			'1024x768': [0.39, 0.39],  # tested, but not has high match %
# 			'1080x1080': [0.5, 0.5],  # fix, not tested
# 			'1280x800': [0.48, 0.48],  # tested
# 			'1280x1024': [0.5, 0.5],  # tested
# 			'1600x900': [0.6, 0.6],  # tested
# 			'1920x1080': [0.75, 0.75],  # tested
# 			'1920x1200': [0.73, 0.73],  # tested
# 			'1920x1440': [0.8, 0.8],  # tested
# 			'2560x1080': [0.75, 0.75],  # tested
# 			'2560x1440': [1.0, 1.0],  # tested
# 			'3440x1440': [1.0, 1.0],  # tested
# 			'Calibrated': [-1.0, -1.0]
# 		}
#
# 		mss = mss.mss()
#
# 		# used this to write the scales table to the json file
# 		# write_config(scales)
#
# 		ss = read_config()
#
# 		# if we read it then point to it, otherwise use the default table above
# 		if ss is not None:
# 			scales = ss
# 			logger.debug("read json:" + str(ss))
#
# 		# try to find the resolution/scale values in table
# 		# if not, then take current screen size and divide it out by 3440 x1440
# 		try:
# 			scale_key = str(screen_width) + "x" + str(screen_height)
# 			scaleX = scales[scale_key][0]
# 			scaleY = scales[scale_key][1]
# 		except:
# 			# if we don't have a definition for the resolution then use calculation
# 			scaleX = screen_width / 3440.0
# 			scaleY = screen_height / 1440.0
#
# 		# if the calibration scale values are not -1, then use those regardless of above
# 		if scales['Calibrated'][0] != -1.0:
# 			scaleX = scales['Calibrated'][0]
# 		if scales['Calibrated'][1] != -1.0:
# 			scaleY = scales['Calibrated'][1]
#
# 		logger.debug('screen size: ' + str(screen_width) + " " + str(screen_height))
# 		logger.debug('Scale X, Y: ' + str(scaleX) + ", " + str(scaleY))
#
# 	def write_config(, data, fileName='./config/resolution.json'):
# 		if data is None:
# 			data = scales
# 		try:
# 			with open(fileName, "w") as fp:
# 				json.dump(data, fp, indent=4)
# 		except Exception as e:
# 			logger.warning("Screen.py write_config error:" + str(e))
#
# 	def read_config(, fileName='./config/resolution.json'):
# 		s = None
# 		try:
# 			with open(fileName, "r") as fp:
# 				s = json.load(fp)
# 		except  Exception as e:
# 			logger.warning("Screen.py read_config error :" + str(e))
#
# 		return s
#
# 	# reg defines a box as a percentage of screen width and height
# 	def get_screen_region(, reg):
# 		image = array(mss.grab((int(reg[0]), int(reg[1]), int(reg[2]), int(reg[3]))))
# 		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# 		return image
#
# 	def get_screen(, x_left, y_top, x_right, y_bot):  # if absolute need to scale??
# 		image = array(mss.grab((x_left, y_top, x_right, y_bot)))
# 		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# 		return image
