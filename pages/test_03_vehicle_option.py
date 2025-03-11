import logging
logging.basicConfig(level=logging.INFO)
import time
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError




def VehicleOption(page, car_number):

    # 진단 전 차량 선택
    listCar = page.get_by_text(car_number, exact=True)
    listCar.wait_for(state="visible", timeout=10000)
    listCar.click()
    logging.info(f"PASS : 예약리스트 > 차량 번호 {car_number} 클릭 성공")


    page.get_by_role("link", name="옵션").click()
    logging.info(f"PASS : 옵션 tab 진입 - {car_number}")


    # 제작일/연식 팝업
    try:
        ProductionPopup = page.get_by_role("button", name="확인")
        ProductionPopup.wait_for(state="visible", timeout=5000)
        ProductionPopup.click()
        logging.info("PASS : 옵션 tab > 제작일/연식 팝업 - 확인")
    except PlaywrightTimeoutError:
        logging.info("PASS : 옵션 tab > 제작일/연식 팝업 - 미노출")



    page.get_by_role("button", name="옵션 완료").click()
    logging.info("PASS : 옵션 tab > 옵션 완료 버튼 선택")
    time.sleep(3)
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : 옵션 tab > 옵션 완료 > 완료 팝업 > 확인 버튼 선택")
    time.sleep(5)

    logging.info(f"PASS : 옵션 Tab 완료 - {car_number}")

    # 모두 완료 후 헤더 차량번호를 눌러 예약리스트로 되돌아가기
    page.get_by_text(car_number, exact=True).click()
    logging.info("PASS : 예약리스트 이동")
    time.sleep(2)
