"""
An Enum containing all XPath expressions to target
"""

from enum import Enum


# TODO add all Xpath expressions in the following Enum

class XPath(Enum):
	SKILL_TREE = '//div[@data-test="skill-path"]'
	CONTINUE_BTN = '//button[contains(text(), "Continue")]'
