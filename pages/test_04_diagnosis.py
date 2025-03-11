import logging
logging.basicConfig(level=logging.INFO)
import time




def Diagnosis(page, car_numbers):

    # 진단 전 차량 선택
    listCar = page.get_by_text(car_number, exact=True)
    listCar.wait_for(state="visible", timeout=10000)
    listCar.click()
    logging.info(f"PASS : 예약리스트 > 차량 번호 {car_number} 클릭 성공")

    page.get_by_role("link", name="진단 대기중").click()
    logging.info(f"PASS : 진단 tab 진입 - {car_numbers}")

    page.get_by_role("link", name="성능장").click()
    page.get_by_text("기타 성능장 qa").click()
    logging.info("PASS : 진단 tab > 성능/상태 점검자 > 성능장 선택")

    page.get_by_role("link", name="평가사").click()
    page.get_by_role("textbox", name="평가사 검색").click()
    page.get_by_role("textbox", name="평가사 검색").fill("채유리")
    page.get_by_role("textbox", name="평가사 검색").press("Enter")
    page.get_by_text("채유리(10834)본사광고지원센터").click()
    logging.info("PASS : 진단 tab > 성능/상태 점검자 > 평가사 선택")

    page.get_by_role("button", name="진단 완료").click()
    logging.info("PASS : 진단 tab > 진단 완료 버튼 선택")
    time.sleep(3)
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : 진단 tab > 진단 완료 > 확인 팝업 > 확인 버튼 선택")
    time.sleep(5)



    logging.info(f"PASS : 진단 Tab 완료 - {car_numbers}")

    # 모두 완료 후 헤더 차량번호를 눌러 예약리스트로 되돌아가기
    page.get_by_text(car_numbers, exact=True).click()
    logging.info("PASS : 예약리스트 이동")
    time.sleep(2)
