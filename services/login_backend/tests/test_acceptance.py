
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import TestConfig

class TestAcceptance(unittest.TestCase):

    def setUp(self):
        # Set up the webdriver for your browser (e.g., Chrome or Firefox)
        self.driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
        self.driver.get(TestConfig.TEST_SERVER)

    def tearDown(self):
        self.driver.quit()

    def test_list_groups(self):
        driver = self.driver

        # Log in
        driver.find_element_by_link_text('Login').click()
        email_field = driver.find_element_by_name('email')
        email_field.send_keys('test@example.com')
        password_field = driver.find_element_by_name('password')
        password_field.send_keys('test_password')
        password_field.submit()

        # Check if the user is on the profile page
        self.assertIn('Profile', driver.title)

        # Navigate to list_groups
        driver.find_element_by_link_text('List Groups').click()

        # Check if the user is on the list_groups page
        self.assertIn('List Groups', driver.title)

        # Check if the list of groups is present
        group_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'group-list'))
        )
        self.assertIsNotNone(group_list)

    def test_create_group(self):
        driver = self.driver

        # Log in
        driver.find_element_by_link_text('Login').click()
        email_field = driver.find_element_by_name('email')
        email_field.send_keys('test@example.com')
        password_field = driver.find_element_by_name('password')
        password_field.send_keys('test_password')
        password_field.submit()

        # Check if the user is on the profile page
        self.assertIn('Profile', driver.title)

        # Navigate to create_group
        driver.find_element_by_link_text('Create Group').click()

        # Check if the user is on the create_group page
        self.assertIn('Create Group', driver.title)

        # Fill out the form and submit it
        group_name_field = driver.find_element_by_name('group_name')
        group_name_field.send_keys('New Test Group')
        group_description_field = driver.find_element_by_name('group_description')
        group_description_field.send_keys('A test group created during acceptance testing.')
        group_description_field.submit()

        # Check if the group creation was successful
        success_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'success-message'))
        )
        self.assertIsNotNone(success_message)
        self.assertIn('Group created successfully', success_message.text)

# if __name__ == '__main__':
#     unittest.main()
