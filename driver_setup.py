from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from appium.options.android import UiAutomator2Options

class Context:
    def __init__(self, driver: WebDriver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait
        self.state = {}

def start_driver():
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Android',
        appPackage='com.insurance.app.stg',
        appActivity='com.insurance.app.MainActivity',
        language='ru',
        newCommandTimeout=900
    )

    appium_server_url = 'http://localhost:4723'
    capabilities_options = UiAutomator2Options().load_capabilities(capabilities)

    driver = webdriver.Remote(command_executor=appium_server_url,options=capabilities_options)
    #driver.implicitly_wait(10)
    wait = WebDriverWait(driver, timeout=10)

    return Context(driver, wait)

