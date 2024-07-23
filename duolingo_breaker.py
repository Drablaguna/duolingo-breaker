"""Duolingo Streak Mantainer
A Python Selenium script to automatically answer Duolingo stories
"""

from random import sample
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep

"""
TODO refactor print() for logger.info() https://docs.python.org/3/library/logging.html
import logging
logger = logging.getLogger("DUO_BREAKER")
logging.basicConfig(filename='duolingo_breaker_log.log', level=logging.INFO)
"""

# GLOBAL VARS
with open("./creds.txt", "r") as file:
	creds = [line.strip() for line in file.readlines()]
USERNAME = creds[0]
PASSWORD = creds[1]
CONTINUE_BUTTON_XPATH = '//button[contains(text(), "Continue")]'
SKILL_TREE_XPATH = '//div[@data-test="skill-path"]'

opts = Options()
# TODO uncomment when finished
# opts.headless = True
opts.add_argument("user-agent=Mozilla/5.0")
browser = webdriver.Chrome(options=opts)
# WEBDRIVER = Service("C:/Users/Drablaguna/Desktop/Dev/chromedriver")
# browser = webdriver.Chrome(service=WEBDRIVER, options=opts)

print("Requesting page...")
browser.get("https://www.duolingo.com/")
browser.maximize_window()
print("maximized!")
WebDriverWait(browser, 120).until(ec.visibility_of_element_located((By.XPATH, '//button[@data-test="have-account"]')))
print("Page loaded!")


# ====================================================
# INSTRUCTION DUMP

def login() -> bool:
	"""Logs in to the account"""
	try:
		print("Logging in...")
		click_element('//button[@data-test="have-account"]')
		WebDriverWait(browser, 20).until(
			ec.visibility_of_element_located((By.XPATH, '//input[@data-test="email-input"]')))
		print("Filling credentials...")
		email_input = browser.find_element(By.XPATH, '//input[@data-test="email-input"]')
		email_input.send_keys(USERNAME)
		pass_input = browser.find_element(By.XPATH, '//input[@data-test="password-input"]')
		pass_input.send_keys(PASSWORD)
		click_element('//button[@data-test="register-button"]')
		print("Awaiting dashboard load...")
		WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, SKILL_TREE_XPATH)))
		print("LOGGED IN! Dashboard loaded successfully")
		return True
	except Exception as e:
		print(f"An error occured during {login}: {e}")
	return False


def select_language(lang_to_switch: str = "Portuguese") -> str:
	"""By default, switches the language to Portuguese, otherwise switches the language to the specified param value"""
	print(f"Selecting {lang_to_switch} language...")
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//div[@data-test="courses-menu"]')))
	hover_on_element('//div[@data-test="courses-menu"]')
	lang_list = browser.find_elements(By.XPATH, '//div[contains(@class, "_3oF3u")]')
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
	browser.implicitly_wait(10)
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, SKILL_TREE_XPATH)),
	                                 "Skilltree not found")
	print("Language switched successfully")
	return current_lang


# TODO wrap WebDriverWait in logger so TimeOutExceptions get logged properly, check if any extra logic is needed as it returns str or object
def select_story(story_id: int) -> bool:
	"""Selects a story from the menu"""
	section_1_xpath = '//h1[contains(text(), "1")]/ancestor::div/ancestor::div/div[@class="_1vvWf"]/button'
	stories_xpath = '//button[@aria-label="Story"]'
	try:
		print("Loading stories tab...")
		browser.get("https://www.duolingo.com/sections")
		sleep(3)  # scroll to top and select section 1
		browser.execute_script("window.scrollTo(0, 0)")
		WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, section_1_xpath)),
		                                 "Story section not found")
		print("Stories tab loaded, selecting section 1...")
		click_element(section_1_xpath)

		if story_id == 0:
			WebDriverWait(browser, 20).until(
				ec.visibility_of_any_elements_located((By.XPATH, '//button[@aria-label="Lesson"]')),
				"Story buttons not found")
			print("Section 1 selected, scrolling and selecting story...")
			sleep(3)  # scroll to story 0 and select it
			browser.execute_script("window.scrollTo(0, 1800)")
			click_element('//button[@aria-label="Story"]')
			click_element('//a[contains(text(), "Practice +5 XP")]')

		print("Story selected, waiting to be loaded...")
		WebDriverWait(browser, 20).until(
			ec.visibility_of_any_elements_located((By.XPATH, '//button[@data-test="stories-player-continue"]')),
			"Story not loaded correctly")

		print("Story loaded correctly!")
		return True
	except Exception as e:
		print(f"An error occured during {select_story}: {e}")
	return False


def click_until_exercise_and_solve(exercise_solution_xpath: str) -> bool:
	"""Infinite loop to click 'Continue' button until exercise presence located, then solve the exercise"""
	try:
		while not click_element(exercise_solution_xpath, 2):
			click_element(CONTINUE_BUTTON_XPATH, 2)
		return True
	except Exception as e:
		print(f"Error occured at {click_until_exercise_and_solve}: {e}")
	return False


