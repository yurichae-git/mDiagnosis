import logging
logging.basicConfig(level=logging.INFO)
import time, re, random
from config import car_type, owner, dealer_id





def Reservation(page, car_number):


    page.get_by_role("link", name="현장 예약").click()
    logging.info(f"PASS : 현장예약 시작 - {car_number}")

    page.get_by_text("아이디 조회").click()
    page.get_by_role("textbox", name="아이디").click()
    page.get_by_role("textbox", name="아이디").fill(dealer_id)
    page.locator("#btnSearch").click()
    logging.info("PASS : 현장예약 > 아이디 조회")
    time.sleep(3)


    ##국산/수입/화물 선택
    page.get_by_text(car_type, exact=True).click()
    logging.info("PASS : 현장예약 > 차량정보 > 국산/수입 선택 ")

    page.get_by_role("textbox", name="차량번호").click()
    page.get_by_role("textbox", name="차량번호").fill(car_number)
    logging.info("PASS : 현장예약 > 차량정보 > 차량번호 입력")

    page.get_by_label("소유자명").select_option("직접입력")

    page.get_by_role("textbox", name="소유자명 입력").click()
    page.get_by_role("textbox", name="소유자명 입력").fill(owner)
    logging.info("PASS : 현장예약 > 차량정보 > 소유자명 입력")

    page.locator("div").filter(has_text=re.compile(r"^조회$")).get_by_role("button").click()
    logging.info(f"PASS : 현장예약 > 차량정보 > 차량정보 조회 중 - {car_number}")
    time.sleep(15)

    # 제조사/모델 조회 실패 케이스

    manufacturer = page.get_by_label("제조사", exact=True)
    model = page.get_by_label("모델", exact=True)
    detail_model = page.get_by_label("세부모델", exact=True)
    if manufacturer.count() > 0:
        # 현재 선택된 제조사 옵션 확인
        selected_manufacturer = manufacturer.evaluate("el => el.options[el.selectedIndex].text")
        selected_model = model.evaluate("el => el.options[el.selectedIndex].text")
        selected_detail_model = detail_model.evaluate("el => el.options[el.selectedIndex].text")
        if selected_manufacturer and selected_manufacturer != "제조사":
            logging.info(f"PASS : 현장예약 > 제조사 / 모델 > 조회 성공 - {selected_manufacturer}")
            if selected_model and selected_model == "모델":
                # 세부모델이 조회 된 경우 옵션 리스트를 가져와서 첫번째 옵션을 선택하고, 없을 땐 에러로그
                model.wait_for(state="enabled", timeout=10000)
                model_options = model.evaluate("el => Array.from(el.options).map(o => o.value)")
                if model_options and len(model_options) > 0:
                    model.select_option(model_options[0])
                    logging.info(f"PASS : 현장예약 > 제조사 / 모델 > 모델 조회 안된 경우 - 첫 번째 옵션 '{model_options[0]}' 선택")
                else:
                    logging.warning("PASS : 모 옵션이 없음")
            if selected_detail_model and selected_detail_model == "세부모델":
                # 세부모델이 조회 된 경우 옵션 리스트를 가져와서 첫번째 옵션을 선택하고, 없을 땐 에러로그
                detail_model.wait_for(state="enabled", timeout=10000)
                detail_model_options = detail_model.evaluate("el => Array.from(el.options).map(o => o.value)")
                if detail_model_options and len(detail_model_options) > 0:
                    detail_model.select_option(detail_model_options[0])
                    logging.info(f"PASS : 현장예약 > 제조사 / 모델 > 세부모델 조회 안된 경우 - 첫 번째 옵션 '{detail_model_options[0]}' 선택")
                else:
                    logging.warning("PASS : 세부모델 옵션이 없음")
        else: # 제조사/모델 조회 안된 경우 지정 선택
            if car_type == "국산":
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 미확인 차량")
                page.get_by_label("제조사").select_option("현대")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 제조사 선택 - 현대")
                time.sleep(1)
                page.get_by_label("모델", exact=True).select_option("베뉴")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 모델 선택 - 베뉴")
                time.sleep(1)
                page.get_by_label("세부모델").select_option("베뉴(19년~현재)")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 세부모델 선택 - 베뉴(19년~현재)")
                time.sleep(1)
            elif car_type == "수입":
                logging.info("PASS : 제조사 / 모델 미확인 차량")
                page.get_by_label("제조사").select_option("BMW")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 제조사 선택 - BMW")
                time.sleep(1)
                page.get_by_label("모델", exact=True).select_option("7시리즈")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 모델 선택 - 7시리즈")
                time.sleep(1)
                page.get_by_label("세부모델").select_option("7시리즈 (G70)(22년~현재)")
                logging.info("PASS : 현장예약 > 제조사 / 모델 > 세부모델 선택 - 7시리즈 (G70)(22년~현재)")
                time.sleep(1)
            else:
                logging.info("FAIL : 현장예약 > 제조사 / 모델 > 차량 유형이 국산/수입이 아님")
    else:
        logging.info("FAIL : 현장예약 > 제조사 / 모델 > 제조사 요소 확인 불가")


    page.get_by_text("진단등록").click()
    logging.info("PASS : 현장예약 > 상품 - 진단등록 선택")
    page.get_by_text("홈서비스 광고이용권").click()
    logging.info("PASS : 현장예약 > 상품 - 홈서비스 광고이용권 선택")




    page.get_by_role("button", name="등록", exact=True).click()
    logging.info("PASS : 현장예약 > 등록 선택")
    time.sleep(3)

    reservationConfirmPopup = page.get_by_role("button", name="확인")
    reservationConfirmPopup.wait_for(state="visible", timeout=5000)
    if reservationConfirmPopup.count() > 0 :
        reservationConfirmPopup.click()
        logging.info("PASS : 현장예약 > 확인 팝업 > 확인 버튼 선택")
    else :
        logging.info("FAIL : 현장예약 > 확인 팝업 미노출")
    time.sleep(5)

    logging.info(f"PASS : 현장예약 완료 - {car_number}")

