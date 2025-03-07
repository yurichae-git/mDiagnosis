import logging
logging.basicConfig(level=logging.INFO)
import time


def Login(page):
    page.goto("https://tdiag.encar.io/dev_login")
    page.get_by_role("link", name="로그인").click()
    logging.info("PASS : 로그인")
    time.sleep(2)

    page.locator('xpath=//*[@id="Header__Xpu4w"]/button/span').scroll_into_view_if_needed()     # 사이드바 열 때 스크롤 처리 필요
    page.locator('xpath=//*[@id="Header__Xpu4w"]/button/span').click()

    logging.info("PASS : 햄버거버튼 선택")

    time.sleep(2)
    page.get_by_role("link", name="지점 변경").click()
    page.get_by_role("button", name="서울").click()
    page.get_by_text("본사 광고지원센터").click()
    page.get_by_role("button", name="저장").click()
    logging.info("PASS : 지점 변경")
