import os
import pytest
import allure
from pathlib import Path

@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "record_video_dir": "videos/",
        "record_video_size": {"width": 1280, "height": 720}
    }

@pytest.fixture(scope="function")
def context(playwright, browser_context_args):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()
    browser.close()

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page

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
