import logging
logging.basicConfig(level=logging.INFO)
import time
from playwright.sync_api import Playwright, sync_playwright, expect
from config import car_numbers, car_type




def Diagnosis(playwright: Playwright) -> None:
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

    page.get_by_role("link", name="변경").click()
    page.get_by_text("본사 광고지원센터").click()
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : 지점 변경")

    ## 차량번호
    for car_number in car_numbers:
        try:
            page.get_by_text(car_number, exact=True).click()
            logging.info(f"PASS : 차량 번호 {car_number} 클릭 성공")
            break  # 성공적으로 클릭했다면 루프 종료
        except:
            logging.warning(f"FAIL : 차량 번호 {car_number} 클릭 실패")

    # 모든 차량 번호에 대해 클릭을 시도했지만 실패한 경우
    else:
        logging.error("FAIL : 모든 차량 번호 클릭 시도 실패")
        # 여기에 오류 처리 로직 추가
    time.sleep(3)

    page.get_by_role("link", name="진단 대기중").click()
    logging.info("PASS : 진단 tab 진입 성공")

    page.get_by_role("link", name="성능장").click()
    page.get_by_text("기타 성능장 qa").click()
    logging.info("PASS : 성능장 선택")

    page.get_by_role("link", name="평가사").click()
    page.get_by_role("textbox", name="평가사 검색").click()
    page.get_by_role("textbox", name="평가사 검색").fill("채유리")
    page.get_by_role("textbox", name="평가사 검색").press("Enter")
    page.get_by_text("채유리(10834)본사광고지원센터").click()
    logging.info("PASS : 평가사 선택")

    page.get_by_role("button", name="진단 완료").click()
    logging.info("PASS : [진단 완료] 버튼 선택")
    time.sleep(3)
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : [확인] 버튼 선택")
    time.sleep(5)
    logging.info("PASS : 진단 Tab 완료")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    Diagnosis(playwright)
