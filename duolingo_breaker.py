"""Duolingo Streak Mantainer
A Python Selenium script to automatically answer Duolingo stories
"""

from random import sample
import duolingo_wrapper

"""
TODO refactor print() for logger.info() https://docs.python.org/3/library/logging.html
import logging
logger = logging.getLogger("DUO_BREAKER")
logging.basicConfig(filename='duolingo_breaker_log.log', level=logging.INFO)
"""

if __name__ == "__main__":
	with open("./creds.txt", "r") as file:
		creds = [line.strip() for line in file.readlines()]
	USERNAME = creds[0]
	PASSWORD = creds[1]

	if duolingo_wrapper.login(USERNAME, PASSWORD):
		# duolingo_wrapper.check_popups()  # Check for pop-ups and close them
		# duolino_wrapper.select_language("Portuguese")  # Change language to Portuguese, if needed

		story_to_answer_id = sample([0, 1], 1)[0]
		story_to_answer_id = 0
		duolingo_wrapper.select_story(story_to_answer_id)

		if story_to_answer_id == 0:
			if duolingo_wrapper.answer_story_0():  # The Passport
				print("Story answered correctly! Dashboard is now loaded")
			else:
				print("Story failed")
		elif story_to_answer_id == 1:
			pass

		if duolingo_wrapper.logout():
			print("Duolingo streak mantained succesfully!")
		else:
			print("Error ocurred on logout")
	else:
		print("Error on login occurred!")
	print("Closing browser...")
