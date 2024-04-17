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

#     def test_valid_login_redirects_to_customer_dashboard_and_applies_policy(self):
#         # Open the login page
#         self.browser.get(self.live_server_url + '/handlelogin/')

#         # Wait for the email input field to be present
#         email_input = WebDriverWait(self.browser, 10).until(
#             EC.presence_of_element_located((By.ID, 'email'))
#         )

#         # Enter valid credentials
#         password_input = self.browser.find_element(By.ID, 'password')
#         submit_button = self.browser.find_element(By.ID, 'submit')

#         email_input.send_keys('sample05@gmail.com')
#         password_input.send_keys('User@123')
#         submit_button.click()

#         # Check if the user is redirected to the hospital dashboard
#         expected_url = self.live_server_url + '/hospital_dashboard/'
#         self.assertEqual(self.browser.current_url, expected_url)

#         # Locate the "Generate PDF" link by its ID and wait for it to be clickable
#         generate_pdf_link = WebDriverWait(self.browser, 10).until(
#             EC.element_to_be_clickable((By.ID, 'generatepdf'))
#         )

#         # Use JavaScript to scroll to the element's location
#         self.browser.execute_script("arguments[0].scrollIntoView();", generate_pdf_link)

#         # Add JavaScript to change the background color for debugging
#         # self.browser.execute_script("document.body.style.backgroundColor = '';")

#         # Click the link using JavaScript to handle potential issues
#         self.browser.execute_script("arguments[0].click();", generate_pdf_link)

#         # Print some information for debugging
#         print(f"Current URL: {self.browser.current_url}")
#         print(f"Page source: {self.browser.page_source}")

#         # Add a wait to give some time for the PDF to be generated (you can adjust the time)
#         WebDriverWait(self.browser, 10).until(
#             EC.url_contains('generate_pdf')  # You can adjust this condition based on your application behavior
#         )

#         # # Now you are on the page where the PDF is generated. Add additional assertions or actions as needed.
#         # # For example, you might want to check if the PDF is visible on the page or download it.
#         # pdf_element = self.browser.find_element(By.TAG_NAME, 'pdf')  # Adjust the tag name based on your PDF embed element
#         # self.assertTrue(pdf_element.is_displayed())
#         # # Add more assertions or actions as needed.
