from .base_testcase import BaseTestCase


class TestLogin(BaseTestCase):
    """
    Test cases revolving around the logging in functionality of the site
    """
    def __init__(self, testname):
        super().__init__(testname, log_in=False)

    def test_login(self):
        """
        Test that if you attempt to go to a url when not logged in,
        you'll be taken to the login screen, and then once logged in,
        taken to that original page you had requested.
        """
        url = "/index.php?semester=" + self.semester + \
              "&course=sample&component=student&gradeable_id=open_homework&success_login=true"
        self.log_in(url, title='SAMPLE')
        self.assertEqual(self.test_url + url, self.driver.current_url)
        cookies = list(filter(lambda x: x['name'] == 'submitty_token', self.driver.get_cookies()))
        self.assertEqual(1, len(cookies))
        self.assertRegex(cookies[0]['value'], r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_bad_login_password(self):
        self.get("/index.php?semester=" + self.semester + "&course=sample")
        self.driver.find_element_by_id("login-guest")
        self.driver.find_element_by_name("user_id").send_keys(self.user_id)
        self.driver.find_element_by_name("password").send_keys("bad_password")
        self.driver.find_element_by_name("login").click()
        error = self.driver.find_element_by_id("error-0")
        self.assertEqual("Could not login using that user id or password", error.text)

    def test_bad_login_username(self):
        self.get("/index.php?semester=" + self.semester + "&course=sample")
        self.driver.find_element_by_id("login-guest")
        self.driver.find_element_by_name("user_id").send_keys("bad_username")
        self.driver.find_element_by_name("password").send_keys(self.user_password)
        self.driver.find_element_by_name("login").click()
        error = self.driver.find_element_by_id("error-0")
        self.assertEqual("Could not login using that user id or password", error.text)

    def test_login_non_course_user(self):
        self.get("/index.php?semester=" + self.semester + "&course=sample")
        self.driver.find_element_by_id("login-guest")
        self.driver.find_element_by_name("user_id").send_keys("pearsr")
        self.driver.find_element_by_name("password").send_keys("pearsr")
        self.driver.find_element_by_name("login").click()
        element = self.driver.find_element_by_class_name("content")
        self.assertEqual("You don't have access to this course.\nThis is sample for {:s}.\nIf you think this is a mistake, please contact your instructor to gain access.\nclick here to back to homepage and see your courses list.".format(self.full_semester), element.text)

if __name__ == "__main__":
    import unittest
    unittest.main()
