import random
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from deflock.engine.state import new_campaign
from deflock.engine.scenes import SCENES, pick_scene, scene_prose
from deflock.engine.turn import resolve


AMBER = (0.85, 0.65, 0.30, 1)
PAPER = (0.90, 0.85, 0.72, 1)
DIM   = (0.55, 0.45, 0.30, 1)
BG    = (0.06, 0.04, 0.03, 1)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.campaign = None
        self._build_ui()
        self._start_new_campaign()

    def _build_ui(self):
        root = BoxLayout(orientation="vertical", padding=16, spacing=10)
        self.add_widget(root)

        self.top_bar = Label(
            text="DeFlock",
            size_hint=(1, None), height=32,
            color=AMBER, font_size="20sp",
            halign="left", valign="middle",
        )
        self.top_bar.bind(size=lambda *a: setattr(self.top_bar, "text_size", self.top_bar.size))
        root.add_widget(self.top_bar)

        self.status = Label(
            text="",
            size_hint=(1, None), height=22,
            color=DIM, font_size="12sp",
            halign="left", valign="middle",
        )
        self.status.bind(size=lambda *a: setattr(self.status, "text_size", self.status.size))
        root.add_widget(self.status)

        self.scene_label = Label(
            text="",
            size_hint=(1, 0.30),
            color=PAPER, font_size="15sp",
            halign="left", valign="top",
        )
        self.scene_label.bind(size=lambda *a: setattr(self.scene_label, "text_size", self.scene_label.size))
        root.add_widget(self.scene_label)

        options_box = BoxLayout(orientation="vertical", size_hint=(1, 0.28), spacing=6)
        self.option_buttons = {}
        specs = [
            ("comply", "[C]  Comply"),
            ("refuse", "[R]  Refuse"),
            ("social", "[S]  Social"),
            ("decree", "[D]  Withdraw and decree"),
            ("purge",  "[P]  Purge"),
        ]
        for key, label in specs:
            b = Button(
                text=label,
                size_hint=(1, None), height=44,
                background_normal="",
                background_color=(0.15, 0.10, 0.06, 1),
                color=PAPER, font_size="14sp",
            )
            b.bind(on_release=lambda btn, k=key: self._on_action(k))
            self.option_buttons[key] = b
            options_box.add_widget(b)
        root.add_widget(options_box)

        log_box = BoxLayout(orientation="vertical", size_hint=(1, 0.28))
        log_header = Label(
            text="EVENTS",
            size_hint=(1, None), height=18,
            color=AMBER, font_size="11sp",
            halign="left", valign="middle",
        )
        log_header.bind(size=lambda *a: setattr(log_header, "text_size", log_header.size))
        log_box.add_widget(log_header)
        self.log_scroll = ScrollView()
        self.log_label = Label(
            text="",
            color=PAPER, font_size="12sp",
            halign="left", valign="top",
        )
        self.log_label.bind(size=lambda *a: setattr(self.log_label, "text_size", self.log_label.size))
        self.log_scroll.add_widget(self.log_label)
        log_box.add_widget(self.log_scroll)
        root.add_widget(log_box)

    def _start_new_campaign(self):
        seed = random.randint(0, 2**31 - 1)
        self.campaign = new_campaign(seed)
        self.campaign.current_scene = pick_scene(seed, 1)
        self.campaign.next_scene = pick_scene(seed, 2)
        self.refresh()

    def refresh(self):
        c = self.campaign
        self.top_bar.text = f"DeFlock  ·  Turn {c.turn} of {c.max_turns}"
        self.status.text = self._band_line(c)

        scene = SCENES[c.current_scene]
        prose = scene_prose(c.current_scene, c.seed, c.turn)
        compulsion = (
            f"You are asked to {scene.compelled_action} {scene.compelled_object} "
            f"({', '.join(scene.conditions)})."
        )
        self.scene_label.text = f"{scene.name}\n\n{prose}\n\n{compulsion}"
        self._update_options(scene)
        self._update_log()

    def _band_line(self, c):
        zeal_band = self._band(c.zeal_pool / max(c.flock_size, 1),
                               ["Cold", "Warm", "Hot", "Feverish"])
        comfort_band = self._band(c.comfort_pool / max(c.flock_size, 1),
                                  ["Strained", "Thin", "Settled", "Copacetic"])
        return (f"Flock {c.flock_size}  ·  Zeal {zeal_band}"
                f"  ·  Comfort {comfort_band}  ·  Strain {c.strain}")

    def _band(self, avg, names):
        if avg < 25: return names[0]
        if avg < 50: return names[1]
        if avg < 75: return names[2]
        return names[3]

    def _update_options(self, scene):
        self.option_buttons["comply"].text = (
            f"[C]  Comply — {scene.compelled_action} {scene.compelled_object}"
        )
        self.option_buttons["social"].text = (
            f"[S]  Social — {scene.social_action} {scene.social_object}"
        )
        self.option_buttons["decree"].disabled = not scene.withdrawable
        has_faction = any(f.faction for f in self.campaign.followers)
        self.option_buttons["purge"].disabled = not has_faction

    def _update_log(self):
        if not self.campaign.events:
            self.log_label.text = "  (nothing yet)"
            return
        lines = [f"T{e['turn']:>2}   {e['text']}" for e in self.campaign.events[-30:]]
        self.log_label.text = "\n".join(lines)

    def _on_action(self, action: str):
        scene = SCENES[self.campaign.current_scene]
        if action == "decree" and not scene.withdrawable:
            return
        if action == "purge" and not any(f.faction for f in self.campaign.followers):
            return

        self.campaign, _new = resolve(self.campaign, action)

        if self.campaign.turn > self.campaign.max_turns:
            self.scene_label.text = (
                "The year has ended.\n\nThe reveal waits for a later slice."
            )
            for b in self.option_buttons.values():
                b.disabled = True
            self._update_log()
            return

        self.refresh()
