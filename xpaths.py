"""
An Enum containing all XPath expressions to target
"""

from enum import Enum


class XPath(Enum):
	MAIN_BODY = "//body"
	SKILL_TREE = '//div[@data-test="skill-path"]'
	CONTINUE_BTN = '//button[contains(text(), "Continue")]'
	HAVE_ACCOUNT = '//button[@data-test="have-account"]'
	EMAIL_INPUT = '//input[@data-test="email-input"]'
	PASSWORD_INPUT = '//input[@data-test="password-input"]'
	REGISTER_BTN = '//button[@data-test="register-button"]'
	LOGOUT_MORE = '//span[text()="More"]/ancestor::span'
	LOGOUT_BTN = "//button[@data-test='logout-button']"
	COURSES_MENU = '//div[@data-test="courses-menu"]'
	LANG_LIST = '//div[contains(@class, "_3oF3u")]'
	SECTION_1 = '//h1[contains(text(), "1")]/ancestor::div/ancestor::div/div[@class="_1vvWf"]/button'
	STORY_LESSON = '//button[@aria-label="Lesson"]'
	STORY_BTN = '//button[@aria-label="Story"]'
	STORIES_CHOICE = '//button[@data-test="stories-choice"]'
	PRACTICE_BTN = '//a[contains(text(), "Practice +5 XP")]'
	WORD_TOKEN = '//span[@data-test="challenge-tap-token-text"]'
	STORY_CONTINUE_BEGIN = '//button[@data-test="stories-player-continue"]'
	PASSPORT_1 = '//span[text()="Cadê"]//ancestor::span//ancestor::button'
	PASSPORT_2 = '//span[text()="Yes"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'
	PASSPORT_3 = '//span[text()="thinks"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'
	PASSPORT_4 = '//button[text()="não está aqui"]'
	PASSPORT_5 = '//span[text()="mão"]//ancestor::span//ancestor::button'
	PASSPORT_6 = '//span[text()="hand"]/ancestor::div/ancestor::div/ancestor::li/button[@data-test="stories-choice"]'
	POPUP_CLOSE_1 = '//div[@class="_3nIAG _1v4iu _1Nb-2 _2klp6"]//button'
