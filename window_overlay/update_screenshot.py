from threading import Thread

import cv2 as cv
import mss
import numpy as np
import pyautogui


class MainAgent:
    def __init__(self):
        self.agent = []
        self.some_other_thread = None

        self.cur_img = None  # BGR Image
        self.cur_imgHSV = None  # HSV Image

        self.time = "night"  # keep track of night/day

        self.w, self.h = pyautogui.size()
        self.screenshot = None


def update_screen(agent):
    w, h = pyautogui.size()
    monitor = {"top": 0, "left": 0, "width": w, "height": h}
    with mss.mss() as sct:
        while True:
            agent.cur_img = sct.grab(monitor)
            agent.cur_img = np.array(agent.cur_img)  # Convert to NumPy array
            # agent.cur_img = cv.cvtColor(agent.cur_img, cv.COLOR_RGB2BGR)  # Convert RGB to BGR color
            agent.cur_imgHSV = cv.cvtColor(agent.cur_img, cv.COLOR_RGB2HSV)

            small = cv.resize(agent.cur_img, (0, 0), fx=0.75, fy=0.75)
            cv.imshow("Computer Vision", small)

            key = cv.waitKey(1)
            if key == ord("q"):
                break


if __name__ == "__main__":
    main_agent = MainAgent()

    update_screen_thread = Thread(
        target=update_screen,
        args=(main_agent,),
        name="update_screen_thread",
        daemon=False,
    )
    update_screen_thread.start()
