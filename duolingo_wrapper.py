"""
A wrapper for Selenium tailored for Duolingo website manipulation, extends functionality of selenium_wrapper
"""
import time

import selenium_wrapper as sw
from time import sleep
from xpaths import XPath

"""
==> Parent methods, pass browser variable 
"""

BROWSER = sw.browser_init()
print(f"Browser created! {BROWSER}")


def login(username: str, password: str, web_browser: sw.webdriver = BROWSER) -> bool:
	"""Logs in to the account"""
	try:
		print("Logging in...")
		sw.click_element(web_browser, XPath.HAVE_ACCOUNT.value)
		sw.wait(web_browser, sw.WaitMethod.Visible, XPath.EMAIL_INPUT.value)
		print("Filling credentials...")
		# email_input = sw.find_object(BROWSER, XPath.EMAIL_INPUT.value)
		# email_input.send_keys(username)
		time.sleep(5)
		sw.fill_form_value(web_browser, XPath.EMAIL_INPUT.value, username)
		# pass_input = sw.find_object(BROWSER, XPath.PASSWORD_INPUT.value)
		# pass_input.send_keys(password)
		time.sleep(5)
		sw.fill_form_value(web_browser, XPath.PASSWORD_INPUT.value, password)
		sw.click_element(web_browser, XPath.REGISTER_BTN.value)
		print("Awaiting dashboard load...")
		sw.wait(web_browser, sw.WaitMethod.Visible, XPath.SKILL_TREE.value)
		print("LOGGED IN! Dashboard loaded successfully")
		return True
	except Exception as e:
		print(f"An error occurred during {login}: {e}")
	return False


def logout(web_browser: sw.webdriver = BROWSER) -> bool:
	"""Logs out of the account"""
	print("Logging out...")
	try:
		sw.wait(web_browser, sw.WaitMethod.Clickable, XPath.LOGOUT_MORE.value)
		sw.hover_on_element(web_browser, XPath.LOGOUT_MORE.value)
		sw.click_element(web_browser, XPath.LOGOUT_BTN.value)
		web_browser.quit()
		return True
	except sw.TimeoutException:
		return False


def select_language(lang_to_switch: str = "Portuguese", web_browser: sw.webdriver = BROWSER) -> str:
	"""By default, switches the language to Portuguese, otherwise switches the language to the specified param value"""
	print(f"Selecting {lang_to_switch} language...")
	sw.wait(web_browser, sw.WaitMethod.Visible, XPath.COURSES_MENU.value)
	sw.hover_on_element(web_browser, XPath.COURSES_MENU.value)
	lang_list = sw.find_multiple_objects(web_browser, XPath.LANG_LIST.value)
	current_lang = lang_list[0].text
	if current_lang != lang_to_switch:
		print(f"Current selected language: {current_lang}")

		for web_elem in lang_list:
			if web_elem.text == lang_to_switch:
				web_elem.click()
				break
		print(f"{lang_to_switch} selected / {current_lang} => {lang_to_switch}")
	else:
		print(f"{lang_to_switch} is already selected!")
	web_browser.implicitly_wait(10)
	sw.wait(web_browser, sw.WaitMethod.Visible, XPath.SKILL_TREE.value, msg="Skilltree not found")
	print("Language switched successfully")
	return current_lang


def select_story(story_id: int, web_browser: sw.webdriver = BROWSER) -> bool:
	"""Selects a story from the menu"""
	# stories_xpath = '//button[@aria-label="Story"]'
	try:
		print("Loading stories tab...")
		web_browser.get("https://www.duolingo.com/sections")
		sleep(3)  # scroll to top and select section 1
		web_browser.execute_script("window.scrollTo(0, 0)")
		sw.wait(web_browser, sw.WaitMethod.Visible, XPath.SECTION_1.value, msg="Story section not found")
		print("Stories tab loaded, selecting section 1...")
		sw.click_element(web_browser, XPath.SECTION_1.value)

		if story_id == 0:
			sw.wait(web_browser, sw.WaitMethod.AnyVisible, XPath.STORY_LESSON.value)
			print("Section 1 selected, scrolling and selecting story...")
			sleep(3)  # scroll to story 0 and select it
			web_browser.execute_script("window.scrollTo(0, 1800)")
			sw.click_element(web_browser, XPath.STORY_BTN.value)
			sw.click_element(web_browser, XPath.PRACTICE_BTN.value)

		print("Story selected, waiting to be loaded...")
		sw.wait(web_browser, sw.WaitMethod.AnyVisible, XPath.STORY_CONTINUE_BEGIN.value)
		print("Story loaded correctly!")
		return True
	except Exception as e:
		print(f"An error occurred during {select_story}: {e}")
	return False


"""
==> Duolingo website manipulation functions, called by parent methods
"""


