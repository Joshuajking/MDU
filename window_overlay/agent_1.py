import cv2

from querysets.querysets import ImageQuerySet


class ActiveTakenMissionAgent:
	def __init__(self, main_agent):
		self.main_agent = main_agent
		self.db_images = ImageQuerySet.get_images_by_field()
		self.screen_images = cv2.imread(
			"SELECT image.image_url FROM image WHERE image.image_location == ACTIVE_TAKEN_MISSIONS_SCREEN")
		self.active_missions_screen_thread = None

	# TODO: create some methods for actions about any images found on the active_missions_screen
