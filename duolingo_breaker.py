"""Duolingo Streak Mantainer
A Python Selenium script to automatically answer Duolingo stories
"""

from random import sample

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

# GLOBAL VARS
WEBDRIVER = Service("C:/Users/Drablaguna/Desktop/Dev/chromedriver")
DUOLINGO_URL = "https://www.duolingo.com/"
with open("C:/Users/Drablaguna/Desktop/creds.txt", "r") as file:
	creds = [line.strip() for line in file.readlines()]
USERNAME = creds[0]
PASSWORD = creds[1]
CONTINUE_BUTTON_XPATH = "//button[@data-test='stories-player-continue']"

opts = Options()
# opts.headless = True
opts.add_argument("user-agent=Mozilla/5.0")
browser = webdriver.Chrome(service=WEBDRIVER, options=opts)

print("Requesting page...")
browser.get(DUOLINGO_URL)
# browser.maximize_window()

WebDriverWait(browser, 120).until(ec.visibility_of_element_located((By.XPATH, '//div[@class="liLLN"]')))
print("Page loaded!")


def login() -> bool:
	"""Logs in to the account"""
	print("Logging in...")
	browser.find_element(By.XPATH, "//button[@data-test='have-account']").click()

	WebDriverWait(browser, 20).until(
		ec.visibility_of_element_located((By.XPATH, '//input[@class="_3MNft fs-exclude"]')))
	print("Filling credentials...")
	login_inputs = browser.find_elements(By.XPATH, '//input[@class="_3MNft fs-exclude"]')
	login_inputs[0].send_keys(USERNAME)
	login_inputs[1].send_keys(PASSWORD)
	browser.find_element(By.XPATH, "//button[@data-test='register-button']").click()
	print("LOGGED IN!")
	print("Awaiting dashboard load...")
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="_3ZJK8"]')))
	print("Dashboard loaded successfully!")
	return True


def select_language(lang_to_switch: str = "German") -> str:
	"""By default switches the language to German, otherwise switches the language to the specified param value"""
	print(f"Selecting {lang_to_switch} language...")
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//div[@data-test="courses-menu"]')))
	hover_on_element('//div[@data-test="courses-menu"]')
	lang_list = browser.find_elements(By.XPATH, '//div[contains(@class, "_2WiQc")]')
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
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="_3ZJK8"]')),
	                                 "Skilltree not found")
	print("Language switched successfully")
	return current_lang


def select_story(story_id: int) -> bool:
	"""Selects a story from the menu"""
	print("Loading stories tab...")
	browser.get("https://www.duolingo.com/stories")
	WebDriverWait(browser, 20).until(ec.visibility_of_element_located((By.XPATH, '//*[@class="X4jDx"]')),
	                                 "Story elements not found")
	browser.find_elements(By.XPATH, '//*[@class="X4jDx"]')[story_id].click()
	WebDriverWait(browser, 20).until(
		ec.visibility_of_element_located(
			(
				By.XPATH,
				'//a[@data-test="story-start-button"]',
			)
		),
		"Clickable Story element not found"
	)
	browser.find_element(By.XPATH, '//a[@data-test="story-start-button"]').click()

	return True


"""
=> Common Selenium methods
"""


def click_element(xpath: str, timeout: int = 20) -> None:
	"""Waits for an element to be clickable, and clicks it, found by XPath"""
	try:
		WebDriverWait(browser, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)),
		                                      f"WebElement with XPath: {xpath} not found")
		(browser.find_element(By.XPATH, xpath)).click()
	except TimeoutException:
		print(f"Time to timeout exceeded, WebElement with XPath: {xpath} not found")


def hover_on_element(xpath: str) -> None:
	"""Hovers on an element"""
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


def check_popups():
	"""Checks for a pop-up in the main interface and exits it"""
	try:
		click_element("//button[@data-test='notification-drawer-no-thanks-button']", 8)
		print("Pop-up was found, and closed succesfully")
	except TimeoutException:
		print("No pop-ups were found, continuing execution...")


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
			click_element(f"//span[@data-test='challenge-tap-token-text'][text()='{k}']/ancestor::li/button", 3)
			click_element(f"//span[@data-test='challenge-tap-token-text'][text()='{v}']/ancestor::li/button", 3)
		except Exception as e:
			print(f"Exercise: [{k} => {v}] not found on this instance, error: {e}")


def answer_story_137() -> None:
	"""Answers story num 137 - Turbulence"""
	print("Answering story num 137 - Turbulence...")

	WebDriverWait(browser, 20).until(ec.element_to_be_clickable((By.XPATH, CONTINUE_BUTTON_XPATH)))

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)  # * CHECK

	# * Select the missing phrase
	select_missing_phrase("werde ich berühmt")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select correct checkbox
	click_element("//span[contains(text(),'wackelt')]/ancestor::li/button")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select the missing phrase
	select_missing_phrase("So etwas passiert oft")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select correct checkbox
	click_element("//span[contains(text(),'Angst')]/ancestor::li/button")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select correct checkbox
	click_element("//span[contains(text(),'stirbt')]/ancestor::li/button")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Order the sentence
	order_the_sentence("Plötzlich hören sie den Piloten")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select correct checkbox
	click_element("//span[contains(text(),'entspannen')]/ancestor::li/button")

	click_element(CONTINUE_BUTTON_XPATH)
	click_element(CONTINUE_BUTTON_XPATH)

	# * Select correct checkbox
	click_element("//span[contains(text(),'abgestürzt')]/ancestor::li/button")

	click_element(CONTINUE_BUTTON_XPATH)

	# * Final exercise - Select matching pairs
	story_wordbank = {
		"over": "vorbei",
		"relax": "entspannen",
		"turbulence": "Turbulenzen",
		"crashed": "abgestürzt",
		"not a big deal": "nicht schlimm",
		"noise": "Geräusch",
		"plane crash": "Flugzeugabsturz",
		"plane": "Flugzeug",
		"never": "nie",
		"bird": "vogel",
		"famous": "berühmt"
	}

	story_wordbank = filter_present_words_dict(story_wordbank)
	select_matching_pairs(story_wordbank)

	click_element(CONTINUE_BUTTON_XPATH)
	while True:  # Keep sending ENTER presses until the execution returns to the main menu
		try:
			WebDriverWait(browser, 8).until(
				ec.visibility_of_element_located((By.XPATH, '//div[@data-test="courses-menu"]')),
				"Continue button not found, yet")
			break
		except TimeoutException:
			browser.find_element(By.XPATH, "//body").send_keys("\ue007")


def logout() -> bool:
	"""Logs out of the account"""
	print("Logging out...")
	try:
		WebDriverWait(browser, 20).until(ec.element_to_be_clickable((By.XPATH, "//div[@data-test='profile-dropdown']")))
		hover_on_element("//div[@data-test='profile-dropdown']")
		click_element("//button[@data-test='logout-button']")
		return True
	except TimeoutException:
		return False


if __name__ == "__main__":
	if not login():
		print("Error on login occurred!")
	else:
		# Check for pop-ups and close them
		check_popups()

		selected_language = select_language()

		if selected_language != "German":
			select_language(selected_language)

		story_to_answer_id = sample([137, 137], 1)[0]
		select_story(story_to_answer_id)

		if story_to_answer_id == 137:
			answer_story_137()
		elif story_to_answer_id == 82:
			pass

		if logout() is True:
			print("Duolingo streak mantained succesfully! You smartass!!!")
		else:
			print("Error ocurred on logout")
	print("Closing browser...")
	browser.quit()
