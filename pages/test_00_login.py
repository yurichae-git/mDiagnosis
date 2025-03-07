import logging
logging.basicConfig(level=logging.INFO)
import time


def Login(page):
    page.goto("https://tdiag.encar.io/dev_login")
    page.get_by_role("link", name="로그인").click()
    logging.info("PASS : 로그인")
    time.sleep(2)

    # 햄버거버튼 사이드바 스크롤, 대기, 클릭
    page.locator('xpath=//*[@id="Header__Xpu4w"]/button/span').scroll_into_view_if_needed()     # 사이드바 열 때 스크롤 처리 필요
    page.locator('xpath=//*[@id="Header__Xpu4w"]/button/span').wait_for(state="visible", timeout=10000)
    page.locator('xpath=//*[@id="Header__Xpu4w"]/button/span').click()
    logging.info("PASS : 햄버거버튼")


    page.get_by_role("link", name="지점 변경").wait_for(state="visible", timeout=10000)
    page.get_by_role("link", name="지점 변경").click()
    logging.info("PASS : 햄버거버튼 > 지점 변경")

    page.get_by_role("button", name="서울").wait_for(state="visible", timeout=10000)
    page.get_by_role("button", name="서울").click()
    logging.info("PASS : 햄버거버튼 > 지점 변경 > 서울")

    page.get_by_text("본사 광고지원센터").wait_for(state="visible", timeout=10000)
    page.get_by_text("본사 광고지원센터").click()
    logging.info("PASS : 햄버거버튼 > 지점 변경 > 서울 > 본사 광고지원센터")

    page.get_by_role("button", name="저장").click()
    logging.info("PASS : 햄버거버튼 > 지점 변경 > 서울 > 본사 광고지원센터 > 지점 변경 성공")

    logging.info("PASS : 로그인 완료")
