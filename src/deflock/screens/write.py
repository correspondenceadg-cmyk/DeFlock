import os
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

from deflock.engine.grammar import VERBS, ACTIONS, OBJECTS, CONDITIONS, PENALTIES
from deflock.engine.doctrine import create_doctrine

AMBER = (0.85, 0.65, 0.30, 1)
PAPER = (0.90, 0.85, 0.72, 1)
LEATHER = (0.10, 0.04, 0.02, 1)
BG    = (0.12, 0.08, 0.05, 1)

class WriteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        self.layout = BoxLayout(orientation="vertical", padding=dp(30), spacing=dp(10), size_hint=(0.9, 0.85), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        with self.layout.canvas.before:
            Color(*LEATHER)
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
            Color(0.30, 0.22, 0.12, 1)
            self.page = Rectangle(pos=(self.layout.pos[0]+dp(10), self.layout.pos[1]+dp(10)), size=(self.layout.size[0]-dp(20), self.layout.size[1]-dp(20)))
            
        self.layout.bind(size=self._update_rects, pos=self._update_rects)
        self.add_widget(self.layout)

        top_layout = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(32))
        title = Label(text="Inscribe a Verse", size_hint=(1, 1), color=AMBER, font_size="20sp", halign="left", valign="middle")
        title.bind(size=lambda *a: setattr(title, "text_size", title.size))
        top_layout.add_widget(title)
        
        cancel_btn = Button(text="X", size_hint=(None, 1), width=dp(32), background_normal="", background_color=(0.3, 0.1, 0.1, 1), color=PAPER)
        cancel_btn.bind(on_release=self._cancel)
        top_layout.add_widget(cancel_btn)
        self.layout.add_widget(top_layout)

        self.verse_input = TextInput(
            hint_text="The cup is not for the faithful while the sun is high...",
            multiline=False, size_hint=(1, None), height=dp(60),
            background_color=BG, foreground_color=PAPER, cursor_color=AMBER
        )
        self.layout.add_widget(self.verse_input)

        spinner_opts = {"size_hint": (1, None), "height": dp(40), "background_color": BG, "color": PAPER}
        self.spin_verb = Spinner(text='FORBID', values=VERBS, **spinner_opts)
        self.spin_action = Spinner(text='eat', values=ACTIONS, **spinner_opts)
        self.spin_object = Spinner(text='flesh', values=OBJECTS, **spinner_opts)
        self.spin_condition = Spinner(text='always', values=CONDITIONS, **spinner_opts)
        self.spin_penalty = Spinner(text='public shaming', values=PENALTIES, **spinner_opts)

        self.layout.add_widget(self.spin_verb)
        self.layout.add_widget(self.spin_action)
        self.layout.add_widget(self.spin_object)
        self.layout.add_widget(self.spin_condition)
        self.layout.add_widget(self.spin_penalty)
        self.layout.add_widget(Widget())

        commit_btn = Button(text="Inscribe", size_hint=(1, None), height=dp(50), background_normal="", background_color=(0.2, 0.15, 0.1, 1), color=AMBER, font_size="16sp")
        commit_btn.bind(on_release=self._commit)
        self.layout.add_widget(commit_btn)

    def _update_rects(self, *args):
        self.bg.pos = self.layout.pos
        self.bg.size = self.layout.size
        self.page.pos = (self.layout.pos[0]+dp(10), self.layout.pos[1]+dp(10))
        self.page.size = (self.layout.size[0]-dp(20), self.layout.size[1]-dp(20))

    def _cancel(self, instance):
        self.manager.current = "main"

    def _commit(self, instance):
        text = self.verse_input.text.strip()
        if not text:
            text = f"A verse concerning {self.spin_object.text}."

        new_doc = create_doctrine(
            verse_text=text, verb=self.spin_verb.text, action=self.spin_action.text,
            object_name=self.spin_object.text, condition=self.spin_condition.text, penalty=self.spin_penalty.text
        )
        
        main_screen = self.manager.get_screen("main")
        reveal_screen = self.manager.get_screen("reveal")
        
        reveal_screen.play_animation(new_doc, lambda: main_screen.finish_decree(new_doc))
        self.manager.current = "reveal"
        self.verse_input.text = ""
