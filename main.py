import logging
logging.basicConfig(level=logging.INFO)
from playwright.sync_api import sync_playwright
from pages.test_00_login import Login
from pages.test_01_reservation import Reservation
from pages.test_02_vehicle_info import VehicleInfo
from pages.test_03_vehicle_option import VehicleOption
from pages.test_04_diagnosis import Diagnosis


def main():
    with sync_playwright() as playwright:

        browser = playwright.chromium.launch(headless=False, args=["--start-fullscreen"])
        context = browser.new_context(viewport={'width': 800, 'height': 1200}, device_scale_factor=2)
        page = context.new_page()

        Login(page)


        from config import car_numbers
        for car_number in car_numbers:
            try:
                Reservation(page, car_number)
                VehicleInfo(page, car_number)
                VehicleOption(page, car_number)
                Diagnosis(page, car_number)


            except Exception as e:
                logging.error(f"FAIL : 차량 번호 {car_number} 처리 중 오류 발생 - {str(e)}")

        browser.close()

if __name__ == '__main__':
    main()

