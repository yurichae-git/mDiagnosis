import logging
logging.basicConfig(level=logging.INFO)
from playwright.sync_api import sync_playwright
from pages.test_00_login import Login
from pages.test_01_mobileDiagnosis import Reservation
#from pages.test_02_vehicle_info import VehicleInfo
#from pages.test_03_vehicle_option import VehicleOption
#from pages.test_04_diagnosis import Diagnosis


def main():
    with sync_playwright() as playwright:
        # 브라우저 및 페이지 생성
        browser = playwright.chromium.launch(headless=False, args=["--start-fullscreen"])
        context = browser.new_context(viewport={'width': 800, 'height': 1200}, device_scale_factor=2)
        page = context.new_page()

        # Login 함수 호출
        Login(page)

        # 차량 번호별 예약 처리
        from config import car_numbers  # 필요한 경우 config에서 가져오기
        for car_number in car_numbers:
            try:
                Reservation(page, car_number)
                logging.info(f"PASS : 현장예약 완료 - {car_number}")
            except Exception as e:
                logging.error(f"FAIL : 차량 번호 {car_number} 처리 중 오류 발생 - {str(e)}")

        # 브라우저 종료
        browser.close()

if __name__ == '__main__':
    main()

