import sys
import traceback

_import_ok = False
_import_err = ""
try:
    from deflock.app import DeFlockApp
    _import_ok = True
except Exception:
    _import_err = traceback.format_exc()

try:
    with open("/sdcard/deflock_main_ran.log", "w") as f:
        f.write("main.py ran\n")
        f.write("import ok: %s\n" % _import_ok)
        if not _import_ok:
            f.write(_import_err)
except Exception:
    pass

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

Window.clearcolor = (0.06, 0.04, 0.03, 1)

if _import_ok:
    AppClass = DeFlockApp
else:
    class _ErrScreen(Screen):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            box = BoxLayout(orientation="vertical", padding=10)
            box.add_widget(Label(
                text="IMPORT FAILED — see /sdcard/deflock_main_ran.log",
                size_hint=(1, None), height=40,
                color=(1, 0.4, 0.4, 1), font_size="14sp",
            ))
            sv = ScrollView()
            lbl = Label(
                text=_import_err or "(empty error)", size_hint=(1, None),
                halign="left", valign="top",
                font_size="10sp", color=(1, 0.7, 0.7, 1),
            )
            lbl.bind(
                width=lambda inst, w: setattr(inst, "text_size", (w, None)),
                texture_size=lambda inst, sz: setattr(inst, "height", sz[1]),
            )
            sv.add_widget(lbl)
            box.add_widget(sv)
            self.add_widget(box)

    class _ErrApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(_ErrScreen(name="err"))
            return sm

    AppClass = _ErrApp

if __name__ == "__main__":
    AppClass().run()
