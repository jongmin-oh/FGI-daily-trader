from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.config import CRAWL_URL

WAIT_TIME = 60  # 최대 대기 시간 (초)


def get_fear_greed_index() -> float:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-automation")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    )
    chrome_options.binary_location = (
        "/opt/chrome/chrome-linux64/chrome"  # Chrome 바이너리 위치 지정
    )

    # WebDriver 설정
    service = Service(
        "/opt/chromedriver/chromedriver-linux64/chromedriver"
    )  # ChromeDriver 위치 지정
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 페이지 로드
        driver.get(CRAWL_URL)

        element = WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "market-fng-gauge__dial-number-value")
            )
        )

        # 값 추출 및 반환
        value = element.text.strip()
        return float(value)

    except Exception as e:
        raise ValueError(f"Failed to find the FNG index value: {str(e)}")

    finally:
        driver.quit()  # 브라우저 종료
