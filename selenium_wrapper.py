"""
A Selenium wrapper to abstract common operations
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from enum import Enum
from xpaths import XPath


# from selenium.webdriver.chrome.service import Service
# from selenium.common.exceptions import NoSuchElementException


class WaitMethod(Enum):
	Visible = "visible"
	AnyVisible = "any_visible"
	Clickable = "clickable"


def browser_init() -> webdriver:
	"""Creates a browser object"""
	opts = Options()
	# opts.headless = True  # TODO uncomment when finished and merging to main branch
	opts.add_argument("user-agent=Mozilla/5.0")
	browser = webdriver.Chrome(options=opts)

	print("Requesting page...")
	browser.get("https://www.duolingo.com/")
	browser.maximize_window()
	print("maximized!")
	WebDriverWait(browser, 120).until(
		ec.visibility_of_element_located((By.XPATH, '//button[@data-test="have-account"]')))
	print("Page loaded!")
	return browser


def find_object(web_browser: webdriver, xpath: XPath | str):
	"""Wrapper for find_element Selenium method"""
	return web_browser.find_element(By.XPATH, xpath)


def find_multiple_objects(web_browser: webdriver, xpath: XPath | str):
	"""Wrapper for find_elements Selenium method"""
	return web_browser.find_elements(By.XPATH, xpath)


def fill_form_value(web_browser: webdriver, xpath: XPath | str, value: str):
	"""Wrapper for find_element.send_keys()"""
	return web_browser.find_element(By.XPATH, xpath).send_keys(value)


def wait(web_browser: webdriver, method: WaitMethod, xpath: XPath | str, timeout: int = 20, msg: str = "Error"):
	"""Wrapper for WebDriverWait Selenium event"""
	# TODO define if error msg for WebDriverWait should be present or handled different, investigate this
	# TODO wrap WebDriverWait in logger so TimeoutExceptions get logged properly
	if method == "visible":
		return WebDriverWait(web_browser, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)), msg)
	elif method == "any_visible":
		return WebDriverWait(web_browser, timeout).until(ec.visibility_of_any_elements_located((By.XPATH, xpath)), msg)
	elif method == "clickable":
		return WebDriverWait(web_browser, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)), msg)


def click_element(web_browser: webdriver, xpath: XPath | str, timeout: int = 10) -> bool:
	"""Waits for an element to be clickable, and clicks it, found by XPath. Returns found state"""
	try:
		WebDriverWait(web_browser, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)),
		                                          f"WebElement with XPath: {xpath} not found")
		(web_browser.find_element(By.XPATH, xpath)).click()
		return True
	except TimeoutException:
		print(f"Timeout exceeded, WebElement with XPath: {xpath} not found")
	except Exception as e:
		print(f"Error occurred at {click_element}: {e}")
	finally:
		return False


def hover_on_element(web_browser: webdriver, xpath: XPath | str, timeout: int = 20) -> None:
	"""Finds an element by XPath and hovers over it"""
	try:
		WebDriverWait(web_browser, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)),
		                                          f"WebElement with XPath: {xpath} not found, hover was not executed")
		element = web_browser.find_element(By.XPATH, xpath)
		hover = ActionChains(web_browser).move_to_element(element)
		hover.perform()
	except TimeoutException:
		print(f"Time to timeout exceeded, WebElement with XPath: {xpath} not found, hover was not executed")
