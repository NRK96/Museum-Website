# from django.test import LiveServerTestCase, TestCase
# from django.urls import resolve
# from selenium import webdriver
#
# from scheduling.views import scheduling, home, contact, RequestIndex
#
# class AdminURLsTestCase(LiveServerTestCase):
#
# 	def setUp(self):
# 		self.browser = webdriver.Firefox()
# 		self.browser.implicitly_wait(2)
#
# 	def tearDown(self):
# 		self.browser.quit()
#
# 	def test_admin(self):
#
# 		# Check to see if the admin page is accessible
# 		response = self.client.get('/admin/login/')
# 		self.assertEqual(response.status_code, 200)
#
# 	def test_admin_login(self):
# 		"""
# 		Test that we are able to login using the assigned credentials
# 		to the admin page
# 		"""
#
# 		self.browser.get('%s%s' % (self.live_server_url, '/admin/login/'))
#
# 		# Input Username and Password
# 		username_input = self.browser.find_element_by_id("id_username")
# 		username_input.send_keys('Woogity')
# 		password_input = self.browser.find_element_by_id("id_password")
# 		password_input.send_keys('shoreshack')
#
# 		# Click "Log in" button
# 		self.browser.find_element_by_xpath('//input[@value="Log in"]').click()
#
# class HomeURLTestCase(TestCase):
#
# 	def test_root_url_uses_home_view(self):
# 		root = resolve('/')
# 		self.assertEqual(root.func, home)
#
# class ContactURLTestCase(TestCase):
#
# 	def test_contact_url_uses_contact_view(self):
# 		root = resolve('/contact/')
# 		self.assertEqual(root.func, contact)
#
# class ScheduleURLTestCase(TestCase):
#
#     def test_schedule_url_uses_schedule_view(self):
#         root = resolve('/scheduling/')
#         self.assertEqual(root.func, scheduling)
#