def click_until_exercise_and_solve(web_browser: sw.webdriver, exercise_solution_xpath: XPath, timeout: int = 2) -> bool:
	"""Infinite loop to click 'Continue' button until exercise presence located, then solve the exercise"""
	try:
		while not sw.click_element(web_browser, exercise_solution_xpath, timeout):
			sw.click_element(web_browser, XPath.CONTINUE_BTN.value, timeout)
		return True
	except Exception as e:
		print(f"Error occurred at {click_until_exercise_and_solve}: {e}")
	return False


def answer_story_0(web_browser: sw.webdriver = BROWSER) -> bool:
	"""Answers story: The Passport"""
	try:
		sleep(5)

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_1.value):
			return False

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_2.value):
			return False

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_3.value):
			return False

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_4.value):
			return False

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_5.value):
			return False

		if not click_until_exercise_and_solve(web_browser, XPath.PASSPORT_6.value):
			return False

		sw.click_element(web_browser, XPath.CONTINUE_BTN.value)

		# * Final exercise - Select matching pairs
		# TODO keep filling workbank
		story_wordbank = {
			"where is": "cadê",
			"wife": "esposa",
			"hand": "mão",
			"runs after": "corre atrás de",
			"my love": "meu amor",
			"bag": "bolsa",
			"thank you": "obrigado",
			"problem": "problema",
			"in the": "no",
			"oh no": "ah, não",
			"passport": "passaporte",
			"is": "está"
		}

		story_wordbank = filter_present_words_dict(web_browser, story_wordbank)
		select_matching_pairs(web_browser, story_wordbank)

		sw.click_element(web_browser, XPath.CONTINUE_BTN.value)
		skip_all_post_story_completion(web_browser)

		return True
	except Exception as e:
		print(f"Error occurred at {answer_story_0}: {e}")
	return False


def check_popups(web_browser: sw.webdriver) -> bool:
	"""Checks for a pop-up in the main interface and exits it"""
	# TODO investigate any other popup scenarios
	try:
		if sw.click_element(web_browser, XPath.POPUP_CLOSE_1.value):
			print("Pop-up was found, and closed succesfully")
		else:
			print("No pop up was found")
	except sw.TimeoutException:
		print("No pop-ups were found, continuing execution...")
	except Exception as e:
		print(f"No pop-ups found, but an error could have occurred... {e}")
	return False


"""
=> Exercise manipulation methods
"""


def skip_all_post_story_completion(web_browser: sw.webdriver, timeout: int = 8):
	"""After story completion, presses ENTER key automatically until dashboard is loaded"""
	while True:  # Keep sending ENTER presses until the execution returns to the main menu
		try:
			sw.wait(web_browser, sw.WaitMethod.Visible, XPath.SKILL_TREE.value, timeout, "Continue button not found, yet")
			break
		except sw.TimeoutException:
			# sw.find_object(web_browser, XPath.MAIN_BODY.value).send_keys("\ue007")
			sw.fill_form_value(web_browser, XPath.MAIN_BODY.value, "\ue007")


def select_missing_phrase(web_browser: sw.webdriver, text_to_match: str) -> None:
	"""Selects the missing phrase from a list of button options"""
	for web_elem in sw.find_multiple_objects(web_browser, XPath.STORIES_CHOICE.value):
		if web_elem.text == text_to_match:
			web_elem.click()


def order_the_sentence(web_browser: sw.webdriver, ordered_sentence: str) -> None:
	"""Receives a sentence, then clicks the words that conform it, in order"""
	for word in ordered_sentence.split(" "):
		sw.click_element(web_browser, f"//button[@data-test='challenge-tap-token']/span[text()='{word.strip()}']")


def filter_present_words_dict(web_browser: sw.webdriver, wordbank: dict) -> dict:
	"""Filter the story wordbank dict with the present words in the exercise"""

	present_words = [span.text for span in
	                 sw.find_multiple_objects(web_browser, XPath.WORD_TOKEN.value)]
	# Filter the dictionary with the words present in the exercise
	present_words = list(filter(lambda word: word in wordbank.keys(), present_words))

	intersected_words = list(set(present_words).intersection(wordbank.keys()))
	wordbank = {key: wordbank[key] for key in intersected_words}
	return wordbank


def select_matching_pairs(web_browser: sw.webdriver, wordbank: dict, timeout: int = 5) -> None:
	"""Iterates through a dict and clicks the correct items"""
	for k, v in wordbank.items():
		try:
			sw.click_element(web_browser,
			                 f"//span[@data-test='challenge-tap-token-text'][text()='{k}']/ancestor::span/ancestor::button",
			                 timeout)
			sw.click_element(web_browser,
			                 f"//span[@data-test='challenge-tap-token-text'][text()='{v}']/ancestor::span/ancestor::button",
			                 timeout)
		except Exception as e:
			print(f"Exercise: [{k} => {v}] not found on this instance, therefore skipping, error: {e}")
