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
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)
        if page:
            # 📸 Сохраняем скриншот
            screenshot_path = f"allure-results/{item.name}_screenshot.png"
            page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)

            # 🎥 Обрабатываем видео (если есть)
            try:
                video = page.video
                if video:
                    raw_path = video.path()  # путь временного видеофайла
                    final_path = Path(f"videos/{item.name}.webm")
                    os.makedirs(final_path.parent, exist_ok=True)
                    page.context.close()  # нужно вызвать до move
                    shutil.move(raw_path, final_path)
                    allure.attach.file(str(final_path), name="video", attachment_type=allure.attachment_type.WEBM)
            except Exception as e:
                print(f"[!] Video save error: {e}")
