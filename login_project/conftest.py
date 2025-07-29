import glob
import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function", autouse=True)
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
def screenshot_on_failure(page, request):
    yield
    if request.node.rep_call.failed:
        screenshot_path = Path(f"screenshots/{request.node.name}.png")
        page.screenshot(path=screenshot_path, full_page=True)
        if hasattr(request.node, "allure_attach"):
            request.node.allure_attach(screenshot_path)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Добавляем атрибуты в тест для доступа из фикстур
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    
    if rep.failed:
        # найти видео
        video_files = glob.glob("test-results/**/video.webm", recursive=True)
        if video_files:
            latest_video = video_files[-1]
            allure.attach.file(latest_video, name="Video", attachment_type=allure.attachment_type.WEBM)

 # Для Allure
    if rep.failed and hasattr(item, "allure_attach"):
        import allure
        screenshot_path = Path(f"screenshots/{item.name}.png")
        allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)
