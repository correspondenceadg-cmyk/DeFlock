import traceback
from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from deflock.screens.main import MainScreen

APP_DIR = Path(__file__).resolve().parent


def asset_path(relative_path):
    return str(APP_DIR / relative_path)


def log_path():
    app = App.get_running_app()
    if app is not None:
        return str(Path(app.user_data_dir) / "deflock_crash.log")
    return str(APP_DIR / "deflock_crash.log")


def log_crash(exc_text):
    try:
        with open(log_path(), "w") as f:
            f.write(exc_text)
    except Exception:
        pass


Window.clearcolor = (0.06, 0.04, 0.03, 1)


class DeFlockApp(App):
    title = "DeFlock"

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.current = "main"
        return sm


def main():
    try:
        DeFlockApp().run()
    except Exception:
        log_crash(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
