import os
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
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            screenshot_path = f"allure-results/{item.name}_screenshot.png"
            page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)

        # Прикрепим видео, если оно есть
        video_dir = "videos"
        if os.path.exists(video_dir):
            for root, _, files in os.walk(video_dir):
                for file in files:
                    if file.endswith(".webm") and item.name in file:
                        video_path = os.path.join(root, file)
                        allure.attach.file(video_path, name="video", attachment_type=allure.attachment_type.WEBM)

 # Для Allure
    if rep.failed and hasattr(item, "allure_attach"):
        import allure
        screenshot_path = Path(f"screenshots/{item.name}.png")
        allure.attach.file(screenshot_path, name="Screenshot", attachment_type=allure.attachment_type.PNG)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/"
    }