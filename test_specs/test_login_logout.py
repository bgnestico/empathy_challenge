import unittest
from selenium import webdriver


class LoginLogoutTest(unittest.TestCase):

    """
    Locators
    """
    users = ["standard_user", "locked_out_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
    wrong_username = "not_a_user"
    password = "secret_sauce"
    wrong_password = "incorrect_password"
    cart = "shopping_cart_container"
    username_box = "user-name"
    password_box = "password"
    login_button = "login-button"
    burger_menu = "react-burger-menu-btn"
    logout_button = "logout_sidebar_link"
    error_message_box = "[data-test='error']"

    """
    Methods
    """

    def click_element(self, locator):
        self.driver.find_element_by_id(locator).click()

    def login(self, username, password):
        self.driver.find_element_by_id(self.username_box).send_keys(username)
        self.driver.find_element_by_id(self.password_box).send_keys(password)
        self.driver.find_element_by_id(self.login_button).click()

    def logout(self):
        self.driver.find_element_by_id(self.burger_menu).click()
        self.driver.find_element_by_id(self.logout_button).click()

    """
    Tests
    """
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="/Users/braiannestico/chromedriver")
        self.driver.get("https://www.saucedemo.com/")
        self.driver.implicitly_wait(5)

    def test_login_logout(self):

        self.login(self.users[0], self.password)
        assert self.driver.find_element_by_id(self.cart).is_displayed(), "login failed"

        self.logout()
        assert self.driver.find_element_by_id(self.login_button).is_displayed(), "logout failed"

    def test_login_locked_out_user(self):
        self.login(self.users[1], self.password)
        error_message = self.driver.find_element_by_css_selector(self.error_message_box).text
        expected_message = "Epic sadface: Sorry, this user has been locked out."
        assert expected_message == error_message, "failed to authenticate or missing error message"

    def test_login_logout_problem_user(self):

        self.login(self.users[2], self.password)
        assert self.driver.find_element_by_id(self.cart).is_displayed(), "login failed"

        self.logout()
        assert self.driver.find_element_by_id(self.login_button).is_displayed(), "logout failed"

    def test_login_performance_glitch_user(self):
        self.login(self.users[3], self.password)
        assert self.driver.find_element_by_id(self.cart).is_displayed(), "login failed"

        self.logout()
        assert self.driver.find_element_by_id(self.login_button).is_displayed(), "logout failed"

    def test_login_error_user(self):
        self.login(self.users[4], self.password)
        assert self.driver.find_element_by_id(self.cart).is_displayed(), "login failed"

        self.logout()
        assert self.driver.find_element_by_id(self.login_button).is_displayed(), "logout failed"

    def test_login_visual_user(self):
        self.login(self.users[5], self.password)
        assert self.driver.find_element_by_id(self.cart).is_displayed(), "login failed"

        self.logout()
        assert self.driver.find_element_by_id(self.login_button).is_displayed(), "logout failed"

    def test_wrong_username(self):
        self.login(self.wrong_username, self.password)
        error_message = self.driver.find_element_by_css_selector(self.error_message_box).text
        expected_message = "Epic sadface: Username and password do not match any user in this service"
        assert expected_message == error_message, "missing error message"

    def test_wrong_password(self):
        self.login(self.users[0], self.wrong_password)
        error_message = self.driver.find_element_by_css_selector(self.error_message_box).text
        expected_message = "Epic sadface: Username and password do not match any user in this service"
        assert expected_message == error_message, "missing error message"

    def test_missing_username(self):
        self.driver.find_element_by_id(self.password_box).send_keys(self.password)
        self.driver.find_element_by_id(self.login_button).click()
        error_message = self.driver.find_element_by_css_selector(self.error_message_box).text
        assert error_message == "Epic sadface: Username is required", "missing error message"

    def test_missing_password(self):
        self.driver.find_element_by_id(self.username_box).send_keys(self.users[0])
        self.driver.find_element_by_id(self.login_button).click()
        error_message = self.driver.find_element_by_css_selector(self.error_message_box).text
        assert error_message == "Epic sadface: Password is required", "missing error message"

    def tearDown(self):
        self.driver.quit()
