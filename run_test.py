from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import re
from helpers import allow_camera_access, login, pin_code, logout, sign_application, fill_driver_data, fill_ID_card
from driver_setup import Context
from participants import create_participants, drivers_data
from logger import setup_logger, rename_log_file, log_step, log_test_case_info
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def run_test(ctx: Context, test_case: str):
    setup_logger()
    driver: WebDriver = ctx.driver
    wait: WebDriverWait = ctx.wait
    applicant, contender, settlement_type = create_participants(test_case)
    log_test_case_info(test_case, applicant, contender, settlement_type)

    with log_step(ctx, "Разрешение на получение уведомлений"):
        try:
            WebDriverWait(driver, timeout=2).until(EC.element_to_be_clickable((AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_button'))).click()
        except (NoSuchElementException, TimeoutException):
            pass

    with log_step(ctx, "Авторизация заявителя"):
        login(ctx, applicant)

    with log_step(ctx, "Пин-код"):
        pin_code(ctx)

    with log_step(ctx, "Создание заявки"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Заявление\nВкладка 2 из 3'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Европротокол\nОформление ДТП онлайн без вызова полиции'))).click()

    with log_step(ctx, "Разрешение на получение геолокации"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button'))).click()

    if applicant.type == "individual":
        with log_step(ctx, "Вы являетесь (физ.лицом)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Физическим лицом'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Укажите ГРНЗ"):
            applicant_grnz_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText')))
            applicant_grnz_field.click()
            applicant_grnz_field.send_keys(applicant.grnz)
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    elif applicant.type == "entity":
        with log_step(ctx, "Вы являетесь (юр.лицом)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Юридическим лицом'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Укажите ГРНЗ и БИН"):
            applicant_entity_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')))
            applicant_entity_name_field.click()
            applicant_entity_name_field.send_keys('ТОО "Тест1"')

            applicant_bin_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')))
            applicant_bin_field.click()
            applicant_bin_field.send_keys(applicant.company.bin)

            applicant_grnz_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[3]')))
            applicant_grnz_field.click()
            applicant_grnz_field.send_keys(applicant.company.entity_grnz)
            driver.hide_keyboard(strategy="tapOutside")

            applicant_entity_doc_number_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[4]')))
            applicant_entity_doc_number_field.click()
            applicant_entity_doc_number_field.send_keys('111111')
            driver.hide_keyboard(strategy="tapOutside")

            driver.execute_script("mobile: scroll", {
                "strategy": "accessibility id",
                "selector": "Продолжить",
                "direction": "down"
            })

            with log_step(ctx, "Путевой лист - фотография"):
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, '+ Добавить'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Сфотографировать'))).click()
                allow_camera_access(ctx)
                wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Общие вопросы для оформления Европротокола"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да\nВ ДТП участвовали 2 транспортных средства'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да\nОба участника находятся в трезвом состоянии'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да\nОба участника находятся на месте ДТП'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Нет\nНикому не причинен вред здоровью'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Нет\nНе причинен вред окружающей среде или инфраструктуре'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    if applicant.role == "defendant":
        with log_step(ctx, "Вы являетесь (виновным)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Виновным'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    elif applicant.role == "victim":
        with log_step(ctx, "Вы являетесь (пострадавшим)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Пострадавшим'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        
        with log_step(ctx, "Сумма ущерба"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да\nСумма ущерба менее 100 МРП'))).click()
            damage_cost = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText')))
            damage_cost.click()
            damage_cost.send_keys(345000)
            driver.hide_keyboard(strategy="tapOutside")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Выберите тип урегулирования"):
            if settlement_type == "standard":
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Стандартный тип')]"))).click()
            elif settlement_type == "direct":
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Прямой тип')]"))).click()    
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    if contender.type == "individual":
        with log_step(ctx, "Вторая сторона является (Физ.лицом)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Физическим лицом'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
            
        with log_step(ctx, "Укажите данные виновной стороны"):
            contender_iin_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')))
            contender_iin_field.click()
            contender_iin_field.send_keys(contender.iin)

            contender_grnz_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')))
            contender_grnz_field.click()
            contender_grnz_field.send_keys(contender.grnz)
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
            
    elif contender.type == "entity":
        with log_step(ctx, "Вторая сторона является (Юр.лицом)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Юридическим лицом'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Укажите данные виновной стороны"):
            contender_iin_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')))
            contender_iin_field.click()
            contender_iin_field.send_keys(contender.iin)

            contender_grnz_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')))
            contender_grnz_field.click()
            contender_grnz_field.send_keys(contender.company.entity_grnz)
            driver.hide_keyboard(strategy="tapOutside")

            contender_bin_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')))
            contender_bin_field.click()
            contender_bin_field.send_keys(contender.company.bin)
            driver.hide_keyboard(strategy="tapOutside")

            contender_entity_name_field = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(3)')))
            contender_entity_name_field.click()
            contender_entity_name_field.send_keys('ТОО "Тест2"')
            driver.hide_keyboard(strategy="tapOutside")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
        
    # Транспортным средством управляли Вы?
    if applicant.has_driver == False:
        with log_step(ctx, "Транспортным средством управляли Вы? (Да)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Сфотографируйте свои документы"):
            fill_ID_card(ctx)

            with log_step(ctx, "Водительское удостоверение 1-ая фотография"):
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображения водительского удостоверения с двух сторон\n+ Добавить'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            with log_step(ctx, "Водительское удостоверение 2-ая фотография"):
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображения водительского удостоверения с двух сторон\n+ Добавить'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
            
            driver.execute_script("mobile: scroll", {
                "strategy": "accessibility id",
                "selector": "Продолжить",
                "direction": "down"
            })

            with log_step(ctx, "Тех.паспорт 1-ая фотография"):
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение тех.паспорта с двух сторон\n+ Добавить'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            with log_step(ctx, "Тех.паспорт 2-ая фотография"):
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение тех.паспорта с двух сторон\n+ Добавить'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
                wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    elif applicant.has_driver == True:
        with log_step(ctx, "Транспортным средством управляли Вы? (Нет)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Нет'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Введите данные водителя"):
            fill_driver_data(ctx, drivers_data["applicant_driver"])

        with log_step(ctx, "Сфотографируйте свои документы"):
            fill_ID_card(ctx)

    with log_step(ctx, "Заполнение местоположения"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.EditText'))) # ждем подтягивания местоположения
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "окошко 'Безопасность на первом месте'"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ImageView')))
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Сделайте фотографии Вашего транспортного средства с ГРНЗ"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.ImageView[1]'))).click() # передняя сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.ImageView[2]'))).click() # левая сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.ImageView[4]'))).click() # правая сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.ImageView[5]'))).click() # задняя сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Тип транспортного средства"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Легковое авто",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Легковое авто'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Выберите пострадавшие стороны"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Левая сторона'))).click()
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Выберите поврежденную часть ТС"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Левая часть ТС'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Опишите обстоятельства ДТП"):
        applicant_сircumstances_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText')))
        applicant_сircumstances_field.click()
        applicant_сircumstances_field.send_keys("Обстоятельства заявителя")
        driver.hide_keyboard(strategy="tapOutside")
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Заполните данные Вашего транспортного средства"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        applicant_vincode_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')))
        applicant_vincode_field.click()
        applicant_vincode_field.send_keys("VINCODE001")

        applicant_mileage_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')))
        applicant_mileage_field.click()
        applicant_mileage_field.send_keys("51000")
        driver.hide_keyboard(strategy="tapOutside")

        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click() # фото пробега
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, '+ Добавить'))).click() # фото VIN кода
        wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Сфотографировать'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение окружающей среды.\n+ Добавить'))).click() # фото схема ДТП
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте фотографию или видеосьемку общего плана ДТП.\n+ Добавить'))).click() # фото общий план ДТП
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Проверьте данные заявления"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Подтвердить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Подтвердить'))).click()

    with log_step(ctx, "Получение номера заявления"):
        application_number = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Заявление №')]")))
        application_number = application_number.get_attribute("contentDescription")
        application_number = re.search(r'Заявление\s*№ \s*(\d+)', application_number)
        application_number = application_number.group(1)
    ctx.state["application_number"] = application_number
    rename_log_file(application_number, test_case)

    with log_step(ctx, "Выход с аккаунта"):
        logout(ctx)

    with log_step(ctx, "Авторизация второй стороны"): 
        login(ctx, contender)

    with log_step(ctx, "Пин-код"):
        pin_code(ctx)

    with log_step(ctx, "Вход в заявку"):
        wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, 'Заявление № {application_number}')]"))).click()

    with log_step(ctx, "Проверьте данные заявления"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    if contender.has_driver == False:
        with log_step(ctx, "Транспортным средством управляли Вы? (Да)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Сфотографируйте свои документы"):
            fill_ID_card(ctx)

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображения водительского удостоверения с двух сторон\n+ Добавить'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображения водительского удостоверения с двух сторон\n+ Добавить'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            driver.execute_script("mobile: scroll", {
                "strategy": "accessibility id",
                "selector": "Продолжить",
                "direction": "down"
            })
            
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение тех.паспорта с двух сторон\n+ Добавить'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение тех.паспорта с двух сторон\n+ Добавить'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    elif contender.has_driver == True:
        with log_step(ctx, "Транспортным средством управляли Вы? (Нет)"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Нет'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Введите данные водителя"):
            fill_driver_data(ctx, drivers_data["contender_driver"])

        with log_step(ctx, "Сфотографируйте свои документы"):
            fill_ID_card(ctx)


    if applicant.role == 'defendant': # В случае если вторая сторона пострадавшая
        with log_step(ctx, "Сумма ущерба"):
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Да\nСумма ущерба менее 100 МРП'))).click()
            damage_cost = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText')))
            damage_cost.click()
            damage_cost.send_keys("345000")
            driver.hide_keyboard(strategy="tapOutside")
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        with log_step(ctx, "Тип урегулирования"):
            if settlement_type == "standard":
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Стандартный тип')]"))).click()
            elif settlement_type == "direct":
                wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[contains(@content-desc, 'Прямой тип')]"))).click()    
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "окошко 'Безопасность на первом месте'"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ImageView')))
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Сделайте фотографии транспортного средства"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)'))).click() # передняя сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(1)'))).click() # левая сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(3)'))).click() # правая сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(4)'))).click() # задняя сторона
        wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Тип транспортного средства"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Легковое авто'))).click()
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Выберите пострадавшие стороны"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Передняя сторона'))).click()
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Продолжить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Выберите области повреждения"):
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Передняя часть ТС'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Опишите обстоятельства ДТП"):
        wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))) # чтобы раньше времени не нажал на поле
        applicant_сircumstances_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.EditText')))
        applicant_сircumstances_field.click()
        applicant_сircumstances_field.send_keys("Обстоятельства второй стороны")
        driver.hide_keyboard(strategy="tapOutside")
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    if applicant.role == "defendant":
        with log_step(ctx, "Заполните данные транспортного средства (как пострадавший)"):
            contender_mileage_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')))
            contender_mileage_field.click()
            contender_mileage_field.send_keys("52000")

            contender_vincode_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')))
            contender_vincode_field.click()
            contender_vincode_field.send_keys("VINCODE002")
            driver.hide_keyboard(strategy="tapOutside")

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение VIN кода\n+ Добавить'))).click() # фото VIN кода
            wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, 'Сфотографировать'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Добавьте изображение показаний одометра\n+ Добавить'))).click() # фото пробега
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(10)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            driver.execute_script("mobile: scroll", {
                "strategy": "accessibility id",
                "selector": "Продолжить",
                "direction": "down"
            })

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
    elif applicant.role == "victim":
        with log_step(ctx, "Заполните данные транспортного средства (как виновный)"):
            contender_mileage_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[1]')))
            contender_mileage_field.click()
            contender_mileage_field.send_keys("52000")

            contender_vincode_field = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '//android.widget.ScrollView/android.widget.EditText[2]')))
            contender_vincode_field.click()
            contender_vincode_field.send_keys("VINCODE002")
            driver.hide_keyboard(strategy="tapOutside")

            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click() # общее фото
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, '+ Добавить'))).click() # фото VIN кода
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Сфотографировать'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()
            
            driver.execute_script("mobile: scroll", {
                "strategy": "accessibility id",
                "selector": "Продолжить",
                "direction": "down"
            })

            wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, '(//android.widget.ImageView[@content-desc="+ Добавить"])[1]'))).click() # окружающая среда
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, '+ Добавить'))).click() # Фото пробега
            wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(9)'))).click()
            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

            wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Продолжить'))).click()

    with log_step(ctx, "Проверьте данные заявления"):
        wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'android.widget.ScrollView')))
        driver.execute_script("mobile: scroll", {
            "strategy": "accessibility id",
            "selector": "Подтвердить",
            "direction": "down"
        })
        wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Подтвердить'))).click()

    # Выход со второго аккаунта и вход под первым аккаунтом для подписания
    with log_step(ctx, "Выход с аккаунта"):
        logout(ctx)

    with log_step(ctx, "Авторизация заявителя для подписания"):
        login(ctx, applicant)

    with log_step(ctx, "Пин-код"):
        pin_code(ctx)

    with log_step(ctx, "Этап подписания"):
        sign_application(ctx, application_number)

    # Выход со первого аккаунта и вход под вторым аккаунтом для подписания
    with log_step(ctx, "Выход с аккаунта"):
        logout(ctx)

    # with log_step(ctx, "Авторизация второй стороны для подписания"):
    #     login(ctx, contender)

    # with log_step(ctx, "Пин-код"):
    #     pin_code(ctx)

    # with log_step(ctx, "Этап подписания"):
    #     sign_application(ctx, application_number)

    # with log_step(ctx, "Выход с аккаунта"):
    #     logout(ctx)