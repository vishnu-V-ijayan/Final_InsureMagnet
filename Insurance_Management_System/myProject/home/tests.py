# from django.test import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTests(LiveServerTestCase):
#     def setUp(self):
#         self.live_server_url = 'http://127.0.0.1:8000'
#         self.browser = webdriver.Chrome()
#         self.browser.implicitly_wait(10)

#     def tearDown(self):
#         self.browser.quit()

#     def test_valid_login_redirects_to_admin_dashboard_and_performs_category_actions(self):
#         # Open the login page
#         self.browser.get(self.live_server_url + '/handlelogin/')

#         # Wait for the email input field to be present
#         email_input = WebDriverWait(self.browser, 10).until(
#             EC.presence_of_element_located((By.ID, 'email'))
#         )

#         # Enter valid admin credentials
#         password_input = self.browser.find_element(By.ID, 'password')
#         submit_button = self.browser.find_element(By.ID, 'submit')

#         email_input.send_keys('vvvadoor@gmail.com')
#         password_input.send_keys('Admin@123')
#         submit_button.click()

#         # Check if the admin is redirected to the admin dashboard
#         expected_url = self.live_server_url + '/admin_dashboard/'
#         self.assertEqual(self.browser.current_url, expected_url)

#         # Click on the "Category" button in the admin dashboard
#         category_button = WebDriverWait(self.browser, 10).until(
#             EC.element_to_be_clickable((By.XPATH, '//a[@href="/admin-category"]'))
#         )
#         category_button.click()

#         # Check if the admin is redirected to the admin_category page
#         expected_url = self.live_server_url + '/admin-category'
#         self.assertEqual(self.browser.current_url, expected_url)

#         # Click on the "Add Category" link
#         add_category_link = WebDriverWait(self.browser, 20).until(
#             EC.element_to_be_clickable((By.XPATH, '//a[@href="admin-add-category"]'))
#         )
#         add_category_link.click()

#         # Check if the admin is redirected to the admin-add-category page
#         expected_url = self.live_server_url + '/admin-add-category'
#         self.assertEqual(self.browser.current_url, expected_url)

#         # Fill in the form to add a category
#         category_name_input = WebDriverWait(self.browser, 20).until(
#             EC.presence_of_element_located((By.ID, 'id_category_name'))
#         )
#         category_name_input.send_keys('Travel Insurance')

#         # Submit the form
#         submit_button = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
#         submit_button.click()

#         # Check if the admin is redirected to the admin-view-category page (adjust the URL accordingly)
#         expected_url = self.live_server_url + '/admin-view-category'
#         self.assertEqual(self.browser.current_url, expected_url)

#         # Add more assertions or actions as needed based on the behavior of the admin-view-category page
#         # For example, check if the added category is visible on the page.


# from django.test import TestCase

# # Create your tests here.
# from datetime import datetime
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# class Hosttest(TestCase):
    
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()
        
#     def test_01_login_page(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/handlelogin/']")

#         login.click()
#         time.sleep(2)
#         email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
#         email.send_keys("vvvadoor@gmail.com")
#         password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
#         password.send_keys("Admin@123")
#         time.sleep(2)
#         submit = driver.find_element(By.CSS_SELECTOR, "button#submit")  # Ensure the correct CSS selector for the button
#         submit.click()
#         time.sleep(2)


# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time

# class HostTest(TestCase):
    
#     def setUp(self):
#         # Set up the WebDriver
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         # Clean up after each test method
#         self.driver.quit()
        
#     def test_add_agent(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()

#         # Navigate to the login page and log in
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/handlelogin/']")
#         login.click()
#         time.sleep(2)

#         email = driver.find_element(By.CSS_SELECTOR, "input[type='email'][name='email']")
#         email.send_keys("vvvvv5adoor@gmail.com")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='password']")
#         password.send_keys("User@123")
#         submit_button = driver.find_element(By.CSS_SELECTOR, "button#submit")
#         submit_button.click()
#         time.sleep(2)

