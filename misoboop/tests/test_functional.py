from selenium import webdriver
import unittest
import pytest 

# TODO: write some functional tests; lower priority at the moment
# need to set up selenium on circleci

# class NewVisitorTest(unittest.TestCase):

#     def setUp(self):
#         self.browser = webdriver.Firefox()

#     def tearDown(self):
#         self.browser.quit()

#     def test_can_start_a_list_and_retrieve_it_later(self):
#         # Edith has heard about a cool new online to-do app. She goes
#         # to check out its homepage
#         self.browser.get('http://localhost:8000')

#         # She notices the page title and header mention to-do lists
#         self.assertIn('MisoBoop', self.browser.title)
#         self.fail('Finish the test!')

#         # She is invited to enter a to-do item straight away
#         # [...rest of comments as before]

if __name__ == '__main__':
    unittest.main(warnings='ignore')