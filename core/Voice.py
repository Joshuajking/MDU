# import queue
# from time import sleep
#
# import kthread
# import pyttsx3
#
# # rate = voiceEngine.getProperty('rate')
# # volume = voiceEngine.getProperty('volume')
# # voice = voiceEngine.getProperty('voice')
# # voiceEngine.setProperty('rate', newVoiceRate)
# # voiceEngine.setProperty('voice', voice.id)   id = 0, 1, ...
#
# """
# File:Voice.py
#
# Description:
#   Class to enapsulate the Text to Speech package in python
#
# To Use:
#   See main() at bottom as example
#
# Author: sumzer0@yahoo.com
#
# """
#
#
# class Voice:
#
# 	def __init__():
# 		q = queue.Queue(5)
# 		v_enabled = False
# 		v_quit = False
# 		t = kthread.KThread(target=voice_exec, name="Voice", daemon=True)
# 		t.start()
# 		v_id = 1
#
# 	def say(, vSay):
# 		if v_enabled:
# 			q.put(vSay)
#
# 	def set_off():
# 		v_enabled = False
#
# 	def set_on():
# 		v_enabled = True
#
# 	def set_voice_id(, id):
# 		v_id = id
#
# 	def quit():
# 		v_quit = True
#
# 	def voice_exec():
# 		engine = pyttsx3.init()
# 		voices = engine.getProperty('voices')
# 		v_id_current = 0  # David
# 		engine.setProperty('voice', voices[v_id_current].id)
# 		engine.setProperty('rate', 160)
# 		while not v_quit:
# 			# check if the voice ID changed
# 			if v_id != v_id_current:
# 				v_id_current = v_id
# 				try:
# 					engine.setProperty('voice', voices[v_id_current].id)
# 				except:
# 					print("Voice ID out of range")
#
# 			try:
# 				words = q.get(timeout=1)
# 				q.task_done()
# 				if words is not None:
# 					engine.say(words)
# 					engine.runAndWait()
# 			except:
# 				pass
#
#
# def main():
# 	v = Voice()
# 	v.set_on()
# 	sleep(2)
# 	v.say("Hey dude")
# 	sleep(2)
# 	v.say("whats up")
# 	sleep(2)
# 	v.quit()
#
#
# if __name__ == "__main__":
# 	main()
