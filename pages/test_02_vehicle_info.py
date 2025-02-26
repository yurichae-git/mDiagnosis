import logging
logging.basicConfig(level=logging.INFO)
import time
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from config import car_numbers, car_type



def VehicleInfo(playwright: Playwright) -> None:
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



    page.get_by_role("link", name="차량정보").click()
##    page.get_by_role("tab", name="차량정보", exact=False).click(force=True)
    time.sleep(3)
    logging.info("PASS : 차량정보 tab 진입 성공")

    ##차대번호 없는경우, 반절 있는 경우 입력하기
    '''try:
        # "차대번호(선택)" 텍스트박스 찾기
        vin_input = page.get_by_role("textbox", name="차대번호(선택)")

        if vin_input.count() > 0:
            vin_input.click()
            vin_input.fill("KMHK3816ZZZZZZZZZ")
            logging.info("PASS : 차대번호 입력 - 빈칸 입력")
        else:
            # "차대번호(선택)"이 없는 경우, 대체 입력 필드 찾기
            alternative_input = page.locator("input#vehicleIdNo[name='vehicleIdNo'][placeholder='차대번호 입력']")
            alternative_input.click()
            alternative_input.fill("KMHK3816ZZZZZZZZZ")
            logging.info("PASS : 차대번호 입력 - 값 있는 경우 입력")
    except Exception as e:
        logging.error(f"FAIL : 차대번호 입력 중 오류 발생: {str(e)}")'''

    page.locator("input#vehicleIdNo[name='vehicleIdNo'][placeholder='차대번호 입력']").click()
    page.locator("input#vehicleIdNo[name='vehicleIdNo'][placeholder='차대번호 입력']").fill("KMHK3816ZZZZZZZZZ")
    logging.info("PASS : 차대번호 입력")

    ## 차대번호 확인버튼 노출유무 예외처리
    identification_number_button = page.get_by_role("button", name="확인")
    if identification_number_button.count() > 0:
        identification_number_button.click()
        logging.info("PASS : 차대번호 입력 - 확인 버튼 선택")
    else:
        logging.info("PASS : 차대번호 입력 - 확인 버튼 미노출")


    # 연식
    try:
        year = page.get_by_role("spinbutton", name="연식")
        if year.count() > 0:
            current_value = year.input_value()
            if current_value and current_value != "yyyymm":
                logging.info(f"PASS: 연식 값이 있음: {current_value}")
            else:
                year.fill("201901")
                logging.info("PASS: 연식 '201901' 입력 완료")
        else:
            logging.info("PASS: 연식 요소를 찾을 수 없음")
    except Exception as e:
        logging.error(f"FAIL: 연식 요소 처리 중 오류 발생: {str(e)}")

    # 형식년도
    try:
        formalYear = page.get_by_role("spinbutton", name="형식년도")
        if formalYear.count() > 0:
            current_value = formalYear.input_value()
            if current_value and current_value != "yyyy":
                logging.info(f"PASS: 형식년도 값이 있음: {current_value}")
            else:
                formalYear.fill("2019")
                logging.info("PASS: 형식년도 '2019' 입력 완료")
        else:
            logging.info("PASS: 형식년도 요소를 찾을 수 없음")
    except Exception as e:
        logging.error(f"FAIL: 형식년도 요소 처리 중 오류 발생: {str(e)}")



    # 등급/세부등급 - 진입(연식/형식년도 없으면 진입 불가함)
    page.get_by_role("link", name="등급/세부등급 선택").click()
    logging.info("PASS : 등급/세부등급 선택 진입")


    ## 등급/세부등급 - 진입 시 팝업 뜨는 케이스 예외처리
    try:
        # 팝업이 나타날 때까지 최대 5초 대기
        notiPopup = page.get_by_role("button", name="확인")
        notiPopup.wait_for(state="visible", timeout=5000)

        # 팝업이 나타나면 클릭
        notiPopup.click()
        logging.info("PASS : 주의사항 팝업 확인")
    except PlaywrightTimeoutError:
        logging.info("PASS : 주의사항 팝업 미노출")

    page.get_by_role("button", name="직접 선택").click()
    logging.info("PASS : 직접 선택 진입")
    page.once("dialog", lambda dialog: dialog.dismiss())


    ## 등급X 첫번째 옵션 / 등급O 첫번째 옵션 선택 / 에러 발생 시 로그
    try:
        grade_select = page.get_by_label("등급", exact=True)
        grade_select.wait_for(state="visible", timeout=5000)
        if grade_select.count() > 0:
            grade_select.select_option("001")
            logging.info("PASS : '등급' 옵션 선택 완료")
        else:
            logging.info("PASS : '등급' 이 선택된 상태")
    except Exception as e:
        logging.error(f"FAIL : '등급' 옵션 선택 중 오류 발생: {str(e)}")



    ##  page.get_by_label("세부등급").select_option("001") ## 라벨이름이 세부등ㅇ급이 아니면 로그만 남기기
    try:
        grade_detail_select = page.get_by_label("세부등급", exact=True)
        if grade_detail_select.count() > 0:
            # select 요소의 옵션 개수 확인
            options_count = grade_detail_select.evaluate("el => el.options.length")
            if options_count > 1:  # 첫 번째 옵션(보통 "선택" 등)을 제외하고 옵션이 있는지 확인
                grade_detail_select.select_option("001")
                logging.info("PASS : '세부등급' 옵션 선택 완료 (001)")
            else:
                logging.info("PASS : '세부등급' 선택할 수 있는 옵션이 없음")
        else:
            logging.info("PASS : '세부등급' 요소를 찾을 수 없음")
    except Exception as e:
        logging.error(f"FAIL : '세부등급' 옵션 선택 중 오류 발생: {str(e)}")


    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="저장").click()
    logging.info("PASS : 등급/세부등급 저장")

    page.get_by_role("spinbutton", name="판매가격").click()
    page.get_by_role("spinbutton", name="판매가격").fill("3333")
    logging.info("PASS : 판매가격 입력")

    page.get_by_label("연료").select_option("가솔린")
    logging.info("PASS : 연료 선택")

    page.get_by_role("spinbutton", name="배기량").click()
    page.get_by_role("spinbutton", name="배기량").fill("2999")
    logging.info("PASS : 배기량 입략")

    page.get_by_label("포토존 색상").select_option("WHITE")
    logging.info("PASS : 포토존 색상 선택")

    page.get_by_role("listitem").filter(has_text="화이트").get_by_role("link").click()
    page.get_by_text("은색투톤").click()
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : 외관 색상 선택")

    page.get_by_label("변속기").select_option("오토")
    logging.info("PASS : 변속기 선택")

    page.get_by_role("link", name="선택").click()
    page.locator("label").filter(has_text="빨간색").click()
    page.get_by_role("button", name="확인").click()
    logging.info("PASS : 시트 색상 선택")

    page.get_by_role("spinbutton", name="주행거리").click()
    page.get_by_role("spinbutton", name="주행거리").fill("2345")
    logging.info("PASS : 주행거리 입력")
    time.sleep(1)

    page.get_by_role("button", name="차량정보 완료").click()
    logging.info("PASS : [차량정보 완료] 버튼 선택")
    time.sleep(3)

    '''    page.get_by_role("button", name="확인").click()
    logging.info("PASS : [확인] 버튼 선택")
    time.sleep(5)
    '''
    logging.info(f"PASS : 차량정보 Tab 완료")


    context.close()
    browser.close()

with sync_playwright() as playwright:
    VehicleInfo(playwright)
