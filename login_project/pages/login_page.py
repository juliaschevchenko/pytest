class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("input#username")
        self.password_input = page.locator("input#password")
        self.login_button = page.locator("button#submit")

    def goto(self):
        self.page.goto("https://practicetestautomation.com/practice-test-login/")

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