#         # Navigate to Register Agents after login
#         register_agents = driver.find_element(By.CSS_SELECTOR, "a[href='/add-agent/']")
#         register_agents.click()
#         time.sleep(2)

#         # Fill the form with agent details
#         driver.find_element(By.NAME, "email").send_keys("agentt@example.com")
#         driver.find_element(By.NAME, "name").send_keys("John Doe")
#         driver.find_element(By.NAME, "address").send_keys("123 Street, City")
#         driver.find_element(By.NAME, "place").send_keys("CityPlace")
#         driver.find_element(By.NAME, "location").send_keys("LocationArea")
#         driver.find_element(By.NAME, "pin").send_keys("123456")
#         driver.find_element(By.NAME, "phone").send_keys("923267890")
#         driver.find_element(By.NAME, "gender").send_keys("Male")
#         driver.find_element(By.NAME, "qualification").send_keys("Degree")
#         driver.find_element(By.NAME, "aadhar").send_keys("125412311234")
#         driver.find_element(By.NAME, "registration_date").send_keys("01-01-2021")
#         #driver.find_element(By.NAME, "photo").send_keys("C:\Users\vishn\OneDrive\Desktop\MCA\sem4\banner-shape-01.png")  # Adjust path as necessary
#         driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
#         time.sleep(3)


# from django.test import TestCase
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class Hosttest(TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()

#     def test_01_login_page_and_ask_question(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/handlelogin/']")
#         login.click()
#         time.sleep(2)
#         email = driver.find_element(By.CSS_SELECTOR, "input[type='email'][name='email']")
#         email.send_keys("vishnuadrofficial@gmail.com")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='password']")
#         password.send_keys("User@123")
#         time.sleep(2)
#         submit = driver.find_element(By.CSS_SELECTOR, "button#submit")
#         submit.click()
#         time.sleep(2)

#         # Navigate to the Ask Question page
#         ask_question_button = driver.find_element(By.CSS_SELECTOR, "a[href='/ask-question']")
#         ask_question_button.click()
#         time.sleep(2)

#         # Wait until the textarea is visible and then type the question
#         question_text_area = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.ID, "id_description"))
#         )
#         question_text_area.send_keys("Could you provide more information on the different types of insurance coverage available?")

#         # Submit the question
#         submit_question_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn.btn-primary")
#         submit_question_button.click()
#         time.sleep(2)




# from django.test import TestCase
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class Hosttest(TestCase):

#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()

#     def test_01_login_and_register_office(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)

#         # Login steps
#         login = driver.find_element(By.CSS_SELECTOR, "a[href='/handlelogin/']")
#         login.click()
#         time.sleep(2)

#         email = driver.find_element(By.CSS_SELECTOR, "input[type='email'][name='email']")
#         email.send_keys("vvvadoor@gmail.com")
#         password = driver.find_element(By.CSS_SELECTOR, "input[type='password'][name='password']")
#         password.send_keys("Admin@123")
#         time.sleep(2)
#         submit = driver.find_element(By.CSS_SELECTOR, "button#submit")
#         submit.click()
#         time.sleep(2)

#         # Navigate to the Office Registration page
#         office_registration = driver.find_element(By.CSS_SELECTOR, "a[href='/register_office']")
#         office_registration.click()
#         time.sleep(2)

#         # Fill the Office Registration form
#         driver.find_element(By.ID, "address").send_keys("123 Street, XYZ Building")
#         driver.find_element(By.ID, "place").send_keys("Central Park")
#         driver.find_element(By.ID, "location").send_keys("Main Area")
#         driver.find_element(By.ID, "pin").send_keys("123456")
#         driver.find_element(By.ID, "phone").send_keys("1234567890")
#         driver.find_element(By.ID, "district").send_keys("New District")
#         driver.find_element(By.ID, "state").send_keys("Kerala")
        
#         # Submit the form
#         driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
#         time.sleep(2)

#         # Optional: Add assertions to check for successful registration or validation messages
#         # Example: assert "Registration Successful" in driver.page_source








