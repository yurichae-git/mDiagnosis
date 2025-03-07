# 작업 1 : 브라우저, 콘텐트, 페이지, url, 지점변경 까지 옮기기
# 작업 2 : 다른 페이지에 import 함수 호출
# 작업 3 : 다른 페이지에 browser.close 제거하고 예약리스트로 가는 동작 추가 처리
# 작업 4 : main.py browser.close 처리



import logging
logging.basicConfig(level=logging.INFO)
import time, re, random
from playwright.sync_api import Playwright, sync_playwright, expect
from config import car_numbers, car_type, owner, dealer_id





def process_reservation(page, car_numbers):

    page.get_by_role("link", name="현장 예약").click()
    logging.info("PASS : 현장예약 진입")

    page.get_by_text("이름 조회아이디 조회").click()
    page.get_by_role("textbox", name="아이디").click()
    page.get_by_role("textbox", name="아이디").fill(dealer_id)
    page.locator("#btnSearch").click()
    logging.info("PASS : 제휴딜러 조회")
    time.sleep(3)


    ##국산/수입/화물 선택
    page.get_by_text(car_type, exact=True).click()
    logging.info("PASS : 국산/수입 선택 ")

    page.get_by_role("textbox", name="차량번호").click()
    page.get_by_role("textbox", name="차량번호").fill(car_numbers)
    logging.info("PASS : 차량번호 입력")

    page.get_by_label("소유자명").select_option("직접입력")

    page.get_by_role("textbox", name="소유자명 입력").click()
    page.get_by_role("textbox", name="소유자명 입력").fill(owner)
    logging.info("PASS : 소유자명 입력")

    page.locator("div").filter(has_text=re.compile(r"^조회$")).get_by_role("button").click()
    logging.info(f"PASS : 차량정보 조회 완료 : {car_numbers}")
    time.sleep(15)

    # 제조사/모델 조회 실패 케이스

    manufacturer = page.get_by_label("제조사", exact=True)
    detail_model = page.get_by_label("세부모델", exact=True)
    if manufacturer.count() > 0:
        # 현재 선택된 제조사 옵션 확인
        selected_manufacturer = manufacturer.evaluate("el => el.options[el.selectedIndex].text")
        selected_detail_model = detail_model.evaluate("el => el.options[el.selectedIndex].text")
        if selected_manufacturer and selected_manufacturer != "제조사":
            if selected_detail_model and selected_detail_model == "세부모델":
                # 세부모델이 조회 된 경우 옵션 리스트를 가져와서 첫번째 옵션을 선택하고, 없을 땐 에러로그
                options = detail_model.evaluate("el => Array.from(el.options).map(o => o.value)")
                if options and len(options) > 0:
                    detail_model.select_option(options[0])
                    logging.info(f"PASS : 세부모델 조회 안된 경우 - 첫 번째 옵션 '{options[0]}' 선택")
                else:
                    logging.warning("PASS : 세부모델 옵션이 없음")
            logging.info(f"PASS : 제조사 / 모델 조회 성공 - {selected_manufacturer}")
        else:
            if car_type == "국산":
                logging.info("PASS : 제조사 / 모델 미확인 차량")
                page.get_by_label("제조사").select_option("현대")
                logging.info("PASS : 제조사 선택 - 현대")
                time.sleep(1)
                page.get_by_label("모델", exact=True).select_option("베뉴")
                logging.info("PASS : 모델 선택 - 베뉴")
                time.sleep(1)
                page.get_by_label("세부모델").select_option("베뉴(19년~현재)")
                logging.info("PASS : 세부모델 선택 - 베뉴(19년~현재)")
                time.sleep(1)
            elif car_type == "수입":
                logging.info("PASS : 제조사 / 모델 미확인 차량")
                page.get_by_label("제조사").select_option("BMW")
                logging.info("PASS : 제조사 선택 - BMW")
                time.sleep(1)
                page.get_by_label("모델", exact=True).select_option("7시리즈")
                logging.info("PASS : 모델 선택 - 7시리즈")
                time.sleep(1)
                page.get_by_label("세부모델").select_option("7시리즈 (G70)(22년~현재)")
                logging.info("PASS : 세부모델 선택 - 7시리즈 (G70)(22년~현재)")
                time.sleep(1)
            else:
                logging.info("FAIL : 차량유형이 국산/수입이 아님")
    else:
        logging.info("FAIL : 제조사 요소 확인 불가")


    page.get_by_text("진단등록").click()
    logging.info("PASS : 상품 - 진단등록 선택")
    page.get_by_text("홈서비스 광고이용권").click()
    logging.info("PASS : 상품 - 홈서비스 광고이용권 선택")




    page.get_by_role("button", name="등록", exact=True).click()
    logging.info("PASS : [등록] 버튼 선택")
    time.sleep(3)

    confirmPopup = page.get_by_role("button", name="확인")
    confirmPopup.wait_for(state="visible", timeout=5000)
    if confirmPopup.count() > 0 :
        confirmPopup.click()
        logging.info("PASS : [확인] 버튼 선택")
    else :
        logging.info("FAIL : 확인 팝업 미노출")
##        page.goto("https://tdiag.encar.io/revList/155?tab=0&inpCarNo=3902&page=1")
    time.sleep(5)






def Reservation(playwright: Playwright) -> None:
    ''' browser = playwright.chromium.launch(headless=False)
                            context = browser.new_context()
                        '''
    browser = playwright.chromium.launch(
        headless=False,  # GUI 모드
        args=["--start-fullscreen"]  # 전체 화면 모드
    )
    ##iphone_12 = playwright.devices['iPhone 12']
    # 페이지 생성 및 모바일 환경 설정
    context = browser.new_context(
        viewport={'width': 800, 'height': 1200},
        device_scale_factor=2
    )

    page = context.new_page()

    page.goto("https://tdiag.encar.io/dev_login")
    page.get_by_role("link", name="로그인").click()
    logging.info("PASS : 로그인")

    page.get_by_role("button", name="확장메뉴열기").click()
    page.get_by_role("link", name="지점 변경").click()
    page.get_by_role("button", name="서울").click()
    page.get_by_text("본사 광고지원센터").click()
    page.get_by_role("button", name="저장").click()
    logging.info("PASS : 지점 변경")

    for car_number in car_numbers:
        try:
            process_reservation(page, car_number)
            logging.info(f"PASS : 현장예약 완료 {car_number}")
        except Exception as e:
            logging.error(f"FAIL : 차량 번호 {car_number} 처리 중 오류 발생 - {str(e)}")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    Reservation(playwright)
