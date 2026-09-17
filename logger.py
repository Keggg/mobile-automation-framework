from contextlib import contextmanager
import logging
from datetime import datetime
import os
from driver_setup import Context
from appium.webdriver.webdriver import WebDriver
from models import Participant

log_file = 'app_temp.log'
log_dir = 'logs'

def setup_logger():
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_file)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def rename_log_file(application_number: str, test_case: str):
    logging.shutdown()

    old_path = os.path.join(log_dir, log_file)
    new_name = f"{application_number}_{test_case}.log"
    new_path = os.path.join(log_dir, new_name)

    if os.path.exists(old_path):
        os.rename(old_path, new_path)
    else:
        raise FileNotFoundError(f"Лог-файл {old_path} не найден для переименования")

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    file_handler = logging.FileHandler(new_path, encoding='utf-8')
    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[file_handler, stream_handler]
    )

def log_test_case_info(test_case_name: str, applicant: Participant, contender: Participant, settlement_type: str):
    logging.info("=" * 60)
    logging.info(f"▶️ Тест-кейс: {test_case_name}")
    logging.info(f"🟦 Applicant: type={applicant.type}, phone={applicant.phone_number}, driver={applicant.has_driver}, role={applicant.role}")
    logging.info(f"🟥 Contender: type={contender.type}, phone={contender.phone_number}, driver={contender.has_driver}")
    logging.info(f"🟨 Settlement Type: {settlement_type}")
    logging.info("=" * 60)

@contextmanager
def log_step(ctx: Context, step_name: str):
    actor_name = ctx.state.get("actor_name", None)
    prefix = f"[{actor_name}] " if actor_name else ""
    logging.info(f"🔷 {prefix}Начало шага: {step_name}")
    try:
        yield
        logging.info(f"✅ {prefix}Шаг '{step_name}' выполнен успешно")
    except Exception as e:
        logging.error(f"❌ {prefix}Ошибка в шаге '{step_name}': {e}")
        try:
            driver: WebDriver = ctx.driver
            application_number = ctx.state.get("application_number")
            screenshot_dir = 'screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)

            actor_tag = actor_name.replace(" ", "_") if actor_name else "no_actor"
            safe_name = step_name.replace(" ", "_").replace("'", "")
            if application_number:
                screenshot_path = os.path.join(
                    screenshot_dir,
                    f"{application_number}_{actor_tag}_{safe_name}.png"
                )
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                screenshot_path = os.path.join(
                    screenshot_dir,
                    f"{timestamp}_{actor_tag}_{safe_name}.png"
                )

            driver.get_screenshot_as_file(screenshot_path)
            logging.error(f"📸 Скриншот сохранён: {screenshot_path}")
        except Exception as screenshot_error:
            logging.error(f"❌ Ошибка при создании скриншота: {screenshot_error}")
        raise