def answer_story_0() -> bool:
	"""Answers story: The Passport"""
	try:
		sleep(5)

		if not click_until_exercise_and_solve('//span[text()="Cadê"]//ancestor::span//ancestor::button'):
			return False

		if not click_until_exercise_and_solve(
				'//span[text()="Yes"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'):
			return False

		if not click_until_exercise_and_solve(
				'//span[text()="thinks"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'):
			return False

		if not click_until_exercise_and_solve('//button[text()="não está aqui"]'):
			return False

		if not click_until_exercise_and_solve('//span[text()="mão"]//ancestor::span//ancestor::button'):
			return False

		if not click_until_exercise_and_solve(
				'//span[text()="hand"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'):
			return False

		click_element(CONTINUE_BUTTON_XPATH)

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

		story_wordbank = filter_present_words_dict(story_wordbank)
		select_matching_pairs(story_wordbank)

		click_element(CONTINUE_BUTTON_XPATH)
		skip_all_post_story_completion()
		
		return True
	except Exception as e:
		print(f"Error occured at {answer_story_0}: {e}")
	return False


def skip_all_post_story_completion():
	"""After story completion, presses ENTER key automatically until dashboard is loaded"""
	while True:  # Keep sending ENTER presses until the execution returns to the main menu
		try:
			WebDriverWait(browser, 8).until(
				ec.visibility_of_element_located((By.XPATH, SKILL_TREE_XPATH)),
				"Continue button not found, yet")
			break
		except TimeoutException:
			browser.find_element(By.XPATH, "//body").send_keys("\ue007")


"""
=> Common Selenium methods
"""


def click_element(xpath: str, timeout: int = 10) -> bool:
	"""Waits for an element to be clickable, and clicks it, found by XPath. Returns found state"""
	try:
		WebDriverWait(browser, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)),
		                                      f"WebElement with XPath: {xpath} not found")
		(browser.find_element(By.XPATH, xpath)).click()
		return True
	except TimeoutException:
		print(f"Timeout exceeded, WebElement with XPath: {xpath} not found")
	except Exception as e:
		print(f"Error occurred at {click_element}: {e}")
	return False


def hover_on_element(xpath: str) -> None:
	"""Finds an element by XPath and hovers over it"""
	try:
		WebDriverWait(browser, 20).until(ec.element_to_be_clickable((By.XPATH, xpath)),
		                                 f"WebElement with XPath: {xpath} not found, hover was not executed")
		element = browser.find_element(By.XPATH, xpath)
		hover = ActionChains(browser).move_to_element(element)
		hover.perform()
	except TimeoutException:
		print(f"Time to timeout exceeded, WebElement with XPath: {xpath} not found, hover was not executed")


"""
=> UI manipulation methods
"""


def check_popups() -> bool:
	"""Checks for a pop-up in the main interface and exits it"""
	# TODO investigate any other popup scenarios
	try:
		# click_element("//button[@data-test='notification-drawer-no-thanks-button']", 8)
		if click_element('//div[@class="_3nIAG _1v4iu _1Nb-2 _2klp6"]//button'):
			print("Pop-up was found, and closed succesfully")
		else:
			print("No pop up was found")
	except TimeoutException:
		print("No pop-ups were found, continuing execution...")
	except Exception as e:
		print(f"No pop-ups found, but an error could have occurred... {e}")
	return False


"""
=> Exercise specific methods
"""


def select_missing_phrase(text_to_match: str) -> None:
	"""Selects the missing phrase from a list of button options"""
	for webelem in browser.find_elements(By.XPATH, "//button[@data-test='stories-choice']"):
		if webelem.text == text_to_match:
			webelem.click()


def order_the_sentence(ordered_sentence: str) -> None:
	"""Receives a sentence, then clicks the words that conform it, in order"""
	for word in ordered_sentence.split(" "):
		click_element(f"//button[@data-test='challenge-tap-token']/span[text()='{word.strip()}']")


def filter_present_words_dict(wordbank: dict) -> dict:
	"""Filter the story wordbank dict with the present words in the exercise"""
	present_words = [span.text for span in
	                 browser.find_elements(By.XPATH, '//span[@data-test="challenge-tap-token-text"]')]
	# Filter the dictionary with the words present in the exercise
	present_words = list(filter(lambda word: word in wordbank.keys(), present_words))

	intersected_words = list(set(present_words).intersection(wordbank.keys()))
	wordbank = {key: wordbank[key] for key in intersected_words}
	return wordbank


def select_matching_pairs(wordbank: dict) -> None:
	"""Iterates through a dict and clicks the correct items"""
	for k, v in wordbank.items():
		try:
			click_element(
				f"//span[@data-test='challenge-tap-token-text'][text()='{k}']/ancestor::span/ancestor::button", 5)
			click_element(
				f"//span[@data-test='challenge-tap-token-text'][text()='{v}']/ancestor::span/ancestor::button", 5)
		except Exception as e:
			print(f"Exercise: [{k} => {v}] not found on this instance, therefore skipping, error: {e}")


def logout() -> bool:
	"""Logs out of the account"""
	print("Logging out...")
	try:
		WebDriverWait(browser, 20).until(ec.element_to_be_clickable((By.XPATH, '//span[text()="More"]/ancestor::span')))
		hover_on_element('//span[text()="More"]/ancestor::span')
		click_element("//button[@data-test='logout-button']")
		return True
	except TimeoutException:
		return False


if __name__ == "__main__":
	if login():
		# check_popups()  # Check for pop-ups and close them
		# select_language("Portuguese")  # Change language to Portuguese, if needed

		story_to_answer_id = sample([0, 1], 1)[0]
		story_to_answer_id = 0
		select_story(story_to_answer_id)

		if story_to_answer_id == 0:
			if answer_story_0():  # The Passport
				print("Story answered correctly! Dashboard is now loaded")
			else:
				print("Story failed")
		elif story_to_answer_id == 1:
			pass

		if logout():
			print("Duolingo streak mantained succesfully!")
		else:
			print("Error ocurred on logout")
	else:
		print("Error on login occurred!")
	print("Closing browser...")
	browser.quit()
