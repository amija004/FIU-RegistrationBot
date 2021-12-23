import time
from datetime import datetime
from threading import Thread
import typer

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


#def pause(until: datetime):
#    """block until a specified datetime
#
#    Args:
#        until (datetime): the time at which to resume program execution
#    """
#    while True:
#        diff = until - datetime.now()
#        if diff.total_seconds() > 0:
#            time.sleep(diff.total_seconds() / 2)
#        else:
#            break


class Enroller:
    def __init__(
        self,
        #enroll_time,
        #start_time,
        #profile,
        term,
        username: str,
        password: str,
        base_url: str,
        browser,
        opts,
        headless=False,
        size=(1920, 1080),
        verbose=False,
        test=False,
    ):
        self.driver = self._browser_init(
            Browser=browser, Options=opts, 
            #Profile=profile, 
            headless=headless, size=size
        )
        #self.start_time = start_time
        #self.enroll_time = enroll_time
        #self.profile = profile
        self.term = term
        self.thread = Thread(target=self.register)
        self.headless = headless
        self.verbose = verbose
        self.test = test
        self.base_url = base_url
        self.username = username
        self.password = password

    def _browser_init(self, Browser, Options, 
        #Profile, 
        headless=False, size=(1920, 1080)):
        options = Options()
        options.add_argument("-headless")
        driver = Browser(
            #firefox_profile=Profile, 
            options=options)
        if headless:
            driver.set_window_size(size[0], size[1])
        return driver

    def log(self, msg, debug=True):
        if self.headless or self.verbose or not debug:
            print(f"{self.thread.name}: {msg}")

    def register(self):
        # wait until 15 minutes before registration to start the browser
        #self.log(f"Waiting to begin until {self.start_time}")
        #pause(self.start_time)
        added = False
        # log in
        self.authenticate()
        while not added:
            # navigate to the shopping cart
            self.open_cart()     
            # Select and enroll in classes   
            self.enroll()                    
        # clean up stray processes
        if self.headless:
            self.cleanup()

    def authenticate(self):
        # setup the web self.driver
        self.log("Loading FIU page")
        self.driver.get(self.base_url)
        # wait for the login screen to load
        time.sleep(10)

        self.driver.get("https://mycs.fiu.edu/psc/stdnt/EMPLOYEE/CAMP/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL?")
        time.sleep(5)

        self.log("Entering credentials")
        # enter username & password
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name("password").send_keys(self.password)

        # click login
        self.log("Logging in")
        self.driver.find_element_by_name("submit").click()
        time.sleep(5)

        try:
            self.log("Clicking remember user")
            self.driver.find_element_by_id("rememberLabel").click()
            self.log("Completing Two Factor Authentication")
            time.sleep(1)
            self.log("Calling user")
            self.driver.find_element_by_id("call").click()
            time.sleep(30)
        except BaseException:
            pass

        self.log("Opening Manage Classes")
        self.driver.find_element_by_id("PTNUI_LAND_REC14$0_row_7").click()
        time.sleep(5)

    def open_cart(self):
        self.log("Opening shopping cart.")
        try:
            self.driver.find_element_by_link_text("Shopping Cart").click()
        except BaseException:
            # Expand Enrollment dropdown menu
            self.driver.find_element_by_link_text("Enrollment").click()
            time.sleep(1)
            self.driver.find_element_by_link_text("Shopping Cart").click()
        time.sleep(3)
        try:
            self.driver.find_element_by_link_text(self.term).click()
            time.sleep(5)
        except BaseException:
            pass

    def enroll(self):
        try:
            self.log("Selecting courses...")
            # Select all courses in shopping cart
            chkboxes = self.driver.find_elements_by_class_name("ps-checkbox")
            for c in chkboxes:
                c.click()
            self.log("Selected {} courses".format(len(chkboxes)))

            # self.driver.save_screenshot("preenroll_{}.png".format(self.enroll_time))

            self.log("Clicking enroll.")
            self.driver.find_element_by_id("DERIVED_SSR_FL_SSR_ENROLL_FL").click()
        except BaseException:
            print("No courses in shopping cart. Terminating script.")
            added = True

        self.log("Confirming enrollment")
        time.sleep(1)
        try:
            self.driver.find_element(By.ID, "#ICYes").click()
            self.log(f"Enroll request sent at {datetime.now()}, screenshot saved", debug=False)
            time.sleep(3)
            self.driver.save_screenshot(f"enroll_attempt{datetime.now()}.png")
            self.log("If classes still in cart, will try again in 6 minutes")
        except BaseException:
            self.log("Couldn't confirm, screenshot saved, will retry in 6 minutes")
            self.driver.save_screenshot(f"enroll_fail{datetime.now()}.png")
        
        time.sleep(360)

        #time.sleep(10)
        #if self.headless:
        #    self.driver.save_screenshot(f"confirm_page_{self.enroll_time}.png")

    def cleanup(self):
        if self.headless:
            self.driver.quit()
        exit(0)