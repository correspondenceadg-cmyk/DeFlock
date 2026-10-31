import traceback
from pathlib import Path

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

APP_DIR = Path(__file__).resolve().parent

Window.clearcolor = (0.06, 0.04, 0.03, 1)


def _write_log(text):
    paths = ["/sdcard/deflock_error.log", str(APP_DIR / "deflock_error.log")]
    app = App.get_running_app()
    if app is not None:
        try:
            paths.append(str(Path(app.user_data_dir) / "deflock_error.log"))
        except Exception:
            pass
    for p in paths:
        try:
            Path(p).write_text(text)
            return p
        except Exception:
            continue
    return None


class ErrorScreen(Screen):
    def __init__(self, exc_text, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=8)
        header = Label(
            text="BOOT ERROR", size_hint=(1, None), height=30,
            color=(1, 0.4, 0.4, 1), font_size="16sp",
        )
        box.add_widget(header)
        sv = ScrollView()
        lbl = Label(
            text=exc_text, size_hint=(1, None),
            halign="left", valign="top",
            font_size="11sp", color=(1, 0.7, 0.7, 1),
        )
        lbl.bind(
            width=lambda inst, w: setattr(inst, "text_size", (w, None)),
            texture_size=lambda inst, sz: setattr(inst, "height", sz[1]),
        )
        sv.add_widget(lbl)
        box.add_widget(sv)
        self.add_widget(box)


class DeFlockApp(App):
    title = "DeFlock"

    def build(self):
        try:
            from deflock.screens.main import MainScreen
            sm = ScreenManager()
            sm.add_widget(MainScreen(name="main"))
            sm.current = "main"
            return sm
        except Exception:
            err = traceback.format_exc()
            _write_log(err)
            return ErrorScreen(err)


def main():
    try:
        DeFlockApp().run()
    except Exception:
        _write_log(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
