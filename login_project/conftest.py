import os
import pytest
import shutil
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
    # получаем результат выполнения теста
    outcome = yield
    rep = outcome.get_result()

    # только если тест упал
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)

        # сохраняем скриншот
        if page:
            screenshot_path = f"allure-results/{item.name}_screenshot.png"
            page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(
                screenshot_path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

        # ищем и прикрепляем видео
        video_dir = "videos"
        if os.path.exists(video_dir):
            for root, _, files in os.walk(video_dir):
                for file in files:
                    if file.endswith(".webm"):
                        source_path = os.path.join(root, file)
                        target_path = f"allure-results/{item.name}_video.webm"
                        shutil.copyfile(source_path, target_path)
                        allure.attach.file(
                            target_path,
                            name="Video",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                        break  # достаточно одного видео
