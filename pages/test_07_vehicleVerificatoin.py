from playwright.sync_api import sync_playwright
import re
from config import dealer_id, dealer_pw



def test_example():
    with sync_playwright() as p:
        # 브라우저 및 페이지 설정
        browser = p.chromium.launch(
            headless=False,  # GUI 모드
            args=["--start-fullscreen"]  # 전체 화면 모드
        )
        context = browser.new_context()
        page = context.new_page()


        car_id = '28709914'

        # 페이지 진입
        page.goto("https://tfem.encar.com/car-verification/forms/basic/" + car_id)

        # 검수 페이지 이동
        page.get_by_role("link", name="encar ci").nth(1).click()
        page.get_by_placeholder("아이디").click()
        page.get_by_placeholder("아이디").fill(dealer_id)
        page.get_by_placeholder("비밀번호").click()
        page.get_by_placeholder("비밀번호").fill(dealer_pw)
        page.get_by_role("button", name="로그인").click()
        page.wait_for_timeout(2000)

        page.wait_for_timeout(1000)

        page.goto("https://tfem.encar.com/car-verification/forms/basic/" + car_id)

        # 기본정보
        page.get_by_role("button", name="자세히보기").first.click()
        page.wait_for_timeout(1000)
        page.get_by_label("전면 사진 등록").set_input_files("Photo/Sclass 007.jpeg")

        page.get_by_role("button", name="자세히보기").nth(1).click()
        page.get_by_label("후면 사진 등록").set_input_files("Photo/Sclass 008.jpeg")

        page.get_by_role("button", name="자세히보기").nth(2).click()
        page.wait_for_timeout(1000)
        page.get_by_label("2개").check()
        page.locator("div").filter(has_text=re.compile(r"^차량키통과차량 키 수량1개2개3개사진내용 입력하기$")).get_by_label("",
                                                                                                       exact=True).first.set_input_files(
            "Photo/Sclass 011.jpeg")
        page.wait_for_timeout(500)
        page.locator("div").filter(has_text=re.compile(r"^제조사 매뉴얼있음없음$")).get_by_label("없음").check()
        page.wait_for_timeout(500)
        page.locator("div").filter(has_text=re.compile(r"^블랙박스있음없음사진내용 입력하기$")).get_by_label("",
                                                                                             exact=True).first.set_input_files(
            "Photo/Sclass 017.jpeg")
        page.wait_for_timeout(500)
        page.locator("div").filter(has_text=re.compile(r"^틴팅\(앞 유리\)있음없음통과 여부통과사진내용 입력하기$")).get_by_label("",
                                                                                                          exact=True).first.set_input_files(
            "Photo/Sclass 005.jpeg")
        page.wait_for_timeout(500)

        # 실내
        page.get_by_role("link", name="실내").click()
        page.get_by_role("button", name="자세히보기").first.click()
        page.get_by_role("button", name="자세히보기").nth(1).click()
        page.get_by_role("button", name="자세히보기").nth(2).click()

        # 휠타이어
        page.get_by_role("link", name="휠타이어").click()
        page.wait_for_timeout(2000)

        # 운전석 앞
        page.get_by_role("button", name="자세히보기").first.click()
        page.wait_for_timeout(1000)  # 0.5초 대기
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 009.jpeg")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(앞\\)_manufacturer\"]").select_option("미쉐린")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(앞\\)_productionDate\"]").fill("0424")
        page.wait_for_timeout(500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(앞\\)_tread\"]").fill("15")
        page.wait_for_timeout(500)

        # 운전석 뒤
        page.get_by_role("button", name="자세히보기").nth(1).click()
        page.wait_for_timeout(1000)  # 0.5초 대기
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 009.jpeg")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(뒤\\)_manufacturer\"]").select_option("미쉐린")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(뒤\\)_productionDate\"]").click()
        page.locator("[id=\"운전석\\ \\(뒤\\)_productionDate\"]").fill("0424")
        page.wait_for_timeout(500)  # 0.5초 대기
        page.locator("[id=\"운전석\\ \\(뒤\\)_tread\"]").click()
        page.locator("[id=\"운전석\\ \\(뒤\\)_tread\"]").fill("15")
        page.wait_for_timeout(500)

        # #동승석 뒤
        page.get_by_role("button", name="자세히보기").nth(2).click()
        page.wait_for_timeout(1000)  # 0.5초 대기
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 009.jpeg")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(뒤\\)_manufacturer\"]").select_option("미쉐린")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(뒤\\)_productionDate\"]").click()
        page.locator("[id=\"동승석\\ \\(뒤\\)_productionDate\"]").fill("0424")
        page.wait_for_timeout(500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(뒤\\)_tread\"]").click()
        page.locator("[id=\"동승석\\ \\(뒤\\)_tread\"]").fill("15")
        page.wait_for_timeout(500)

        # 동승석 앞
        page.get_by_role("button", name="자세히보기").nth(3).click()
        page.wait_for_timeout(1000)  # 0.5초 대기
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 009.jpeg")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(앞\\)_manufacturer\"]").select_option("미쉐린")
        page.wait_for_timeout(1500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(앞\\)_productionDate\"]").click()
        page.locator("[id=\"동승석\\ \\(앞\\)_productionDate\"]").fill("0424")
        page.wait_for_timeout(500)  # 0.5초 대기
        page.locator("[id=\"동승석\\ \\(앞\\)_tread\"]").click()
        page.locator("[id=\"동승석\\ \\(앞\\)_tread\"]").fill("15")
        page.wait_for_timeout(500)

        # 외관
        page.get_by_role("link", name="외관").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="자세히보기").first.click()
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 011.jpeg")
        page.wait_for_timeout(1500)

        page.get_by_role("button", name="자세히보기").nth(1).click()
        page.locator("div").filter(has_text=re.compile(r"^운전석 1열 시트\(필수\)통과사진내용 입력하기$")).get_by_label("",
                                                                                                      exact=True).first.set_input_files(
            "Photo/Sclass 002.jpeg")
        page.wait_for_timeout(1000)
        page.locator("div").filter(has_text=re.compile(r"^운전석 2열 시트\(필수\)통과사진내용 입력하기$")).get_by_label("").nth(
            1).set_input_files("Photo/Sclass 004.jpeg")
        page.wait_for_timeout(1500)

        page.get_by_role("button", name="자세히보기").nth(2).click()
        page.wait_for_timeout(1000)
        page.get_by_label("", exact=True).first.set_input_files("Photo/Sclass 019.jpeg")
        page.wait_for_timeout(1500)

        page.locator("div").filter(has_text=re.compile(r"^리페어장비있음없음$")).get_by_label("없음").check()
        page.wait_for_timeout(500)
        page.locator("div").filter(has_text=re.compile(r"^소화기있음없음$")).get_by_label("없음").check()

        page.get_by_role("button", name="자세히보기").nth(3).click()
        page.wait_for_timeout(1000)

        page.get_by_role("button", name="자세히보기").nth(4).click()
        page.wait_for_timeout(1000)

        # 부가정보
        page.get_by_role("link", name="부가정보").click()
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="자세히보기").nth(2).click()
        page.get_by_test_id("tarea").fill("테스트 차량입니다.")
        page.wait_for_timeout(1000)

        # 옵션
        page.get_by_role("link", name="옵션").click()
        page.wait_for_timeout(2000)
        page.get_by_role("button", name="자세히보기").first.click()
        page.locator(
            "div:nth-child(4) > .CarVerificationFormItem_header_group__-FCY5 > div > .TextInToggleSwitch_base__IaAm4 > .TextInToggleSwitch_label__-mtbD").click()
        page.wait_for_timeout(1000)
        page.get_by_label("", exact=True).set_input_files("Photo/Sclass 006.jpeg")
        page.wait_for_timeout(2000)

        page.get_by_role("button", name="등록").click()
        page.get_by_role("button", name="확인").click()
        page.wait_for_timeout(5000)

        # 브라우저 닫기
        browser.close()


if __name__ == "__main__":
    test_example()
