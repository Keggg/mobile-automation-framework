from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from driver_setup import Context
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from logger import log_step
from models import Participant

def allow_camera_access(ctx: Context):
    driver: WebDriver = ctx.driver
    try:
        WebDriverWait(driver, timeout=2).until(EC.element_to_be_clickable((AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button'))).click()
    except (NoSuchElementException, TimeoutException):
        pass

def login(ctx: Context, user: Participant):
    wait: WebDriverWait = ctx.wait
    phone_number = user.phone_number
    password = user.password
    ctx.state["actor_name"] = user.actor_name
    phone_number_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText[@text="+7 "]')))
    phone_number_field.click()
    phone_number_field.send_keys(phone_number)
    password_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.widget.EditText[2]')))
    password_field.click()
    password_field.send_keys(password)
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

# ввод pin-code по одной цифре нажатиями
def pin_code(ctx: Context):
    wait: WebDriverWait = ctx.wait
    zero_number = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.view.View[@content-desc="0"]')))
    for i in range(8):
        zero_number.click()
    faceID_deny_btn = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button[@content-desc="Запретить"]'))).click()

def logout(ctx: Context):
    wait: WebDriverWait = ctx.wait
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Профиль\nВкладка 3 из 3'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Выйти'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Подтвердить'))).click()
    ctx.state.pop("actor_name", None)

# Подпись заявления
def sign_application(ctx: Context, application_number):
    driver: WebDriver = ctx.driver
    wait: WebDriverWait = ctx.wait
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, 'Заявление № {application_number}')]"))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.Button'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    for i in range(12):
        driver.press_keycode(7)
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Перейти в историю'))).click()

def fill_ID_card(ctx: Context):
    wait: WebDriverWait = ctx.wait
    with log_step(ctx, "Удостоверение личности 1-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение паспорта или удостоверения личности с двух сторон\n+ Добавить'))).click()
        allow_camera_access(ctx)
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Удостоверение личности 2-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение паспорта или удостоверения личности с двух сторон\n+ Добавить'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

# Заполнение данных водителя
def fill_driver_data(ctx: Context, driver_data: dict):
    driver: WebDriver = ctx.driver
    wait: WebDriverWait = ctx.wait
    iin = driver_data.get("iin")
    phone_number = driver_data.get("phone_number")
    first_name = driver_data.get("first_name")
    last_name = driver_data.get("last_name")
    middle_name = driver_data.get("middle_name")

    driver_iin_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')))
    driver_iin_field.click()
    driver_iin_field.send_keys(iin)

    driver_phone_number_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')))
    driver_phone_number_field.click()
    driver_phone_number_field.send_keys(phone_number)

    driver_first_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[3]')))
    driver_first_name_field.click()
    driver_first_name_field.send_keys(first_name)
    driver.hide_keyboard(strategy="tapOutside")

    driver_last_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[4]')))
    driver_last_name_field.click()
    driver_last_name_field.send_keys(last_name)
    driver.hide_keyboard(strategy="tapOutside")

    driver_middle_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[5]')))
    driver_middle_name_field.click()
    driver_middle_name_field.send_keys(middle_name)
    driver.hide_keyboard(strategy="tapOutside")

    with log_step(ctx, "Удостоверение личности 1-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        allow_camera_access(ctx)
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Удостоверение личности 2-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    driver.execute_script("mobile: scroll", {
    "strategy": "-android uiautomator",
    "selector": 'new UiSelector().description("+ Добавить").instance(1)',
    "direction": "down"
    })

    with log_step(ctx, "Водительское удостоверение 1-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Водительское удостоверение 2-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Тех.паспорт 1-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Тех.паспорт 2-ая фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    driver.execute_script("mobile: scroll", {
        "strategy": "accessibility id",
        "selector": "Продолжить",
        "direction": "down"
    })

    with log_step(ctx, "Путевой лист фотография"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="+ Добавить"]'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Сфотографировать'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    